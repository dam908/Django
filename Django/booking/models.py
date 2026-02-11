from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    has_projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Booking(models.Model):
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name="bookings"
    )
    user_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.room.name} ({self.start_time})"