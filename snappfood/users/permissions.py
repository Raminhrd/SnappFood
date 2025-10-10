from users.models import UserProfile
from rest_framework.permissions import BasePermission
from django.utils import timezone


class IsNotBanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        return not profile.is_ban