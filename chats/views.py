from django.shortcuts import render,redirect
# Create your views here.
from django.urls import path
from django.contrib import admin,messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic,Message
from .forms import roomform,messageEdit
from accounts.models import blogchatUser
from django.contrib.auth.decorators import login_required

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains = q) |
        Q(desc__icontains = q)
        )
    room_count = rooms.count
    topics = Topic.objects.all()
    room_message = Message.objects.filter(
        Q(room__name__icontains = q) |
        Q(room__topic__name__icontains = q)
    )

    context ={'rooms':rooms,'topic':topics,'room_count':room_count,'room_message':room_message}
    return render(request,'chat_home.html',context)

# for user profile
def profile(request,pk):
    user = blogchatUser.objects.get(id=pk)
    rooms=user.room_set.all()
    topics = Topic.objects.all()
    room_message = user.message_set.all()
    context={'user':user,'rooms':rooms,'topic':topics,'room_message':room_message}
    return render(request,'profile/profile.html',context)

# for indivisual room
def room(request,pk):
    rooms = Room.objects.get(id=pk)
    # _set.all gives all the messages relate to this room
    comments= rooms.message_set.all().order_by('-created')

    # getting participants
    participants = rooms.participants.all()

    # adding comments in the room form
    if request.method == 'POST':
        newcomment = Message.objects.create(
            user = request.user,
            room = rooms,
            body = request.POST.get('body')
        )
        rooms.participants.add(request.user)
        rooms.save()
        return redirect('room',pk=rooms.id)

    context = {'rooms' : rooms, 'comments':comments,'participants':participants}
    return render(request,'base/room.html',context)

# Deleting the message
@login_required(login_url='/login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.method == "POST":
        message.delete()
        return redirect('room',pk=message.room.id)
    return render(request,'base/delete.html',{'obj':message})

# editing the message
@login_required(login_url='/login')
def editMessage(request,pk):
    message = Message.objects.get(id=pk)
    form = messageEdit(instance=message)

    if (request.method =='POST'):
        form = messageEdit(request.POST,instance=message)
        if form.is_valid():
            form.save()
            return redirect('room',pk=message.room.id)

    context = {'form':form,'message':message}
    return render(request,'base/message_edit.html',context)

# Creating the room
@login_required(login_url='/login')
def create_room(request):
    form = roomform()
    topics = Topic.objects.all()
    if request.method =='POST':
        form = roomform(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            room.participants.add(request.user)
            return redirect('home')

    context = {'form':form,'topics':topics}
    return render(request,'base/room_create.html',context)

# updating the room
@login_required(login_url='/login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = roomform(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')

    if (request.method =='POST'):
        form = roomform(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form,'room':room,'topics':topics}
    return render(request,'base/room_edit.html',context)

# delting the room
@login_required(login_url='/login')
def delete(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',context={'obj':room})
