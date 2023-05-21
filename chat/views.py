from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from profileapp.models import *
from .models import Message
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages


def get_news(request):
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=e92090481bc24996a2a89b1f90299cdf'
    response = requests.get(url)
    articles = response.json()['articles']
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
    return render(request, 'chat/news.html', {
                    "page": "Newsplatform",
                    "suggestions": suggestions,
                    "articles" : articles,
                    "posts": posts
                })

@login_required(login_url='login')
def chat_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    chatter = User.objects.get(id=recipient_id)
    u_id = chatter.id
    fname_value = chatter.first_name
    lname_value = chatter.last_name
    pic = chatter.profile_pic

    messages = Message.objects.filter(Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)).order_by('timestamp')

    current_user = request.user
    received_messages = Message.objects.filter(recipient=current_user).values('sender').annotate(
        latest_timestamp=Max('timestamp'))
    sent_messages = Message.objects.filter(sender=current_user).values('recipient').annotate(
        latest_timestamp=Max('timestamp'))


    conversations = []

    # sort the received_messages list in reverse order based on latest timestamp
    received_messages = sorted(received_messages, key=lambda x: x['latest_timestamp'], reverse=True)
    sent_messages = sorted(sent_messages, key=lambda x: x['latest_timestamp'], reverse=True)


    for message in received_messages:
        latest_message = Message.objects.filter(recipient=current_user, sender=message['sender'],
                                                timestamp=message['latest_timestamp']).first()
        conversation = {
            'sender': latest_message.sender,
            'message': latest_message.message,
            'timestamp': latest_message.timestamp
        }
        conversations.append(conversation)     

    for message in sent_messages:
        latest_message = Message.objects.filter(sender=current_user, recipient=message['recipient'],
                                                timestamp=message['latest_timestamp']).first()

        conversation = {
            'sender': latest_message.recipient,
            'message': latest_message.message,
            'timestamp': latest_message.timestamp
        }
        conversations.append(conversation)
   
    sorted_list = sorted(conversations, key=lambda x: x['timestamp'], reverse=True)

    new_list = []
    existing_names = set()
    for dictionary in sorted_list:
        name = dictionary['sender']
        if name not in existing_names:
            new_list.append(dictionary)
            existing_names.add(name)

    # new_list = [dict(t) for t in set([tuple(d.items()) for d in sorted_list])]

    # new_list = [dict(t) for t in set([tuple(d.items()) for d in sorted_list])]

    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]

    context = {
        "recipient": recipient,
        'u_id':u_id,
        'messages': messages,
        'conversations': new_list,
        'fname_value' : fname_value,
        'lname_value' : lname_value,
        'pic': pic,
        "page": "Chat",
        "suggestions": suggestions, 
    }
    
    return render(request, 'chat/chat.html', context)

@login_required(login_url='login')
def send_message_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Message.objects.create(sender=request.user, recipient=recipient, message=message)
            return redirect('chat', recipient_id=recipient_id)
    context = {'recipient': recipient}
    return render(request, 'chat/send_message.html', context)


@login_required(login_url='login')
def search(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    chatter = User.objects.get(id=recipient_id)
    u_id = chatter.id
    fname_value = chatter.first_name
    lname_value = chatter.last_name
    pic = chatter.profile_pic

    messages = Message.objects.filter(Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)).order_by('timestamp')

    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
    suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
            J=User.objects.filter(multiple_q).exclude(username=request.user.username).exclude(username="george")
            return render(request, 'profileapp/search.html', {'key1':J, "posts": posts, "recipient": recipient,'u_id':u_id,'fname_value' : fname_value,
        'lname_value' : lname_value,'pic': pic,'messages': messages, "page": "Search", "suggestions":suggestions})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    return render(request, 'profileapp/search.html',{"page": "Search", "recipient": recipient,'u_id':u_id,'fname_value' : fname_value,
        'lname_value' : lname_value,'pic': pic,'messages': messages, "posts": posts, "suggestions":suggestions})