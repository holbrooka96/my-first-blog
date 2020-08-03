from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('logout/', LogoutView.as_view(template_name='blog/logged_out.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),

]