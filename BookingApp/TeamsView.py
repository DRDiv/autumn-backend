import json
from urllib import response
from urllib.parse import urlencode

import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *


class TeamListView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    def post(self, request, *args, **kwargs):
      
        teamName = request.data.get('teamName')
        users = request.data.getlist('users')
        isAdmin_data = {}
        isReq_data={}
        for check in users:
            isAdmin_data[check]=(request.data.get(f'isAdmin[{check}]')=='true')
        for check in users:
            isReq_data[check]=(request.data.get(f'isReq[{check}]')=='true')
        userobj = []

        for indv in users:
            userindv = get_object_or_404(User.objects.all(), userId=indv)
            isAdmin = isAdmin_data.get(indv, False)  
            userobj.append(userindv)

        team = Team(
            teamName=teamName,
            isAdmin=isAdmin_data,  
            isReq=isReq_data
        )
        team.save()
        team.users.set(userobj)
        return Response()

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamByName(generics.RetrieveAPIView):
    queryset = Team.objects.all()

    def retrieve(self, request, *args, **kwargs):
        teamname = self.kwargs.get('username')
        team = get_object_or_404(self.get_queryset(), teamName=teamname)
        return Response({'teamId': team.teamId})

class ReqToTeam(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
 
    def post(self, request, *args, **kwargs):
        
        team = self.get_object()
        
        userid = request.POST.get('userId')
        state = request.POST.get('state')
        
        if state=='true':
            team.isReq[userid] = False
            team.save()
        else:
            user = get_object_or_404(User, userId=userid)
            team.users.remove(user)
            del team.isAdmin[(userid)]
            del team.isReq[userid]  
           
            team.save()

        return Response()


class AddUserToTeamView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
       
        team = self.get_object()
        userid = kwargs.get('userId')
        user = get_object_or_404(User, userId=userid)  

      
        team.users.add(user)
        team.isAdmin[user.userId]=False
        team.isReq[user.userId]=True
        team.save()
        serializer = self.get_serializer(team)
        return Response(serializer.data)
    
class MakeAdmin(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
        team = self.get_object()
        userid = kwargs.get('userId')
        user = get_object_or_404(User, userId=userid)

       

        team.isAdmin[user.userId]=True
        team.save()
        serializer = self.get_serializer(team)
        return Response(serializer.data)
    
class TeamUser(generics.ListAPIView):
    serializer_class = TeamSerializer  

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user_teams = Team.objects.filter(users__userId=user_id)
        except Team.DoesNotExist:
            user_teams = Team.objects.none()
        return user_teams
        