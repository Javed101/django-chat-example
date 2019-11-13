from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('chat', views.index, name='index'),
    path('login', views.login_view, name='login-view'),
    path('logout', views.logout_view, name='logout-view'),
    path('chat/<str:room_name>/', views.room, name='chat-room-view'),
]
