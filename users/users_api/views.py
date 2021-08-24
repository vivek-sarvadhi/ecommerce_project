from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from users.users_api.serializers import RegisterSerializer, LoginSerializer
from users.models import CustomUser, CustomUserToken
import string, random
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny
import datetime



class IndexAPIView(ListAPIView):

    def get(self, request, *args, **kwargs):
        return Response(data={'status':status.HTTP_202_ACCEPTED,'Message':'Hello world'},status=status.HTTP_202_ACCEPTED)


class LoginRegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email)

        if not user:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, "Message": "User email is not registerd", }, status=status.HTTP_400_BAD_REQUEST)

        if user:
            user = CustomUser.objects.get(email=email)

            letters = string.ascii_letters
            random_string = ''.join(random.choice(letters) for i in range(15))
            payload = {
                        'id': user.id, 
                        'email': user.email, 
                        'random_string': random_string, 
                        'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=1000)
                    }
            encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            CustomUserToken.objects.create(user=user, token=encoded_token)

            return Response(data={'status':status.HTTP_200_OK, 
                                    'Message':"Success fully login",
                                    'Result':{'email':email,'token':encoded_token}}, 
                                    status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


        email = serializer.validated_data['email']
        user_type = serializer.validated_data['user_type']

        if CustomUser.objects.filter(email=email).exists():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':"User email alredy register"},status=status.HTTP_400_BAD_REQUEST)
            
        if not CustomUser.objects.filter(email=email).exists():
            serializer.save()
            user = CustomUser.objects.get(email=email)

            letters = string.ascii_letters
            random_string = ''.join(random.choice(letters) for i in range(15))
            payload = {'id': user.id, 'email': user.email, 'random_string':random_string}
            encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            CustomUserToken.objects.create(user=user, token=encoded_token) 

            return Response(data={'status':status.HTTP_201_CREATED, 
                                    'Message':"Success fully register",
                                    'Result':{'email':email,'user_type':user_type,'token':encoded_token}}, 
                                    status=status.HTTP_201_CREATED)