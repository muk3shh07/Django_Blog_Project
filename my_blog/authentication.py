from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User


class CustomTokenAuthentication(BaseAuthentication):
    """
    Custom authentication using a token.
    """

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None

        # Replace with your actual token validation logic
        if token != "valid-token":
            raise AuthenticationFailed("Invalid or missing token.")

        # Retrieve the user associated with the token
        try:
            # Adjust this logic to retrieve a user based on your setup
            user = User.objects.get(
                username="SAM"
            )  # Example: fixed user for "valid-token"
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")

        return (user, None)
