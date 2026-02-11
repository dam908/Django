from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import logging
from .models import Room, Booking

logger = logging.getLogger(__name__)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'has_projector']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'user_name', 'start_time', 'end_time', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError(
                "Время окончания должно быть позже времени начала"
            )
        room = data['room']
        start_time = data['start_time']
        end_time = data['end_time']
        overlapping_bookings = Booking.objects.filter(
            room=room,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                "Комната уже забронирована на это время"
            )
        user_name = data['user_name']
        now = timezone.now()
        
        active_bookings = Booking.objects.filter(
            user_name=user_name,
            end_time__gt=now
        )

        if self.instance:
            active_bookings = active_bookings.exclude(pk=self.instance.pk)

        if active_bookings.count() >= 3:
            raise serializers.ValidationError(
                "Превышен лимит активных броней (максимум 3)"
            )
        time_until_booking = start_time - timezone.now()
        if time_until_booking < timedelta(minutes=10):
            logger.warning(
                f"Бронь создана менее чем за 10 минут до начала: "
                f"user={user_name}, room={room.name}, start_time={start_time}"
            )

        return data

    def create(self, validated_data):
        with transaction.atomic():
            return super().create(validated_data)