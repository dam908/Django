from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """GET /rooms/<id>/bookings/ — список броней конкретной комнаты"""
        room = self.get_object()
        bookings = room.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='free')
    def free_rooms(self, request):
        """GET /rooms/free/?start_time=<datetime>&end_time=<datetime>"""
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not start_time or not end_time:
            return Response(
                {"error": "Необходимо указать start_time и end_time"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from datetime import datetime
            from django.utils.dateparse import parse_datetime
            
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)

            if not start_time or not end_time:
                raise ValueError("Неверный формат даты")

        except Exception as e:
            return Response(
                {"error": f"Неверный формат даты и времени: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        rooms_with_bookings = Booking.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        ).values_list('room_id', flat=True)
        free_rooms = Room.objects.exclude(id__in=rooms_with_bookings)
        serializer = RoomSerializer(free_rooms, many=True)
        
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ['get', 'post', 'head', 'options'] 