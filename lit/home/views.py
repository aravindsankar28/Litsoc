from django.http import *
from django.shortcuts import *
from django.template import *
from models import *
from forms import *
from django.contrib import auth
from django.contrib.auth.models import User
from home.models import UserProfile
import time
from datetime import datetime
import os
from forms import UploadFileForm
from settings import *

def homepage(request):
	 a = 0
	 flop =  1
	 hostels = Hostel.objects.all().order_by('-total')
	 verticals = verticalDetails.objects.all()
	 files = []
	 os.system("./manage.py collectstatic") 
	 n = len(os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gallery','home_images').replace('\\','/')))
	 for name in os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gallery','home_images').replace('\\','/')): 
	 	files.append(name)
	 return render_to_response('HomePage.html',locals(),context_instance=RequestContext(request))
def calender(request):
	return render_to_response('calender.html',locals(),context_instance=RequestContext(request))	
    
def login(request):
	verticals=verticalDetails.objects.all()
	flop = 1
	events = EventDetails.objects.all()
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username,password=password)
		u=User.objects.get(username=username)
		if user.get_profile().usertype == "litsec" or user.get_profile().usertype == "socsec":
		    auth.login(request,user)
		    return HttpResponseRedirect("/litsoc/") 
		elif user is not None :
			auth.login(request,user)
			return HttpResponseRedirect("/corepage/")
		else:
			flop = 0
			return render_to_response('LoginPage.html',locals(),context_instance=RequestContext(request))  
	return render_to_response('LoginPage.html',locals(),context_instance=RequestContext(request))						                  
                
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/homepage/")

        
def litsoc(request):
    u=request.user
    flag=0
    if u.get_profile().usertype == "litsec":
        h=Hostel.objects.get(litsec_id=u.get_profile().userid)
        flag=1
        if request.method == 'POST':
            h.litsec_comments=request.POST['comments']
            h.save()
            return HttpResponseRedirect("/litsoc/")
    if u.get_profile().usertype == "socsec":
        h=Hostel.objects.get(socsec_id=u.get_profile().userid)
        flag=2
        if request.method == 'POST':
            h.socsec_comments=request.POST['comments']
            h.save()
            return HttpResponseRedirect("/litsoc/")
    return render_to_response('litsoc.html',locals(),context_instance=RequestContext(request))    
    
    
def corepage(request):
	flag=0
	approve = 0
	if not request.user.is_authenticated():
		flag=1
		return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
	name = request.user
	usertype  = name.get_profile().usertype
	verticals = verticalDetails.objects.all()
	if usertype == "supercoord":
		v = vertical_to_scoord.objects.get(supercoord_id = name.get_profile().userid)
		vert_id = v.vert_id
		vertical = verticalDetails.objects.get(vert_id = vert_id)
		verticalname = vertical.name							
	elif usertype == "coord":
		e = event_to_coord.objects.get(coord_id = name.get_profile().userid)
		event = EventDetails.objects.get(event_id = e.event_id)
		eventname = event.name

	return render_to_response('CorePage.html',locals(),context_instance=RequestContext(request))
    
def newevent(request,foobar):
    flag=0
    if not request.user.is_authenticated():
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    genvar=1
    e=EventDetails()
    if request.method == 'POST':
        e.name=request.POST['name']
        e.venue=request.POST['venue']
        e.date= request.POST['date']
        e.description=request.POST['description']
        e.t5e = request.POST['t5e']
        e.result=False     
        e.save()
        v = vertical_to_event(event_id = e.event_id)
        v.vert_id = foobar
        v.save()
        return HttpResponseRedirect("/corepage/")
    
    return render_to_response("newevent.html",locals(),context_instance=RequestContext(request))
    
