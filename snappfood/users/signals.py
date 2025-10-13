from users.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import requests



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        
        data = {
            "username": instance.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
           #"lat": profile.location.lat,
           #"long": profile.location.long,
        }
  
        urls = [
            "http://localhost:8001/api/create-user/",
            "http://localhost:8002/api/create-user/",
            "http://localhost:8003/api/create-user/",
        ]

        for url in urls:
            try:
                response = requests.post(url, json=data, timeout=5)
                print(f"✅ Sent to {url} → {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Could not send to {url}: {e}")