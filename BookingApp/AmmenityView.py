import json
from urllib.parse import urlencode

import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *

from datetime import time

def parse_time(time_str):
    time_str = time_str.replace('TimeOfDay(', '').replace(')', '')
    hours, minutes = map(int, time_str.split(':'))
    return time(hours, minutes)
class AmenityListView(generics.ListCreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    def post(self, request, *args, **kwargs):
        print(request.data)
        userId=request.data.get('userId')
        amenityName=request.data.get('amenityName')
      
        recurance=request.data.get('recurance')
        amenityPicture=request.data.get('amenityPicture')
        user=get_object_or_404(User.objects.all(),userId=userId)
        start_times = [parse_time(start_time_str) for start_time_str in request.data.getlist('startTimes')]
        end_times = [parse_time(end_time_str) for end_time_str in request.data.getlist('endTimes')]
        capacity=request.data.get('capacity')
        amenity=Amenity(
            amenityName=amenityName,
            amenityPicture=amenityPicture,
            userProvider=user,
            recurrance=recurance,
            capacity=capacity,
        )
        amenity.save()
        for index in range(len(start_times)):
            amenitySlot=AmenitySlot(
                amenity=amenity,
                amenityDate=None,
                amenitySlotStart=start_times[index],
                amenitySlotEnd=end_times[index],
                capacity=capacity,
            )
            amenitySlot.save()
        return Response()

class AmenityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

class AmenityByName(generics.RetrieveAPIView):
    queryset = Amenity.objects.all()

    def retrieve(self, request, *args, **kwargs):
        amenityname = self.kwargs.get('username')
        amenity = get_object_or_404(self.get_queryset(), amenityName=amenityname)
        return Response({'amenityId': amenity.amenityId})
class AmenityRegex(generics.ListCreateAPIView):
    lookup_field = 'amenityName'
    serializer_class = AmenitySerializer

    def get_queryset(self):
        substring = self.kwargs.get('amenityName')
        if substring is not None:
            queryset = Amenity.objects.filter(amenityName__icontains=substring)
        else:
            queryset = Amenity.objects.all()
        return queryset
class AmmenitySlotTiming(generics.ListCreateAPIView):
    lookup_field = 'amenity'
    serializer_class = AmenitySlotSerializer
    def get_queryset(self):
        
        amenity = self.kwargs.get('amenityId')
        amenityobj=get_object_or_404(Amenity.objects.all(),amenityId=amenity)
        
        queryset = AmenitySlot.objects.filter(amenity=amenityobj,amenityDate__isnull=True)
        
        return queryset
class AmmenityUserProvider(generics.ListCreateAPIView):
    lookup_field ='userProvider'
    serializer_class=AmenitySerializer
    def get_queryset(self):
        userProvider = self.kwargs.get('userProvider')
        user=get_object_or_404(User.objects.all(),userId=userProvider)
        
        queryset = Amenity.objects.filter(userProvider=user)
        
        return queryset