def editevent(request,foobar):
    verticals = verticalDetails.objects.all()
    flag=0
    if not request.user.is_authenticated():
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    if request.user.is_authenticated() and request.user.get_profile().usertype=='coord':
        coords=event_to_coord.objects.filter(event_id=foobar)
        flag=2
        for coord in coords:
            if request.user.get_profile().userid == coord.coord_id:
                flag=3
        if flag==2:        
            flag=1
            return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    if request.user.is_authenticated() and request.user.get_profile().usertype=='supercoord':
        v=vertical_to_event.objects.get(event_id=foobar)
        scoords=vertical_to_scoord.objects.filter(vert_id=v.vert_id)
        flag=2
        for scoord in scoords:
            if request.user.get_profile().userid == scoord.supercoord_id:
                flag=3
        
        if flag==2:    
            flag=1
            return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
                
    genvar=2
    e=EventDetails.objects.get(event_id=foobar) 
    if request.method == 'POST':
    	if request.user.get_profile().usertype == 'coord':
    		try:
    		    t=temp_eventdetails.objects.get(event_id=foobar)
    		except:
    		    t=temp_eventdetails(event_id = foobar)
    		t.name=request.POST['name']
    		t.venue=request.POST['venue']
    		t.date= request.POST['date']
    		t.description=request.POST['description']
    		t.t5e = request.POST['t5e']
    		v=vertical_to_event.objects.get(event_id=foobar)
    		t.vert_id=v.vert_id
    		t.save()
    	else:
    		e.name=request.POST['name']
    		e.venue=request.POST['venue']
    		e.date= request.POST['date']
    		e.description=request.POST['description']
    		e.t5e = request.POST['t5e']
    		e.save()
    		
    		    
    	return HttpResponseRedirect("/corepage/")
    
    return render_to_response("newevent.html",locals(),context_instance=RequestContext(request))            
            
def events(request,foobar):
    verticals = verticalDetails.objects.all()
    display = 0
    e = EventDetails.objects.get(event_id = foobar)
    cids=event_to_coord.objects.filter(event_id=foobar)
    coords=[]
    for cid in cids:
	    up=UserProfile.objects.get(userid=cid.coord_id)
	    coords.append(up.user)
	    
    results=Results.objects.filter(event_id=foobar)
    resu=0
    if e.result == True:
        resu=1
    
    if request.user.is_authenticated():
        flag= 2
        usertype  = request.user.get_profile().usertype
        if usertype == "core":
            display = 1
            return render_to_response("events.html",locals(),context_instance=RequestContext(request))
        
        if usertype == "supercoord":
            v1=vertical_to_event.objects.get(event_id=foobar)
            scoords=vertical_to_scoord.objects.filter(vert_id=v1.vert_id)
            for scoord in scoords:
                if request.user.get_profile().userid == scoord.supercoord_id:
                    display = 1
                    return render_to_response("events.html",locals(),context_instance=RequestContext(request))
            
        if usertype == "coord":
    	    e1 = event_to_coord.objects.get(coord_id = request.user.get_profile().userid)
    	    if e1.event_id == int(foobar) :
    		    display = 1
    		    return render_to_response("events.html",locals(),context_instance=RequestContext(request))
    	    else:
    		    display = 0
    		    return render_to_response("events.html",locals(),context_instance=RequestContext(request))  	                    
        
        return render_to_response("events.html",locals(),context_instance=RequestContext(request))
    return render_to_response("events.html",locals(),context_instance=RequestContext(request))

def eventdetails(request):
    flag=0
    if request.user.is_authenticated():
        flag=1;
    events=EventDetails.objects.all()
    return render_to_response("eventdetails.html",locals(),context_instance=RequestContext(request))
  
def changepw(request):
    verticals = verticalDetails.objects.all()
    u=request.user
    u = request.user
    us=UserProfile.objects.get(user=u)
    if request.method =='POST':
		u.first_name=request.POST['first_name']
		u.last_name=request.POST['last_name']
		u.username=request.POST['username']
		us.rollno=request.POST['rollno']
		u.email=request.POST['email']
		oldpw = request.POST['oldpw']
		newpw = request.POST['newpw']
		confirm = request.POST['confirmpw']
		if u.check_password(oldpw) == True :
			u.set_password(newpw)
			u.save()
			us.save()
			return HttpResponseRedirect('/corepage/')
		flop = 0
		return render_to_response('Changepw.html',locals(),context_instance=RequestContext(request))
			
    return render_to_response('Changepw.html',locals(),context_instance=RequestContext(request))  
    
