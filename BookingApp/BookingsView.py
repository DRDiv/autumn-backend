import json
from urllib.parse import urlencode

import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *
from django.utils import timezone
from django.db.models import Q


class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer



class BookingUserView(generics.ListCreateAPIView):
    
    serializer_class = BookingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Booking.objects.filter(
            Q(individuals=user_id) &
            (Q(event__isnull=False, event__eventDate__gte=timezone.now()) |
             Q(amenity__isnull=False, dateSlot__gte=timezone.now().date()))
        )
        return queryset

class BookingTeamView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  

      
        try:
            user_teams = Team.objects.filter(users__userId=user_id)
        except Team.DoesNotExist:
            user_teams = []

      
        bookings = Booking.objects.filter(teamId__in=user_teams)
        return bookings