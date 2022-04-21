from django.urls import path

from chat import views, api


app_name = "chat"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("accouts/login/", views.login_staff, name="login"),
    path("accouts/logout/", views.logout_staff, name="logout"),
    path("accouts/registration/", views.registration_staff, name="registration"),
    path("accouts/edit/<int:pk>/", views.change_staff, name="edit"),
    path("api/v1/note/", api.get_note, name="note"),
    path("api/v1/new_chat/<int:ucid>", api.get_chat, name="chat"),
    path("api/v1/chats/", api.get_chats, name="chats"),
    path("api/v1/messages/<int:ucid>/<str:offset>/",
         api.get_messages, name="messages"),
    path("api/v1/emoji/", api.get_emojis, name="emoji"),
    path("api/v1/upload_file/", api.upload_file, name="upload_file"),
]