def changepw2(request):
    u=request.user
    u = request.user
    us=UserProfile.objects.get(user=u)
    if request.method =='POST':
        u.first_name=request.POST['first_name']
        u.last_name=request.POST['last_name']
        u.username=request.POST['username']
        us.rollno=request.POST['rollno']
        u.email=request.POST['email']
        oldpw = request.POST['oldpw']
        newpw = request.POST['newpw']
        confirm = request.POST['confirmpw']
        if u.check_password(oldpw) == True :
            u.set_password(newpw)
            u.save()
            us.save()
            return HttpResponseRedirect('/litsoc/')
        flop = 0
        return render_to_response('changepw2.html',locals(),context_instance=RequestContext(request))
			
    return render_to_response('changepw2.html',locals(),context_instance=RequestContext(request))  

def register(request,foobar):
    verticals = verticalDetails.objects.all()
    u=request.user
    if foobar == "supercoord":
        verticals=verticalDetails.objects.all()
    
    if foobar == "coord":
        vert=vertical_to_scoord.objects.get(supercoord_id=u.get_profile().userid)
        eventids=vertical_to_event.objects.filter(vert_id=vert.vert_id)
        events=[]
        for eid in eventids:
            events.append(EventDetails.objects.get(event_id=eid.event_id))
    
    if request.method == "POST" :
        flop = 0
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        rollno = request.POST['rollno']
        email = request.POST['email']
        username = request.POST['user_name']
        password = request.POST['password']
        select=request.POST['sel']
        try:
            check = User.objects.get(username =username)
        except User.DoesNotExist:
            check = None
        if check is None:
            s=User.objects.create_user(username,email,password)
            s.first_name=first_name
            s.last_name=last_name
            s.save()
            a=UserProfile.objects.get(user = s)
            a.usertype = foobar
            a.rollno=rollno
            a.save()
            if foobar == "supercoord": 
                v=verticalDetails.objects.get(name=select)
                v2s=vertical_to_scoord(vert_id=v.vert_id)
                v2s.supercoord_id=a.userid
                v2s.save()
                return HttpResponseRedirect('/corepage/')
                
            elif foobar == "coord":
                e=EventDetails.objects.get(name=select)
                e2c=event_to_coord(event_id=e.event_id)
                e2c.coord_id=a.userid
                e2c.save()
                return HttpResponseRedirect('/corepage/')  
        else:    
            flop = 1
            return render_to_response('register.html',locals(),context_instance=RequestContext(request))
        return render_to_response("register.html",locals(),context_instance=RequestContext(request))
    return render_to_response("register.html",locals(),context_instance=RequestContext(request))

