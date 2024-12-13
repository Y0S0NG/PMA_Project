from django.urls import path
from . import views

urlpatterns = [
    path('messages_list/<int:course_id>/', views.show_messages, name='list-messages'),
    path('messages/<int:course_id>/post/', views.post_message, name='post-message'),
    path('messages/<int:course_id>/<int:message_id>/reply', views.post_reply, name='post-reply'),
    path('messages_detail/<int:message_id>/', views.message_detail, name='message-detail'),
]
