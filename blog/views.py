from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied





# Create your views here.
class PostList(ListView):
    model = Post

#This Class Based View is a detail view that displays all the information about an object that it was given.
class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#This Class Based View is to create a new post, it has a title and text field, and saves the user as well as the date that it was published. 
#It has a check to make sure the user is logged in, and if they are not then it will redirect them. to the login page.
class PostNew(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post
    fields = ['title', 'text']
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.published_date = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())



#This Class Based View is an edit post view along with a check to make sure the user attempting to edit it is the one that created it. If the check fails it raises a 403 error(Permission Denied) with a message.
class PostUpdate(UserPassesTestMixin, UpdateView):
    template_name_suffix = '_edit'
    model = Post
    
    fields = ['title', 'text']
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.published_date = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
     
    def handle_no_permission(self):
        raise PermissionDenied('You are not allowed to do that!')


#This Class Based View is a delete view along with a check to make sure the user attempting to delete it is the one that created it. If the check fails it raises a 403 error(Permission Denied) with a message.
class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        raise PermissionDenied('You are not allowed to do that!')


#This Class Based View is the generic signup view. It uses the UserCreationForm which is just a basic form that Django provided for us!
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('post_list')
    template_name = 'blog/sign_up.html'