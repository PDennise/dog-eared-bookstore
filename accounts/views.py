from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """Create a new user account. Public — no login required."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Read or update the logged-in user's profile."""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
       """Return the current user's profile, creating it if necessary."""
       profile, _ = Profile.objects.get_or_create(user=self.request.user)
       return profile
