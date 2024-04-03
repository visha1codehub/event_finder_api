"""
Views for handle event finder APIs.
"""
import httpx
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from adrf.views import APIView as aAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pagination import CustomPagination
from .models import Event
from .serializers import EventListSerializer


class EventList(aAPIView):
    """Asynchronous API view for event list."""
    async def get(self, request):
        """Get the list of events."""

        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        search_date = datetime.now().date()
        print(search_date)

        if not all([latitude, longitude]):
            return Response({"error": "All three parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        async def fetch_weather(data):
            """
            Fetch weather for each events from external API asynchronously.
            """
            async with httpx.AsyncClient() as client:
                for event in data:
                    city = event['city_name']    # noqa
                    date = event['date']   # noqa
                    url = f"some url"    # noqa
                    res = await client.get(url)
                    rdata = res.json()
                    event['weather'] = rdata["weather"]

        async def fetch_distance(data):
            """
            Fetch distance for each events from external API asynchronously.
            """
            async with httpx.AsyncClient() as client:
                for event in data:
                    latitude1 = 40.7128    #latitude
                    longitude1 = -74.0060    #longitude
                    latitude2 = event['latitude']
                    longitude2 = event['longitude']
                    url = f"some url"     # noqa
                    res = await client.get(url)
                    rdata = res.json()
                    event['distance_km'] = rdata["distance"]

        events = await sync_to_async(Event.objects.all)()
        serializers = EventListSerializer(events, many=True)
        data = await self.get_sdata(serializers)
        data = data[:10]

        try:
            await fetch_weather(data)
            await fetch_distance(data)

            for item in data:
                del item['time']
                del item['latitude']
                del item['longitude']

            return Response(data, status=status.HTTP_200_OK)
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



class EventAPIView(APIView):
    """API view for event list."""
    def get(self, request):
        """Get the list of events."""

        events = Event.objects.all()
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=14)
        next_14_days_events = Event.objects.filter(date__range=[current_date, end_date])

        paginator = CustomPagination()
        # paginator.page_size = 10

        result_page = paginator.paginate_queryset(next_14_days_events, request)

        serializers = EventListSerializer(result_page, many=True)
        data = serializers.data
        # print(type(data), data)

        for item in data:
            del item['time']
            del item['latitude']
            del item['longitude']

        return paginator.get_paginated_response(data)