def results(request,foobar):
    verticals = verticalDetails.objects.all()
    flag=0
    if not request.user.is_authenticated():
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    e=EventDetails.objects.get(event_id=foobar)
    hostels=Hostel.objects.all()
    r = [Results(event_id=foobar) for x in range(24)]
    z=0
    for x in range(1,9):
        for y in range(3):
            r[z].position=x
            z=z+1
            
    if request.method == 'POST':
        e.result=True
        for z in range(24):
            r[z].name=request.POST["name["+str(z)+"]"]
            if r[z].name != "":
                r[z].hostel=request.POST["sel["+str(z)+"]"]
                r[z].pts=int(request.POST["points["+str(z)+"]"])
                r[z].save()
                if r[z].hostel == "Alakananda":
                    hostel = Hostel.objects.get(hostel = "Alakananda")
                    hostel.total=hostel.total+r[z].pts
                    e.Alakananda =e.Alakananda+ r[z].pts
                if r[z].hostel == "Brahmaputra":
                    hostel = Hostel.objects.get(hostel = "Brahmaputra")
                    hostel.total=hostel.total+r[z].pts
                    e.Brahmaputra =e.Brahmaputra+ r[z].pts
                if r[z].hostel == "Cauvery":
                    hostel = Hostel.objects.get(hostel = "Cauvery")
                    hostel.total=hostel.total+r[z].pts
                    e.Cauvery = e.Cauvery+r[z].pts
                if r[z].hostel == "Ganga":
                    hostel = Hostel.objects.get(hostel = "Ganga")
                    hostel.total=hostel.total+r[z].pts
                    e.Ganga =e.Ganga+ r[z].pts
                if r[z].hostel == "Godavari":
                    hostel = Hostel.objects.get(hostel = "Godavari")
                    hostel.total=hostel.total+r[z].pts
                    e.Godavari =e.Godavari+ r[z].pts
                if r[z].hostel == "Jamuna":
                    hostel = Hostel.objects.get(hostel = "Jamuna")
                    hostel.total=hostel.total+r[z].pts
                    e.Jamuna =e.Jamuna+ r[z].pts
                if r[z].hostel == "Krishna":
                    hostel = Hostel.objects.get(hostel = "Krishna")
                    hostel.total=hostel.total+r[z].pts
                    e.Krishna =e.Krishna+ r[z].pts
                if r[z].hostel == "Mahanadhi":
                    hostel = Hostel.objects.get(hostel = "Mahanadhi")
                    hostel.total=hostel.total+r[z].pts
                    e.Mahanadhi =e.Mahanadhi+ r[z].pts
                if r[z].hostel == "Mandakini":
                    hostel = Hostel.objects.get(hostel = "Mandakini")
                    hostel.total=hostel.total+r[z].pts
                    e.Mandakini =e.Mandakini+ r[z].pts
                if r[z].hostel == "Narmada":
                    hostel = Hostel.objects.get(hostel = "Narmada")
                    hostel.total=hostel.total+r[z].pts
                    e.Narmada =e.Narmada+ r[z].pts
                if r[z].hostel == "Pampa":
                    hostel = Hostel.objects.get(hostel = "Pampa")
                    hostel.total=hostel.total+r[z].pts
                    e.Pampa =e.Pampa+ r[z].pts
                if r[z].hostel == "Saraswathi":
                    hostel = Hostel.objects.get(hostel = "Saraswathi")
                    hostel.total=hostel.total+r[z].pts
                    e.Saraswathi =e.Saraswathi+ r[z].pts
                if r[z].hostel == "Sarayu":
                    hostel = Hostel.objects.get(hostel = "Sarayu")
                    hostel.total=hostel.total+r[z].pts
                    e.Sarayu =e.Sarayu+ r[z].pts
                if r[z].hostel == "Sharavati":
                    hostel = Hostel.objects.get(hostel = "Sharavati")
                    hostel.total=hostel.total+r[z].pts
                    e.Sharavati =e.Sharavati+ r[z].pts
                if r[z].hostel == "Sindhu":
                    hostel = Hostel.objects.get(hostel = "Sindhu")
                    hostel.total=hostel.total+r[z].pts
                    e.Sindhu =e.Sindhu+ r[z].pts
                if r[z].hostel == "Tamiraparani":
                    hostel = Hostel.objects.get(hostel = "Tamiraparani")
                    hostel.total=hostel.total+r[z].pts
                    e.Tamiraparani =e.Tamiraparani+ r[z].pts
                if r[z].hostel == "Tapti":
                    hostel = Hostel.objects.get(hostel = "Tapti")
                    hostel.total=hostel.total+r[z].pts
                    e.Tapti =e.Tapti+ r[z].pts
            
        e.save()        
        return HttpResponseRedirect('/events/'+foobar+'/')  
                    
    return render_to_response("results.html",locals(),context_instance=RequestContext(request))	
	
	
def verticals(request,foobar):
    verticals = verticalDetails.objects.all()
    approve = 0
    flag = 0
    r = []
    name = ''
    v = verticalDetails.objects.get(vert_id=foobar)
    events = vertical_to_event.objects.filter(vert_id = foobar) 
    sids=vertical_to_scoord.objects.filter(vert_id=foobar)
    scoords=[]
    for sid in sids:
        up=UserProfile.objects.get(userid=sid.supercoord_id)
        scoords.append(up.user)
	        
    for event in events:
        e = EventDetails.objects.get(event_id = event.event_id)
        r.append(e)
    try:
        t = temp_eventdetails.objects.filter(vert_id = foobar)
    except:
        t  =  None
    if not request.user.is_authenticated():
        flag = 0
        return render_to_response("verticals.html",locals(),context_instance=RequestContext(request))
    else:
        usertype = request.user.get_profile().usertype
        if usertype == 'core':
            flag = 1
            if t is not None:
                approve = 1
            return render_to_response("verticals.html",locals(),context_instance=RequestContext(request))
        elif usertype == 'supercoord':
            sid = request.user.get_profile().userid
            u = vertical_to_scoord.objects.get(supercoord_id = sid)
            if  int(foobar) == u.vert_id:
                flag = 1
                if t is not None:
                    approve = 1
                return render_to_response("verticals.html",locals(),context_instance=RequestContext(request))
            else:
                flag = 0
                return render_to_response("verticals.html",locals(),context_instance=RequestContext(request))
        return render_to_response("verticals.html",locals(),context_instance=RequestContext(request))		
		
