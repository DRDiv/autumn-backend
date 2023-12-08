from datetime import datetime
import json
from urllib.parse import urlencode

import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *


class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def post(self, request, *args):
        print(request.data)
        userId=request.data.get('userId')
        eventName=request.data.get('eventName')
        eventDate=request.data.get('eventDate')
        minTeamSize=request.data.get('minTeamSize')
        maxTeamSize=request.data.get('maxTeamSize')
        payment=request.data.get('payment')
        eventPicture=request.data.get('eventPicture')
        user=get_object_or_404(User.objects.all(),userId=userId)
        eventDate = timezone.make_aware(datetime.fromisoformat(eventDate))
        event=Event(
            eventName=eventName, 
            eventPicture=eventPicture, 
            eventDate=eventDate,
            minTeamSize=minTeamSize,
            maxTeamSize=maxTeamSize,
            payment=payment,
            userProvider=user

        )
        event.save()
        return Response()

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventByName(generics.RetrieveAPIView):
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kwargs):
        eventname = self.kwargs.get('username')
        event = get_object_or_404(self.get_queryset(), eventName=eventname)
        return Response({'eventId': event.eventId})
    
class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class EventRegex(generics.ListCreateAPIView):
    lookup_field = 'eventName'
    serializer_class = EventSerializer

    def get_queryset(self):
        substring = self.kwargs.get('eventName')
        if substring is not None:
            queryset = Event.objects.filter(eventName__icontains=substring, eventDate__gt=timezone.now())
        else:
            queryset = Event.objects.all()
        return queryset
class EventUserProvider(generics.ListCreateAPIView):
    lookup_field ='userProvider'
    serializer_class=EventSerializer
    def get_queryset(self):
        userProvider = self.kwargs.get('userProvider')
        user=get_object_or_404(User.objects.all(),userId=userProvider)
        
        queryset = Event.objects.filter(userProvider=user)
        
        return queryset
