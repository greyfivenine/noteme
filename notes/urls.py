from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', user_signup, name='signup'),
    path('signin/', user_login, name='signin'),
    path('logout/', user_logout, name='logout'),
    path('add_note/<int:group_id>', add_note, name='add_note'),
    path('change_note/<int:note_id>', change_note, name='change_note'),
    path('delete/', delete_note, name='delete_note'),
]