def editvertical(request,foobar):
    verticals=verticalDetails.objects.all()
    flag=0
    if not request.user.is_authenticated():
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    if request.user.is_authenticated() and request.user.get_profile().usertype=='coord':
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    if request.user.is_authenticated() and request.user.get_profile().usertype=='supercoord':
        scoords=vertical_to_scoord.objects.filter(vert_id=foobar)
        flag=2
        for scoord in scoords:
            if request.user.get_profile().userid == scoord.supercoord_id:
                flag=3
        
        if flag==2:    
            flag=1
            return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    r = []
    v = verticalDetails.objects.get(vert_id=foobar)
    events = vertical_to_event.objects.filter(vert_id = foobar) 
    for event in events:
        e = EventDetails.objects.get(event_id = event.event_id)
        r.append(e)
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        v.name = name
        v.description = description
        v.save()
        return HttpResponseRedirect('/corepage/')
		
    return render_to_response("editvertical.html",locals(),context_instance=RequestContext(request))	

def approve(request,foobar):
    verticals=verticalDetails.objects.all()
    flag=0
    if not request.user.is_authenticated():
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    if request.user.is_authenticated() and request.user.get_profile().usertype=='coord':
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    
    if request.user.is_authenticated() and request.user.get_profile().usertype=='supercoord':
        v=vertical_to_event.objects.get(event_id=foobar)
        scoords=vertical_to_scoord.objects.filter(vert_id=v.vert_id)
        flag=2
        for scoord in scoords:
            if request.user.get_profile().userid == scoord.supercoord_id:
                flag=3
        
        if flag==2:    
            flag=1
            return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
	
    t = temp_eventdetails.objects.get(event_id = foobar)
    if request.method == "POST":
        e=EventDetails.objects.get(event_id=foobar)
        e.venue=request.POST['venue']
        e.name=request.POST['name']
        e.date= request.POST['date']
        e.description=request.POST['description']
        e.t5e = request.POST['t5e']
        e.save()
        t.delete()
        return HttpResponseRedirect('/corepage/')
    else:
        return render_to_response("approve.html",locals(),context_instance=RequestContext(request))
    return render_to_response("approve.html",locals(),context_instance=RequestContext(request))						

