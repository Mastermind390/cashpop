from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UserLogin  # Import your UserProfile model
from django.utils.timezone import now

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(user_logged_in)
def track_login_streak(sender, request, user, **kwargs):
    today = now().date()

    # Check if today's login already recorded
    if not UserLogin.objects.filter(user=user, login_date=today).exists():
        UserLogin.objects.create(user=user, login_date=today)