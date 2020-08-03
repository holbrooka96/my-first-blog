from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.views.generic.edit import DeleteView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm






# Create your views here.
class PostList(ListView):
    model = Post

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class PostNew(CreateView):
    model = Post
    fields = ['title', 'text']
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.published_date = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostUpdate(UpdateView):
    template_name_suffix = '_edit'
    model = Post
    fields = ['title', 'text']
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.published_date = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('post_list')
    template_name = 'blog/sign_up.html'