def gallery(request):
    verticals = verticalDetails.objects.all()
    files = []
    os.system("./manage.py collectstatic") 
    n = len(os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gallery').replace('\\','/')))
    for name in os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gallery').replace('\\','/')):
    	if os.path.isfile(os.path.join(os.path.dirname(__file__),'..','downloads','gallery',name).replace('\\','/'),):
    		files.append(name)
    		
    return render_to_response("gallery.html",locals(),context_instance=RequestContext(request))

def upload(request,foobar):
    if not request.user.is_authenticated():
        flag=1
        return render_to_response("notauthorized.html",locals(),context_instance=RequestContext(request))
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():	
            f = form.cleaned_data['files']
            f = request.FILES['files']	
            title = request.POST['title_with_extension']
            if foobar == "img":
                n = len(os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gallery').replace('\\','/')))
                x = str(n+1)
                os.system("./manage.py collectstatic ") 
                dest = open(os.path.join(os.path.dirname(__file__),'..','downloads','gallery').replace('\\','/'+'/')+'/'+title,'wb+')
                #return HttpResponse(dest.name)
            elif foobar == "gen":
                n = len(os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gen').replace('\\','/')))
                x = str(n+1)
                os.system("./manage.py collectstatic ") 
                dest = open(os.path.join(os.path.dirname(__file__),'..','downloads','gen').replace('\\','/'+'/')+'/'+title,'wb+')
	
            for chunk in request.FILES['files'].chunks():
                dest.write(chunk)
                os.system("./manage.py collectstatic ") 
            dest.close()
            f.close()
            os.system("./manage.py collectstatic ") 
            return HttpResponseRedirect('/corepage/')	
    else:
        form = UploadFileForm()
    return render_to_response('upload.html',{'form': form},context_instance=RequestContext(request))

def downloads(request):
    verticals = verticalDetails.objects.all()
    files = []
    n = len(os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gen').replace('\\','/')))
    for name in os.listdir(os.path.join(os.path.dirname(__file__),'..','downloads','gen').replace('\\','/')):
        files.append(name)
    os.system("./manage.py collectstatic")  
    return render_to_response("downloads.html",locals(),context_instance=RequestContext(request))
	
def pointstally(request):
    verticals=verticalDetails.objects.all()
    hostels=Hostel.objects.all()
    events = EventDetails.objects.all()
    return render_to_response("pointstally.html",locals(),context_instance=RequestContext(request))	
    	
def hostel(request,foobar):
	i = 0 
	events= []
	pts = []
	verticals=verticalDetails.objects.all()
	try:
		hostel = Hostel.objects.get(hostel = foobar)
	except Hostel.DoesNotExist:
		hostel = None
		return HttpResponse("Page Does not Exist - 404")
	up1=UserProfile.objects.get(userid=hostel.litsec_id)
	litsec=up1.user
	
	if foobar == 'Alakananda':
		events = EventDetails.objects.filter(Alakananda__gt =  0)
		for e in events:
			pts.append(e.Alakananda)
	if foobar == 'Brahmaputra':
		events = EventDetails.objects.filter(Brahmaputra__gt = 0)
		for e in events:
			pts.append(e.Brahmaputra)
	if foobar == "Cauvery":
		events = EventDetails.objects.filter(Cauvery__gt = 0)
		for e in events:
			pts.append(e.Cauvery)
	if foobar == "Ganga":
		events = EventDetails.objects.filter(Ganga__gt = 0)
		for e in events:
			pts.append(e.Ganga)
	if foobar == "Godavari":
		events = EventDetails.objects.filter(Godavari__gt = 0)
		for e in events:
			pts.append(e.Godavari)
	if foobar == "Jamuna":
		events = EventDetails.objects.filter(Jamuna__gt = 0)
		for e in events:
			pts.append(e.Jamuna)
	if foobar == "Krishna":
		events = EventDetails.objects.filter(Krishna__gt = 0)
		for e in events:
			pts.append(e.Krishna)
	if foobar == "Mahanadhi":
		events = EventDetails.objects.filter(Mahanadhi__gt = 0)
		for e in events:
			pts.append(e.Mahanadhi)
	if foobar == "Mandakini":
		events = EventDetails.objects.filter(Mandakini__gt = 0)
		for e in events:
			pts.append(e.Mandakini)
	if foobar == "Narmada":
		events = EventDetails.objects.filter(Narmada__gt = 0)
		for e in events:
			pts.append(e.Narmada)
	if foobar == "Pampa":
		events = EventDetails.objects.filter(Pampa__gt = 0)
		for e in events:
			pts.append(e.Pampa)
	if foobar == "Saraswathi":
		events = EventDetails.objects.filter(Saraswathi__gt = 0)
		for e in events:
			pts.append(e.Saraswathi)
	if foobar == "Sarayu":
		events = EventDetails.objects.filter(Sarayu__gt = 0)
		for e in events:
			pts.append(e.Sarayu)
	if foobar == "Sharavati":
		events = EventDetails.objects.filter(Sharavati__gt = 0)
		for e in events:
			pts.append(e.Sharavati)
	if foobar == "Sindhu":
		events = EventDetails.objects.filter(Sindhu__gt = 0)
		for e in events:
			pts.append(e.Sindhu)
	if foobar == "Tamiraparani":
		events = EventDetails.objects.filter(Tamiraparani__gt = 0)
		for e in events:
			pts.append(e.Tamiraparani)
	if foobar == "Tapti":
		events = EventDetails.objects.filter(Tapti__gt = 0)
		for e in events:
			pts.append(e.Tapti)
	 
	try:
		results = Results.objects.filter(hostel = foobar)
	except Result.DoesNotExist:
		results = None
		return HttpResponse("Page Does not Exist - 404")

	return render_to_response("hostelPage.html",locals(),context_instance=RequestContext(request))

def hostels(request):
	verticals = verticalDetails.objects.all()
	hostels = Hostel.objects.all()
	return render_to_response("hostels.html",locals(),context_instance=RequestContext(request))
