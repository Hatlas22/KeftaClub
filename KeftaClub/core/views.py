from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from itertools import chain
import random
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=user_object)
    user_receive_msg = MessageModel.objects.filter(receiver_user_id=request.user.id).order_by("-date")
    
    person_who_like_user_post = []
    for post in user_post:
        like_user_posts = LikePost.objects.filter(post_id=post.id)
        for like in like_user_posts:
            liker_username = like.username
            liker_user = User.objects.get(username=liker_username)
            liker_profile = Profile.objects.get(id_user=liker_user.id)
            person_who_like_user_post.append({'username': liker_user.username,'profile_pic': liker_profile.profileimg}) # Assuming 'profileimg' is the field name for the profile picture

    user_sender = []
    user_following_list = []
    followers_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    followers = FollowersCount.objects.filter(user=request.user.username)

    # Si aucun follower n'existe, définissez la liste des followers sur None
    if not followers.exists():
        followers = []

    #This part list all the users you are following
    for users in user_following:
        user_following_list.append(users.user)

    for sender in user_receive_msg :
        author_msg = User.objects.get(id=sender.sender_user_id)
        user_sender.append({"sender_name":author_msg.username,"message_date":sender.date,"thread":sender.thread_id})
    for follower in followers :

        user_follower = User.objects.get(username = follower.follower)
        followers_list.append(Profile.objects.get(user=user_follower))

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    #The user feed is then contained here
    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list) # ---------- ligne a changer ----------

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4], "followers":followers_list[:4], "person_who_liked_post":person_who_like_user_post,"message_receive":user_sender[:5]})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        meat = request.POST['meat']
        cooking = request.POST['cooking']
        region = request.POST['region']
        location = request.POST['location']

        #Check if a location was entered
        if not location.replace(" ", ""):
            location = "unknown"

        new_post = Post.objects.create(user=user, image=image, caption=caption, 
                                       Meat=meat, Cooking=cooking, Region=region, location=location)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
    
@login_required(login_url='signin')
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user.username == post.user:
            post.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            favoriteMeat = request.POST['favoriteMeat']
            favoriteCooking = request.POST['favoriteCooking']
            favoriteRegion  = request.POST['favoriteRegion']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.favoriteMeat = favoriteMeat   
            user_profile.favoriteCooking = favoriteCooking
            user_profile.favoriteRegion = favoriteRegion 

            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        birthdate = request.POST['birthdate']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, birthDate = birthdate)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_object = User.objects.get(username=request.user.username)
    comments = post.comments.all()
    new_comment = None 
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.username = request.user.username
            new_comment.save()
            return JsonResponse({
                'success': True,
                'comment_id': new_comment.pk,
                'username': new_comment.username,
                'body': new_comment.body,
                'created_on': new_comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

    # Pour une requête GET ou toute autre requête non-AJAX POST
    comment_form = CommentForm()
    return render(request, 'post_detail.html', {
        'post': post,
        'user_profile': user_profile,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

@login_required
@require_POST
def edit_comment_api(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.username != comment.username:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'body': comment.body})
    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)
@login_required
@require_POST
def delete_comment_api(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.username != comment.username:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    comment.delete()
    return JsonResponse({'success': True})

#Fonction pour leq messages privé
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        followers_list = []

        followers = FollowersCount.objects.filter(user=request.user.username)

        for follower in followers :

            user_follower = User.objects.get(username = follower.follower)
            followers_list.append(Profile.objects.get(user=user_follower))
    
        person_who_like_user_post = []
        user_post = Post.objects.filter(user=user_object)

        for post in user_post:
            like_user_posts = LikePost.objects.filter(post_id=post.id)
            for like in like_user_posts:
                liker_username = like.username
                liker_user = User.objects.get(username=liker_username)
                liker_profile = Profile.objects.get(id_user=liker_user.id)
                person_who_like_user_post.append({'username': liker_user.username,'profile_pic': liker_profile.profileimg}) # Assuming 'profileimg' is the field name for the profile picture



        context = {
            'threads': threads,
            'user_profile': user_profile,
            "followers":followers_list[:4], 
            "person_who_liked_post":person_who_like_user_post
            }

        return render(request, 'inbox.html', context)
    


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        
        return redirect('thread', pk=pk)
    
@login_required(login_url='signin')
def create_thread_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username == request.user.username:
            return JsonResponse({'success': False, 'error': 'You cannot create a thread with yourself.'})

        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User with this username does not exist.'})

        thread = (ThreadModel.objects.filter(user=request.user, receiver=receiver) |
                  ThreadModel.objects.filter(user=receiver, receiver=request.user)).first()

        if thread:
            return JsonResponse({'success': True, 'thread_id': thread.pk})

        thread = ThreadModel(user=request.user, receiver=receiver)
        thread.save()
        return JsonResponse({'success': True, 'thread_id': thread.pk})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

#Fonction pour le chat room
def room(request, room_name):
    username = request.user.username
    room = get_object_or_404(Room, name=room_name)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
    })

def checkview(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        username = request.user.username

        user = User.objects.get(username=username)
        
        room, created = Room.objects.get_or_create(name=room_name)

        return redirect(f'/{room.name}/?username={username}')
    return render(request, 'create_room.html')

    

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value= message , user = username , room = room_id)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')


def getMessages(request, room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room.id).order_by('date')
    print(messages[0].value)  # Ajoutez ceci pour voir les messages dans la console du serveur
    return JsonResponse({"messages": list(messages.values())})