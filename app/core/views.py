"""
Views for handle event finder APIs.
"""
from decimal import Decimal
import httpx
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pagination import CustomPagination
from .models import Event
from .serializers import EventListSerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


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
class EventAPIView(APIView):
    """API view for event list."""
    def get(self, request):
        """Get the list of events."""

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
        next_14_days_events = Event.objects.filter(date__range=[current_date, end_date])
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(next_14_days_events, request)
        serializers = EventListSerializer(result_page, many=True)
        data = serializers.data
        # print(type(data), data)

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

        return paginator.get_paginated_response(data)





















# Asynchronous Try 😀

# from asgiref.sync import sync_to_async
# from adrf.views import APIView as aAPIView


# class EventList(aAPIView):
#     """Asynchronous API view for event list."""
#     async def get(self, request):
#         """Get the list of events."""

#         latitude = request.query_params.get('latitude', None)
#         longitude = request.query_params.get('longitude', None)
#         search_date = datetime.now().date()
#         print(search_date)

#         if not all([latitude, longitude]):
#             return Response({"error": "All three parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

#         async def fetch_weather(data):
#             """
#             Fetch weather for each events from external API asynchronously.
#             """
#             async with httpx.AsyncClient() as client:
#                 for event in data:
#                     city = event['city_name']    # noqa
#                     date = event['date']   # noqa
#                     url = f"some url"    # noqa
#                     res = await client.get(url)
#                     rdata = res.json()
#                     event['weather'] = rdata["weather"]

#         async def fetch_distance(data):
#             """
#             Fetch distance for each events from external API asynchronously.
#             """
#             async with httpx.AsyncClient() as client:
#                 for event in data:
#                     latitude1 = 40.7128    #latitude
#                     longitude1 = -74.0060    #longitude
#                     latitude2 = event['latitude']
#                     longitude2 = event['longitude']
#                     url = f"some url"     # noqa
#                     res = await client.get(url)
#                     rdata = res.json()
#                     event['distance_km'] = rdata["distance"]

#         events = await sync_to_async(Event.objects.all)()
#         serializers = EventListSerializer(events, many=True)
#         data = await self.get_sdata(serializers)
#         data = data[:10]

#         try:
#             await fetch_weather(data)
#             await fetch_distance(data)

#             for item in data:
#                 del item['time']
#                 del item['latitude']
#                 del item['longitude']

#             return Response(data, status=status.HTTP_200_OK)
#         except httpx.HTTPError as e:
#             return Response({"error": str(e)},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @sync_to_async
#     def get_sdata(self, srl):
#         """Get the data from serializers asynchronously."""
#         try:
#             return srl.data
#         except Exception:
#             raise Exception
