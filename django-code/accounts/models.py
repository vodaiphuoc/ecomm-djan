from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from accounts.utils import get_avatar_color

# dont need to use Role table!
class AppUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )

    avatar = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_initial(self):
        return self.username[0].upper()

    @property
    def get_avatar_color(self)->str:
        """
        Gets a consistent background color for the letter avatar.
        We use the UUID as the unique identifier for hashing.
        """
        # Assuming 'id' is your UUIDField as per your model screenshot
        return get_avatar_color(self.id)
