from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class UserList(ListView):
    model = User

class UserDetail (DetailView):
    model = User