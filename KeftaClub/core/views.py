from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from itertools import chain
from operator import attrgetter
import random
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy
from datetime import datetime, timedelta
import networkx as nx
#Recommandation algorithms
from .Algorithm.recommendation import friends_recommandation_algorithm as fra
from .Algorithm.recommendation import posts_recommandation_algorithm as pra


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    #####################################
    #### SECTION DE TEST DE L'ALGO ######
    #####################################

    # Tout les profils
    profiles = list(Profile.objects.all())
    all_profiles = [profile.user.username for profile in profiles]

    # Tout les posts
    posts = list(Post.objects.all())
    all_posts = [str(post.id) for post in posts]

    # Les likes par posts
    posts_likes_dict = {post : LikePost.objects.filter(post_id=post).count() for post in all_posts}

    # Les posts par date de création
    posts_creation_date_dict = [(str(post.id), (post.created_at).strftime("%Y-%m-%d %H:%M:%S")) for post in Post.objects.all()]

    # Les relations entre les utilisateurs
    follow_relationships = [(follow.follower, follow.user) for follow in FollowersCount.objects.all()]

    # Les profils et leurs catégories préférée
    u_fav = [[(profile.user.username, profile.favoriteSpicyness),(profile.user.username, profile.favoriteOrigin), (profile.user.username, profile.favoriteCooking)] for profile in Profile.objects.all()]
    users_favorites = list(chain(*u_fav))
    # Les utilisateurs et leurs posts
    users_posts = [(post.user, str(post.id)) for post in Post.objects.all()]

    
    #Trier les likes des 7 derniers jours seulements
    seven_days_ago = datetime.now() - timedelta(days=7)
    users_liked_posts = [(like.username, like.post_id) for like in LikePost.objects.filter(created_on__gte=seven_days_ago)]

    # Récupération des posts et de leurs 3 catégories
    p_cat = [[(str(post.id), post.Spicyness),(str(post.id), post.Origin),(str(post.id), post.Cooking)] for post in Post.objects.all()]
    posts_categories = list(chain(*p_cat))

    #Modalités en mode bruts
    modalities = [
        "Failed Experiment", "Leftovers", "Expired food", "not sure",
        "raw", "raw (probably still alive)", "burnt", "insanely burnt", "calcinated", "Probably radioactive",
        "0", "1", "2", "3", "unspecified"
    ]


    #Relationship Graph
    rj_graph = nx.Graph()
    rj_graph.add_nodes_from(all_profiles)
    rj_graph.add_edges_from(follow_relationships)

    #Interest Graph
    i_graph = nx.Graph()
    i_graph.add_nodes_from(all_profiles)
    i_graph.add_edges_from(users_favorites)

    #User Post Graph
    up_graph = nx.Graph()
    up_graph.add_nodes_from(all_profiles)
    up_graph.add_edges_from(users_posts)

    #User Like Post Graph
    lp_graph = nx.Graph()
    lp_graph.add_nodes_from(all_profiles)
    lp_graph.add_edges_from(users_liked_posts)

    #Post category Graph
    pc_graph = nx.Graph()
    pc_graph.add_nodes_from(modalities)
    pc_graph.add_edges_from(posts_categories)



    #### EXECUTION DES ALGORITHMS DE RECOMMANDATION ###

    
    friends_recommendation, nb_friend_map, nb_interest_map = fra(rj_graph, i_graph, user_profile.user.username)

    posts_recommendation = pra(rj_graph, i_graph, up_graph, lp_graph, pc_graph, posts_likes_dict,
                                posts_creation_date_dict, user_profile.user.username)
    


    #####################################
    ############### FIN #################
    #####################################


    user_following_list = []
    followers_list = []
    feed = []


    user_following = FollowersCount.objects.filter(follower=request.user.username)
    followers = FollowersCount.objects.filter(user=request.user.username)

    # If no followers exist, set followers_list to empty
    if not followers.exists():
        followers_list = []
    else:
        for follower in followers:
            user_follower = User.objects.get(username=follower.follower)
            profile_follower = Profile.objects.get(user=user_follower.id)
            profile_follower.notification_type = 'follower'
            profile_follower.date = follower.date
            followers_list.append({
                'username': user_follower.username,
                'profile_pic': profile_follower.profileimg,
                'notification_type': 'follower',
                'date': follower.date
            })

    #This part list all the users you are following
    for users in user_following:
        user_following_list.append(users.user)

    for post in posts_recommendation:
        feed_lists = Post.objects.filter(id=post)
        #profilepicture = Profile.objects.get(user=User.objects.get(username=follower.follower).id)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))[::-1]

    new_feed = []

    for  post in feed_list:
        username = User.objects.get(username=post.user)
        profile_pic = Profile.objects.get(user=username.id)
        liked_post = LikePost.objects.filter(post_id=post.id)
        is_liked = False
        for zibba in liked_post:
            if zibba.username == user_object.username:
                is_liked = True
        new_feed.append({
            'post' : post,
            'profile' : profile_pic.profileimg.url,
            'is_liked' : is_liked

        })
    
    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []
    final_suggestions_list = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    # Assuming friends_recommendation and posts_recommendation are obtained earlier in the view
    for recommended_user in friends_recommendation:
        user_list = User.objects.get(username=recommended_user)
        final_suggestions_list.append(user_list)

    ## MERGE DU CODE PRECEDENT AU NOUVEL ALGO DE RECOMMANDATION
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all) and x not in list(final_suggestions_list))]
    current_user = User.objects.filter(username=request.user.username)
    suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(suggestions_list) # ---------- ligne a changer ----------

    final_suggestions_list.extend(suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    context = {
        'user_profile': user_profile,
        'posts': new_feed,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
        'followers': followers_list[:4]
    }

    return render(request, 'index.html', context) 

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        origin = request.POST['meat']
        cooking = request.POST['cooking']
        spicyness = request.POST['region']
        location = request.POST['location']

        #Check if a location was entered
        if not location.replace(" ", ""):
            location = "unknown"

        new_post = Post.objects.create(user=user, image=image, caption=caption, 
                                       Spicyness=spicyness, Cooking=cooking, Origin=origin, location=location)
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
    originSelect = {"Failed Experiment" : "Failed Experiment" 
                        , "Leftovers" : "Leftovers"
                        , "Expired food" : "Expired food"
                        , "Wicked Intention": "Wicked Intention"}

    cookingSelect = {"raw" : "raw"
                         , "raw (probably still alive)" : "raw (probably alive)"
                         , "burnt" : "burnt"
                         , "insanely burnt": "insanely burnt"
                         , "calcinated" : "calcinated"}

    spicynessSelect = {"0" : "0"
                           , "1" : "1"
                           , "2" : "2"
                           , "3": "MY MOUTH!!!"} 

    if request.method == 'POST':

        
    
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            favoriteOrigin = request.POST['favoriteMeat']
            favoriteCooking = request.POST['favoriteCooking']
            favoriteSpicyness  = request.POST['favoriteRegion']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.favoriteSpicyness = favoriteSpicyness   
            user_profile.favoriteCooking = favoriteCooking
            user_profile.favoriteOrigin = favoriteOrigin 

            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        print(originSelect)
        return redirect('settings')
    return render(request, 'setting.html', context = {'user_profile': user_profile, 'originSelect' : originSelect, 'cookingSelect':cookingSelect,'spicynessSelect': spicynessSelect})

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

#Fonction pour les messages privé
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        # Récupérez toutes les conversations avec des messages associés
        threads_with_messages = ThreadModel.objects.filter().distinct()

        # Filtrer les conversations pour lesquelles l'utilisateur est soit le créateur soit le destinataire
        all_threads = threads_with_messages.filter(Q(user=request.user) | Q(receiver=request.user))

        # Récupérez tous les messages associés à ces conversations
        messages = {}
        no_null_thread = []
        for thread in all_threads:
            # Vérifiez si le thread a au moins un message associé
            if MessageModel.objects.filter(thread=thread).exists():
                messages[thread.pk] = MessageModel.objects.filter(thread=thread)
                no_null_thread.append(thread)

        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
       # Récupérez les identifiants des salles de discussion dans lesquelles l'utilisateur a envoyé des messages
        room_ids_with_user_messages = Message.objects.filter(user=request.user).values_list('room', flat=True)

        # Récupérez les salles de discussion correspondantes
        rooms = Room.objects.filter(id__in=room_ids_with_user_messages)


        followers_list = []


        followers = FollowersCount.objects.filter(user=request.user.username)

        for follower in followers:
            user_follower = User.objects.get(username=follower.follower)
            followers_list.append(Profile.objects.get(user=user_follower))
    
        person_who_like_user_post = []
        user_post = Post.objects.filter(user=user_object)

        for post in user_post:
            like_user_posts = LikePost.objects.filter(post_id=post.id)
            for like in like_user_posts:
                liker_username = like.username
                liker_user = User.objects.get(username=liker_username)
                liker_profile = Profile.objects.get(id_user=liker_user.id)
                person_who_like_user_post.append({'username': liker_user.username,'profile_pic': liker_profile.profileimg})
        context = {
            'threads': no_null_thread,
            'messages': messages,  # Passer les messages au template
            'user_profile': user_profile,
            "followers": followers_list[:4], 
            "rooms":rooms,
            "person_who_liked_post": person_who_like_user_post
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
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    room = get_object_or_404(Room, name=room_name)
    
    # Fetch all messages related to the room and include user profile pictures
    messages = Message.objects.filter(room=room.id).order_by('date')
    message_list = []
    for message in messages:
        message_user = User.objects.get(username=message.user)
        message_profile = Profile.objects.get(user=message_user)
        message_list.append({
            'user': message.user,
            'value': message.value,
            'date': message.date,
            'profile': message_profile.profileimg.url,
        })

    return render(request, 'room.html', {
        'username': username,
        'profile': user_profile.profileimg.url,
        'room': room,
        'messages': message_list,
    })

def checkview(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        username = request.user.username

        room, created = Room.objects.get_or_create(name=room_name)

        return redirect(f'/{room.name}/?username={username}')
    return render(request, 'create_room.html')

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)

    new_message = Message.objects.create(value=message, user=username, room=room_id, profile=user_profile.profileimg.url)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')

def getMessages(request, room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room.id).order_by('date')
    message_list = []

    for message in messages:
        user = User.objects.get(username=message.user)
        user_profile = Profile.objects.get(user=user)
        message_list.append({
            'user': message.user,
            'value': message.value,
            'date': message.date,
            'profile': user_profile.profileimg.url,  # Inclure l'URL de la photo de profil
        })

    return JsonResponse({"messages": message_list})