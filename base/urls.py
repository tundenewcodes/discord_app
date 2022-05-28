from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name ='home'),
    
    path('room/<str:pk>', views.room, name ='room'),
    path('topics-page/', views.topicsPage, name ='topics-page'),
    
    path('create_room/', views.create_room, name ='create_room'),
    path('update_room/<str:pk>', views.update_room, name ='update_room'),
    path('delete_room/<str:pk>', views.delete_room, name ='delete_room'),
    path('delete-message/<str:pk>', views.delete_message, name ='delete-message'),
    
    path('update-user/', views.updateUser, name ='update-user'),
    path('activity/', views.activityPage, name ='activity'),
    
    
    
    
    path('profile/<str:pk>', views.profile, name ='profile'),
    
    
    path('login/', views.login_page, name ='login'),
    path('logout/', views.logout_user, name ='logout'),
    path('register/', views.registerPage, name ='register'),
]
