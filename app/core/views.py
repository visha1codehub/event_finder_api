"""
Views for handle event finder APIs.
"""
from decimal import Decimal
import httpx
import time
from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .pagination import CustomPagination
from .models import Event
from .serializers import EventSerializer

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

import asyncio
from asgiref.sync import sync_to_async
from adrf.views import APIView as aAPIView

from concurrent.futures import ThreadPoolExecutor, as_completed

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

WCODE = "KfQnTWHJbg1giyB_Q9Ih3Xu3L9QOBDTuU5zwqVikZepCAzFut3rqsg"
DCODE = "IAKvV2EvJa6Z6dEIUqqd7yGAu7IZ8gaH-a0QO6btjRc1AzFu8Y3IcQ"


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='latitude',
            description="User's latitude.",
            required=True,
            type=OpenApiTypes.NUMBER,
        ),
        OpenApiParameter(
            name='longitude',
            description="User's longitude.",
            required=True,
            type=OpenApiTypes.NUMBER,
        ),
    ]
)
class SyncEventListView(generics.ListAPIView):
    """Synchronous API view for event list."""
    serializer_class = EventSerializer
    queryset = Event
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        """Get the list of events synchronously."""
        s = time.perf_counter()
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        if not all([latitude, longitude]):
            return Response({"error": "Latitude and Longitude parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            latitude = Decimal(latitude)
            longitude = Decimal(longitude)
        except Exception as ex:
            print(ex)
            return Response({"error": "Invalid paramters."}, status=status.HTTP_400_BAD_REQUEST)

        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=14)
        next_14_days_events = self.queryset.objects.filter(
            date__range=[current_date, end_date])
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(next_14_days_events, request)
        serializers = self.get_serializer(result_page, many=True)
        data = serializers.data

        with httpx.Client() as client:
            for event in data:
                latitude1 = latitude
                longitude1 = longitude
                latitude2 = event['latitude']
                longitude2 = event['longitude']
                city = event['city_name']
                date = event['date']
                weather_url = f"https://gg-backend-assignment.azurewebsites.net/api/Weather?code={WCODE}==&city={city}&date={date}"    # noqa
                distance_url = f"https://gg-backend-assignment.azurewebsites.net/api/Distance?code={DCODE}==&latitude1={latitude1}&longitude1={longitude1}&latitude2={latitude2}&longitude2={longitude2}"   # noqa
                weather_res = client.get(weather_url)
                distance_res = client.get(distance_url)
                weather_res_data = weather_res.json()
                distance_res_data = distance_res.json()
                event['weather'] = weather_res_data["weather"]
                event['distance_km'] = distance_res_data["distance"]

        for event in data:
            del event['time']
            del event['latitude']
            del event['longitude']
        print("Sync Time: ", time.perf_counter()-s)
        return paginator.get_paginated_response(data)


class EventCreateView(generics.CreateAPIView):
    """View for creating a event."""
    queryset = Event
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cache.clear()
            self.perform_create(serializer)
            success_data = {
                "success": True,
                "message": "Event created successfully!",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data,
            }
            return Response(success_data, status=status.HTTP_201_CREATED)
        else:
            failed_data = {
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors,
            }
            return Response(failed_data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=EventSerializer,
    responses=None,
    parameters=[
        OpenApiParameter(
            name='latitude',
            description="User's latitude.",
            required=True,
            type=OpenApiTypes.NUMBER,
        ),
        OpenApiParameter(
            name='longitude',
            description="User's longitude.",
            required=True,
            type=OpenApiTypes.NUMBER,
        ),
    ],
)
class AsyncEventListView(aAPIView):
    """Asynchronous API view for event list."""

    async def get(self, request):
        """Get the list of events asynchronously."""
        s = time.perf_counter()
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        if not all([latitude, longitude]):
            return Response({"error": "Latitude and Longitude parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            latitude = Decimal(latitude)
            longitude = Decimal(longitude)
        except Exception as ex:
            print(ex)
            return Response({"error": "Invalid paramters."}, status=status.HTTP_400_BAD_REQUEST)

        async def get_cached_data(sdata):
            """Get the cached data if otherwise call fetch api."""
            data = cache.get(f'{latitude}-{longitude}')
            if data is None:
                data = await fetch_weather_distance(sdata)
                cache.set(f'{latitude}-{longitude}', data, timeout=60*15)
            return data

        async def get_all(url, d_url, event, client):
            """Async Method for Hit the urls."""
            weather_res = await client.get(url)
            weather_res_data = weather_res.json()
            event['weather'] = weather_res_data["weather"]
            distance_res = await client.get(d_url)
            distance_res_data = distance_res.json()
            event['distance_km'] = distance_res_data["distance"]
            return event

        async def fetch_weather_distance(data):
            """
            Fetch weather and distance for each events from external API asynchronously.
            """
            async with httpx.AsyncClient() as client:
                tasks = []
                for event in data:
                    latitude1 = latitude
                    longitude1 = longitude
                    latitude2 = event['latitude']
                    longitude2 = event['longitude']
                    city = event['city_name']
                    date = event['date']
                    w_url = f"https://gg-backend-assignment.azurewebsites.net/api/Weather?code={WCODE}==&city={city}&date={date}"    # noqa
                    d_url = f"https://gg-backend-assignment.azurewebsites.net/api/Distance?code={DCODE}==&latitude1={latitude1}&longitude1={longitude1}&latitude2={latitude2}&longitude2={longitude2}"   # noqa
                    tasks.append(asyncio.ensure_future(
                        get_all(w_url, d_url, event, client)))
                events_data = await asyncio.gather(*tasks)
                return events_data

        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=14)
        next_14_days_events = await sync_to_async(Event.objects.filter)(date__range=[current_date, end_date])
        paginator = CustomPagination()
        result_page = await sync_to_async(paginator.paginate_queryset)(next_14_days_events, request)
        serializers = EventSerializer(result_page, many=True)
        data = await self.get_sdata(serializers)

        try:
            data = await get_cached_data(data)

            for item in data:
                del item['time']
                del item['latitude']
                del item['longitude']
            print("Async Time: ", time.perf_counter()-s)
            return paginator.get_paginated_response(data)
        except httpx.HTTPError as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @sync_to_async
    def get_sdata(self, srl):
        """Get the data from serializers asynchronously."""
        try:
            return srl.data
        except Exception:
            raise Exception


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='latitude',
            description="User's latitude.",
            required=True,
            type=OpenApiTypes.NUMBER,
        ),
        OpenApiParameter(
            name='longitude',
            description="User's longitude.",
            required=True,
            type=OpenApiTypes.NUMBER,
        ),
    ]
)
class ThreadEventListView(generics.ListAPIView):
    """Threading API view for event list."""

    serializer_class = EventSerializer
    queryset = Event
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        """Get the list of events using threads."""
        s = time.perf_counter()
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        if not all([latitude, longitude]):
            return Response({"error": "Latitude and Longitude parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            latitude = Decimal(latitude)
            longitude = Decimal(longitude)
        except Exception as ex:
            print(ex)
            return Response({"error": "Invalid paramters."}, status=status.HTTP_400_BAD_REQUEST)

        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=14)
        next_14_days_events = self.queryset.objects.filter(
            date__range=[current_date, end_date])
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(next_14_days_events, request)
        serializers = self.get_serializer(result_page, many=True)
        data = serializers.data

        def get_all(url, d_url, event, client):
            """Thread Method for Hit the urls."""
            weather_res = client.get(url)
            weather_res_data = weather_res.json()
            event['weather'] = weather_res_data["weather"]
            distance_res = client.get(d_url)
            distance_res_data = distance_res.json()
            event['distance_km'] = distance_res_data["distance"]
            return event

        def fetch_weather_distance(data):
            """
            Fetch weather and distance for each events from external API using threads.
            """
            with ThreadPoolExecutor(max_workers=5) as executer:
                with httpx.Client() as client:
                    futures = []
                    for event in data:
                        latitude1 = latitude
                        longitude1 = longitude
                        latitude2 = event['latitude']
                        longitude2 = event['longitude']
                        city = event['city_name']
                        date = event['date']
                        w_url = f"https://gg-backend-assignment.azurewebsites.net/api/Weather?code={WCODE}==&city={city}&date={date}"    # noqa
                        d_url = f"https://gg-backend-assignment.azurewebsites.net/api/Distance?code={DCODE}==&latitude1={latitude1}&longitude1={longitude1}&latitude2={latitude2}&longitude2={longitude2}"   # noqa
                        futures.append(executer.submit(
                            get_all, w_url, d_url, event, client))
                    events_data = []
                    try:
                        for future in as_completed(futures):
                            events_data.append(future.result())
                        return events_data
                    except Exception as ex:
                        print(ex)

        try:
            data = fetch_weather_distance(data)

            for item in data:
                del item['time']
                del item['latitude']
                del item['longitude']
            print("Thread Time: ", time.perf_counter()-s)
            return paginator.get_paginated_response(data)
        except httpx.HTTPError as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
