from datetime import datetime
import json
from urllib.parse import urlencode
import uuid
from rest_framework import status
import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *
from django.db.models import Q


class RequestListView(generics.ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    def post(self, request):
        queryset = Request.objects.all()
        
        event_id = request.data.get('event_id') 
      
        if(event_id!=None):
            team_id = request.data.get('team_id') 
        
            
            payment_image = request.data.get('payment_image') 

            
           

            team=get_object_or_404(Team.objects.all(),teamId=team_id)
            event=get_object_or_404(Event.objects.all(),eventId=event_id)
            query=queryset.filter(teamId=team).filter(event=event).all()
            
            if query :
                return Response({"message": "Request already pending"})
            request = Request(
               
                event=event,
                teamId=team,
                capacity=team.users.count(),
                timeRequest=timezone.now(),
                payment=payment_image,
                userProvider=event.userProvider.userId
            )

            request.save()

           
        else:
           
            amenity_id=request.data.get('amenity_id')
            amenity=get_object_or_404(Amenity.objects.all(),amenityId=amenity_id)
            users=request.data.getlist('users')
            date=request.data.get('date')
            time=request.data.get('timeStart')
            userobj=[]
            date_time_format = "%Y-%m-%d %H:%M:%S.%f"
            dateSlot = datetime.strptime(date, date_time_format).date()
             
            timeStart = datetime.strptime(time, date_time_format).time()
          
            for indv in users:
                
                userind=get_object_or_404(User.objects.all(),userId=indv)
               
                userobj.append(userind)
               
                query=queryset.filter(  individuals__in=userobj,amenity=amenity,dateSlot=dateSlot,timeStart__contains=timeStart, ).all()
                
                if query.count()!=0:
                    return Response({'message':f"Request Already Pending for {userind.userName}"})

                query=Booking.objects.all().filter(  individuals__in=userobj,amenity=amenity,dateSlot=dateSlot,timeStart__contains=timeStart, ).all()
                
                if query.count()!=0:
                    return Response({'message':f"Booking Already Pending for {userind.userName}"})
            
            availability=AmenitySlot.objects.all().filter(amenity=amenity,amenityDate=dateSlot,amenitySlotStart__contains=timeStart)
            if (availability.count()>0 and availability.first().capacity<len(users)) or (amenity.capacity<len(users)):
                return Response({"message":"Count of people exceeds capacity"})
            

            request = Request(
               
                amenity=amenity,
                timeRequest=timezone.now(),
                capacity=len(users),
                
                dateSlot=dateSlot,
                timeStart=timeStart,
                userProvider=amenity.userProvider.userId

            )
            
            request.save()
            request.individuals.set(userobj)
        return Response({"message": "Request created successfully","code":200}, status=status.HTTP_201_CREATED)


class RequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
class RequestProvider(generics.ListAPIView):
    lookup_field = "userProvider"
    serializer_class = RequestSerializer

    def get_queryset(self):
        userId = self.kwargs['userProvider']
        queryset = Request.objects.filter(userProvider=userId)
        return queryset
class RequestByUser(generics.ListAPIView):
    serializer_class=RequestSerializer
    def get_queryset(self):
        userId = self.kwargs['userId']

        queryset = Request.objects.filter(   Q(individuals=userId) | Q(teamId__users=userId))
        return queryset
class RequestToBooking(generics.RetrieveUpdateDestroyAPIView):
    queryset=Request.objects.all()
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        requestObj = self.get_object()

        
       
        
       
        booking = Booking(
                event=requestObj.event,
            amenity=requestObj.amenity,
            timeRequest=requestObj.timeRequest,
            capacity=requestObj.capacity,
            teamId=requestObj.teamId,
            dateSlot=requestObj.dateSlot,
    timeStart=requestObj.timeStart,
            verified=False
        )
        if booking.amenity is not None:
            availability=AmenitySlot.objects.all().filter(amenity=booking.amenity,amenityDate=booking.dateSlot,amenitySlotStart__contains=booking.timeStart)
            if (availability.count()==0):
                if (booking.amenity.capacity-len(requestObj.individuals.all())>=0):
                    amenitySlot=AmenitySlot(
                        amenity=booking.amenity,
        amenityDate=booking.dateSlot,
        amenitySlotStart=booking.timeStart,
        amenitySlotEnd=AmenitySlot.objects.all().filter(amenity=booking.amenity,amenityDate=None,amenitySlotStart__contains=booking.timeStart).first().amenitySlotEnd,
        
        
        capacity=booking.amenity.capacity-len(requestObj.individuals.all())
                )
                    amenitySlot.save()
                    booking.save()
                    for individual in requestObj.individuals.all():
                            booking.individuals.add(individual)  
                    requestObj.delete()    
                    
            else:
                availability=availability.first()
                if (availability.capacity-len(requestObj.individuals.all())>=0):
                    availability.capacity-=len((requestObj.individuals.all()))
                    availability.save()
                    booking.save()

            
                    for individual in requestObj.individuals.all():
                            booking.individuals.add(individual)  
                    requestObj.delete()    
                     
        print(booking.event,booking.teamId)
        if booking.event is not None and booking.teamId is not None:
                        team = Team.objects.get(pk=booking.teamId.teamId)
                        team.bookedEvents.add(booking.event)
                        team.save()  
                        booking.save()
                        requestObj.delete() 
        return Response( status=status.HTTP_201_CREATED)
        




