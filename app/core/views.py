"""
Views for handle event finder APIs.
"""
import httpx
from asgiref.sync import sync_to_async
from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventListSerializer


class EventList(APIView):
    """Asynchronous API view for event list."""
    async def get(self, request):
        """Get the list of events."""
        async def fetch_weather(sdata):
            """
            Fetch weather for each events from external API asynchronously.
            """
            async with httpx.AsyncClient() as client:
                for event in sdata:
                    city = event['city_name']
                    date = event['date']
                    url = f"someurl"
                    res = await client.get(url)
                    rdata = res.json()
                    event['weather'] = rdata["weather"]

        events = await sync_to_async(Event.objects.all)()
        serializers = EventListSerializer(events, many=True)
        data = await self.get_sdata(serializers)
        data = data[:10]

        try:
            await fetch_weather(data)
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

