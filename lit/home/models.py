from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models.signals import post_save

class EventDetails(models.Model):
    name = models.CharField(max_length = 50)
    venue = models.CharField(max_length = 100)
    description=models.TextField(max_length=1000)
    event_id=models.AutoField(primary_key=True)
    date = models.DateField()
    result = models.BooleanField(default=False)
    t5e = models.URLField()
    Alakananda=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Brahmaputra=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Cauvery=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Ganga=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Godavari=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Jamuna=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Krishna=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Mahanadhi=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Mandakini=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Narmada=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Pampa=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Saraswathi=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Sarayu=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Sharavati=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Sindhu=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Tamiraparani=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    Tapti=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    #approve = models.BooleanField(default = False)
    
    def __unicode__(self):
        return self.name
      
        
class Results(models.Model):
    position=models.DecimalField(max_digits = 1,decimal_places=0)
    event_id=models.DecimalField(max_digits=3, decimal_places=0)
    name=models.CharField(max_length=100)
    hostel=models.CharField(max_length=100)
    pts=models.DecimalField(max_digits=5, decimal_places=2)
    
    def __unicode__(self):
        return self.name
    
    
class Hostel(models.Model):
    hostel=models.CharField(max_length=1000)
    total=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    litsec_id=models.DecimalField(max_digits=3,decimal_places=0)
    socsec_id=models.DecimalField(max_digits=3,decimal_places=0)
    litsec_comments=models.CharField(max_length=100)
    socsec_comments=models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.hostel        

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    usertype = models.CharField(max_length = 20)
    rollno = models.CharField(max_length = 20)
    userid = models.AutoField(primary_key = True)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    		
    post_save.connect(create_user_profile, sender=User)	

class verticalDetails(models.Model):
	name = models.CharField(max_length = 100)
	description = models.TextField(max_length = 100)
	vert_id = models.AutoField(primary_key = True)

class vertical_to_event(models.Model):
	vert_id = models.DecimalField(max_digits = 5,decimal_places = 0)
	event_id = models.DecimalField(max_digits = 5,decimal_places = 0)
	
class vertical_to_scoord(models.Model):
	vert_id = models.DecimalField(max_digits = 5,decimal_places = 0)
	supercoord_id = models.DecimalField(max_digits = 5,decimal_places = 0)

class event_to_coord(models.Model):
	event_id = models.DecimalField(max_digits = 5,decimal_places = 0)
	coord_id = models.DecimalField(max_digits = 5,decimal_places = 0)

class temp_eventdetails(models.Model):
	name = models.CharField(max_length = 50)
	venue = models.CharField(max_length = 100)
	description=models.TextField(max_length=1000)
	event_id=models.DecimalField(max_digits = 5,decimal_places = 0)
	date = models.DateField()
	result = models.BooleanField()
	t5e = models. URLField()
	vert_id = models.DecimalField(max_digits = 5,decimal_places = 0)
	
	
