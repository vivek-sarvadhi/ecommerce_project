from rest_framework.authentication import TokenAuthentication, get_authorization_header
from users.models import CustomUser, CustomUserToken
from rest_framework import status, exceptions
from django.conf import settings
import jwt


class MyOwnTokenAuthentication(TokenAuthentication):

	model = CustomUser
	
	def get_model(self):
		return CustomUser

	
	def authenticate(self, request):

		auth = get_authorization_header(request).split()

		if not auth or auth[0].lower() != b'token':
			return None

		if len(auth) == 1:
			msg = 'Invalid token header. No credentials provided.'
			raise exceptions.AuthenticationFailed(msg)

		elif len(auth) > 2:
			msg = 'Invalid token header'
			raise exceptions.AuthenticationFailed(msg)


		try:
			token = auth[1]
			if token == "null":
				msg = "null token not allow"
				raise exceptions.AuthenticationFailed(msg)
		except UnicodeError:
			msg = 'Invalid token header. token string should not contain Invalid characters'
			raise exceptions.AuthenticationFailed(msg)

		return self.authentication_credential(token)


	def authentication_credential(self, token):
		model = self.get_model()
		try:
			payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
			id = payload['id']
			email = payload['email']
			token1 = token.decode('utf-8')
			try:
				try:
					user = CustomUser.objects.get(id=id, email=email)
				except:
					msg = {"Status": status.HTTP_404_NOT_FOUND, "detail": "User Not Found"}
					raise exceptions.AuthenticationFailed(msg)
				
				try:
					user_token = CustomUserToken.objects.get(user=user, token=token1)
				except:
					msg = {"Status": status.HTTP_404_NOT_FOUND, "detail": "Token Not Found"}
					raise exceptions.AuthenticationFailed(msg)
				
				if not str(token.decode('utf-8')) == str(user_token.token):
					msg = {"Status": status.HTTP_401_UNAUTHORIZED, "detail": "Token Missmatch"}
					raise exceptions.AuthenticationFailed(msg)
			except CustomUser.DoesNotExist:
				msg = {"Status" :status.HTTP_404_NOT_FOUND, "detail": "User Not Found"}
				raise exceptions.AuthenticationFailed(msg)

		except (jwt.InvalidTokenError,jwt.DecodeError,jwt.ExpiredSignatureError):
			msg = {"Status" :status.HTTP_401_UNAUTHORIZED, "detail": "Token is invalid"}
			raise exceptions.AuthenticationFailed(msg)

		return(user, token)

	def authenticate_header(self, request):
		return 'Token'
		
