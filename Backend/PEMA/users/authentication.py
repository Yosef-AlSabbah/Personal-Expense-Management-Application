# from rest_framework import exceptions
# from rest_framework.authentication import BaseAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
#
#
# class RefreshTokenAuthentication(BaseAuthentication):
#     """
#     Custom authentication using the Refresh Token from the request body.
#     """
#
#     def authenticate(self, request):
#         refresh_token = request.data.get('refresh')
#         if not refresh_token:
#             return None  # No authentication attempted
#
#         try:
#             token = RefreshToken(refresh_token)
#             # Optionally, you can verify the token here
#             user_id = token['user_id']
#             # Fetch the user based on user_id
#             from django.contrib.auth import get_user_model
#             User = get_user_model()
#             user = User.objects.get(id=user_id)
#             return user, token
#         except Exception as e:
#             raise exceptions.AuthenticationFailed('Invalid refresh token')
