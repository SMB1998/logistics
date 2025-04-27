from django.db import models
import uuid
from users.models import Users
from discussion_board.models import DiscussionBoard

class DiscussionBoardRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discussion_board = models.ForeignKey(DiscussionBoard, on_delete=models.CASCADE, related_name='discussion_board_requests')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='discussion_board_requests')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if the status is being updated to 'approved'
        if self.pk and self.status == 'approved':
            # Add the user to the discussion board's users if not already added
            if self.user not in self.discussion_board.users.all():
                self.discussion_board.users.add(self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Request for {self.discussion_board.nombre} by {self.user.username}"