from itertools import chain
from django.contrib.auth.models import User

def nav_bar(request):
    from core.models import Profile, Post, MessageModel, LikePost, FollowersCount
    # Vérifier si l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return {}

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=user_object)
    user_receive_msg = MessageModel.objects.filter(receiver_user_id=request.user.id).order_by("-date")
    
    person_who_like_user_post = []
    for post in user_post:
        like_user_posts = LikePost.objects.filter(post_id=post.id)
        for like in like_user_posts:
            liker_user = User.objects.get(username=like.username)
            liker_profile = Profile.objects.get(user=liker_user.id)
            person_who_like_user_post.append({
                'username': like.username,
                'profile_pic': liker_profile.profileimg,
                'notification_type': 'like',
                'date': like.created_on
            })

    user_sender = []
    user_following_list = []
    followers_list = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    followers = FollowersCount.objects.filter(user=request.user.username)

    if followers.exists():
        for follower in followers:
            user_follower = User.objects.get(username=follower.follower)
            profile_follower = Profile.objects.get(user=user_follower.id)
            followers_list.append({
                'username': user_follower.username,
                'profile_pic': profile_follower.profileimg,
                'notification_type': 'follower',
                'date': follower.date
            })

    for users in user_following:
        user_following_list.append(users.user)

    for sender in user_receive_msg:
        author_msg = User.objects.get(id=sender.sender_user_id)
        author_profile = Profile.objects.get(user=author_msg.id)
        user_sender.append({
            "sender_name": author_msg.username,
            "message_date": sender.date,
            "thread": sender.thread_id,
            "body": sender.body,
            "profile": author_profile.profileimg.url
        })

    user_following_all = [User.objects.get(username=user.user) for user in user_following]

    notifications = sorted(
        list(chain(followers_list, person_who_like_user_post)),
        key=lambda x: x["date"],
        reverse=True
    )

    return {
        'user_profile': user_profile,
        'followers': followers_list[:4],
        'person_who_liked_post': person_who_like_user_post,
        'message_receive': user_sender[:5],
        'notifications': notifications
    }