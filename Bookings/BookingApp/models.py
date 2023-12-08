
import uuid
import django
from django.core.validators import *
from django.db import models
from django.utils import timezone



class User(models.Model):
    userId=models.CharField(max_length=100,primary_key=True,default='0')
    userName=models.CharField(max_length=100)
    data=models.JSONField(default=dict)
    penalties=models.IntegerField(default=0)
    ammenityProvider=models.BooleanField(default=False)
    userSession=models.CharField(max_length=100,blank=True)

class Event(models.Model):
    eventId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eventName=models.CharField(max_length=100)
    eventPicture=models.ImageField(upload_to='images/',null=True,blank=True)
    eventDate=models.DateTimeField(default=timezone.now)
    userProvider=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    minTeamSize=models.IntegerField(validators=[MinValueValidator(1)] ,default=1)
    maxTeamSize=models.IntegerField(default=1)
    payment=models.DecimalField(default=0,decimal_places=2,max_digits=10)
class Amenity(models.Model):
    amenityId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amenityName=models.CharField(max_length=100)
    amenityPicture=models.ImageField(upload_to='images/',blank=True)
    userProvider=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    recurrance=models.CharField(default='D',choices=[('D','daily'),('W','weekly'),('M','monthly'),('Y','yearly'),('O','onetime')])
    capacity=models.IntegerField(validators=[MinValueValidator(1)],default=1 )
class AmenitySlot(models.Model):
    
    amenity=models.ForeignKey(Amenity,on_delete=models.CASCADE)
    amenityDate=models.DateField(default=timezone.now,blank=True,null=True)
    amenitySlotStart=models.TimeField(default=timezone.now)
    amenitySlotEnd=models.TimeField(default=timezone.now)
    
    
    capacity=models.IntegerField(validators=[MinValueValidator(1)],default=1 )

class Team(models.Model):
    teamId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamName=models.CharField(max_length=100)
    
    users=models.ManyToManyField(User)
    isAdmin=models.JSONField(default=dict,blank=True)
    isReq=models.JSONField(default=dict,blank=True)
    bookedEvents=models.ManyToManyField(Event,blank=True)



class Request(models.Model):
    requestId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event=models.ForeignKey(Event, on_delete=models.CASCADE,blank=True,null=True)
    amenity=models.ForeignKey(Amenity, on_delete=models.CASCADE,blank=True,null=True)
    timeRequest=models.DateTimeField(default=timezone.now)
    capacity=models.IntegerField(validators=[MinValueValidator(1)],default=1 )
    payment=models.ImageField(upload_to='images/',null=True)
    teamId=models.ForeignKey(Team, on_delete=models.CASCADE,blank=True,null=True)
    individuals=models.ManyToManyField(User,blank=True)
    dateSlot=models.DateField(blank=True,null=True)
    timeStart=models.TimeField(blank=True,null=True)
    userProvider=models.CharField(default='')
    

class Booking(models.Model):
    bookingId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event=models.ForeignKey(Event, on_delete=models.CASCADE,blank=True,default=None,null=True)
    amenity=models.ForeignKey(Amenity, on_delete=models.CASCADE,blank=True,default=None,null=True)
    timeRequest=models.DateTimeField(default=timezone.now)
    capacity=models.IntegerField(validators=[MinValueValidator(1)] ,default=1)
    teamId=models.ForeignKey(Team, on_delete=models.CASCADE,default=None,blank=True,null=True)
    individuals=models.ManyToManyField(User,blank=True)
    verified=models.BooleanField(default=False)
    dateSlot=models.DateField(blank=True,null=True)
    timeStart=models.TimeField(blank=True,null=True)





