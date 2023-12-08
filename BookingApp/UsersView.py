
import json
import os
from urllib.parse import urlencode
import uuid
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework import status
import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import generics,status
from rest_framework.response import Response
from decouple import Config
from .models import *
from .serializers import *

load_dotenv()
ip=os.getenv('ip')

class CustomOAuthAuthorizeView(View):
    def get(self, request):
      
        response=request.GET.get('reponse')
        return response
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AdminLogin(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        try:
            user = request.data.get('username')
            password = request.data.get('password')
            admin = User.objects.get(userName=user)
        except User.DoesNotExist:
            return Response({'message': 'Invalid Username'}, status=status.HTTP_226_IM_USED)

        admin_data = json.loads(admin.data)

        if password == admin_data['password']:
            user_session_token = str(uuid.uuid4())
            last_redirect_param = {
                'userId': admin.userId,
                'sessionToken': user_session_token
            }
            return Response(last_redirect_param, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Invalid Password'}, status=status.HTTP_226_IM_USED)

       
       


class UserLogin(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request):
            state=request.GET.get('state')
            
            if (state=='finished'):
                return JsonResponse({'data':'nothing'})
            print(ip)
            
            redirect_uri = ip+'userlogin/'

            authorization_code = request.GET.get('code')
           

            load_dotenv()
            client_id = '1XDTUULqBMBdeIy4GyMEBuAwl8CWTjvzeTpr29Hy'
            client_secret = os.getenv('client_secret')

           
            token_url = 'https://channeli.in/open_auth/token/?'
            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
                'code': authorization_code,
            }
            response = requests.post(token_url, data=data)
        
            if response.status_code == 200:
                
                token_data = response.json()
                access_token = token_data['access_token']
                
            
                user_data_url = 'https://channeli.in/open_auth/get_user_data/?'  
                headers = {
                    'Authorization': f'Bearer {access_token}',
                }
                response = requests.get(user_data_url, headers=headers)
                userSessionToken=str(uuid.uuid4())
                if response.status_code == 200:
                    user_data = response.json()
                    poster={
                        'userId':user_data['userId'],
                        'userName':user_data['person']['fullName'],
                        'data':json.dumps(user_data),
                        'penalties':0,
                        'ammenityProvider':False,
                        'userSession': userSessionToken
                    }
                    poster=json.dumps(poster)
                    headers = {
        'Content-Type': 'application/json',
    }
                    

                    
                    response = requests.post(ip+'user/?', data=poster,headers=headers)
                    last_redirect_param={
                        'state':'finished',
                        'userId': user_data['userId'],
                        'sessionToken':userSessionToken }
                   
                    return redirect(ip+'userlogin/?'+urlencode(last_redirect_param))
                     
                else:
                    return redirect(ip+'user/')
            else:
                return redirect(ip+'user/')

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        try:
            User.objects.get(userId=user_id)
           
        except User.DoesNotExist:
            
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

class AddPenalty(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.penalties += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return redirect(ip+'user/')

class UserByName(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user = get_object_or_404(self.get_queryset(), userName=username)
        return Response({'userId': user.userId})
class UserSessionView(generics.RetrieveAPIView):
    queryset = User.objects.all()  # Replace 'User' with your actual User model

    def retrieve(self, request, *args, **kwargs):
        userSession = self.kwargs.get('userSession')
        
        user = get_object_or_404(self.get_queryset(), userSession=userSession)
                
        return Response({'userId': user.userId})

class UserRegex(generics.ListCreateAPIView):
    lookup_field = 'userName'
    serializer_class = UserSerializer

    def get_queryset(self):
        substring = self.kwargs.get('userName')
        if substring is not None:
            queryset = User.objects.filter(userName__icontains=substring)
        else:
            queryset = User.objects.all()
        return queryset
        
class UserUpdateSessionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        session = self.kwargs.get('userSession')  

        if session:
            instance.userSession = session
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid session provided.'}, status=status.HTTP_400_BAD_REQUEST)