from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('post/<str:pk>', views.post_detail, name='post_detail'),
    path('post/<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:pk>/edit/', views.edit_comment_api, name='edit_comment_api'),
    path('comment/<int:pk>/delete/', views.delete_comment_api, name='delete_comment_api'),
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', views.create_thread_ajax, name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', views.CreateMessage.as_view(), name='create-message'),
    path('<str:room_name>/', views.room , name ="room"),
    path('send', views.send , name ="send"),
    path('checkview', views.checkview , name ="checkview"),
    path('getMessages/<str:room_name>/', views.getMessages , name ="getMessages"),

]