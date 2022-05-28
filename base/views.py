from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models  import Room,Topic, Message, User
from .form import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login, logout
# Create your views here.

def login_page(request):
    page = 'login'
    #if the user is already authenticated i want to redirect them back to home
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()  #get username and password from name attribute in html
        password = request.POST.get('password')
        try: 
            user = User.objects.get(username=username) #check if the user exists
        except Exception:
              messages.error(request, 'user does not exist') # if user doesn't exist show this message 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')
    context = {'page' : page}
    return render(request, 'base/login_page.html', context)

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #suspend saving it we want to check and edit user before saving hence commit = false
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occured during registration')
    context = {'page' : page, 'form' : form}
    return render(request, 'base/login_page.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics =  Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics' : topics})


def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''    #A. Get q from url if q exist else q = '' get a q value from the url
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        )  #filter room by topic names that contains one or 2 values of q  - whatever values contains in topic name is contained in room
    count_room = rooms.count()
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q)) # filter ny room messages (activity threads). room is in message (one to many from Room) that has topic and topic has name name 
    context = {'rooms' : rooms, 'topics' : topics, 'count_room' : count_room, 'room_messages' : room_messages}
    return render(request, 'base/home.html', context)  # when this function is called take the user to home.html

def  profile(request, pk):
    user  = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {'user' : user, 'rooms' : rooms, 'room_messages' : room_messages, 'topics' : topics}
    return render(request, 'base/profile.html', context)


def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()  #.order_by('-created') can also be controlled globally in the model
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user) #to add to list of  participants in the room. you can also do remove to remove
        return redirect('room', pk=room.id)
    context = {'room' : room, 'room_messages' : room_messages, 'participants' : participants}        
    return render(request, 'base/room.html', context) # when this function is called take the user to room.html


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #this method will get topic_name if exisitng or create one if not exiting
        # form = RoomForm(request.POST)  #room form having the data of that request.post( which is the value i just entered)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        Room.objects.create(
            host = request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
           
        )
        return redirect('home')
        
    context = {'form' : form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def  update_room(request, pk):
    
    room  = Room.objects.get(id=pk)  #get a particular room
    form = RoomForm(instance=room)  # let a form be for a specific room id - form for a particular id
    topics = Topic.objects.all()
    if request.user != room.host: 
        return HttpResponse('sign in if you\'re the real user')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #this method will get topic_name if exisitng or create one if not exiting
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form' : form, 'topics' : topics, 'room' : room}
    return render(request,'base/room_form.html', context )


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host: 
        return HttpResponse('sign in if you\'re the real user')
    if request.method =='POST':
        room.delete()
        
    return render(request, 'base/delete.html', {'obj':room})   
 
@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user: 
        return HttpResponse('sign in if you\'re the real user of this account')
    if request.method =='POST':
        message.delete()
        
    return render(request, 'base/delete.html', {'obj':message}) 


@login_required(login_url='login')  
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
       form = UserForm(request.POST, request.FILES, instance=user)
       if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)        
    context  ={'form' : form}
    return render(request, 'base/update-user.html', context)



def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages' : room_messages})