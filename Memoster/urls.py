"""Memoster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import Post.views
import Register_Page.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('register/', Register_Page.views.register, name='Register_Page'),
    path('home/', Post.views.home, name='Home_Page'),
    path('post/', Post.views.post, name='Post_Page'),
    path('login/', Register_Page.views.login_page, name='Login_Page'),
    path('logout/', Register_Page.views.logout_user, name='Logout_Page'),
    path('user/', Post.views.user_home, name='Home'),
    path('edit/', Register_Page.views.edit, name='Edit_Page'),
    path('profile/', Register_Page.views.show_profile, name='Profile_Page'),
    path('list/', Register_Page.views.user_list, name='User_List'),
    path('comment/<int:identity>', Post.views.comment_update, name='Comment_Update'),
    path('god/', Post.views.god, name="Shrine_of_our_God"),
    path('theme/', Register_Page.views.theme_builder, name="Build_your_Themes"),
    path('test/<int:test_val>', Post.views.test, name="Test"),
    path('ring/<str:reload>/<str:len_msgs>/<str:edit_msgs>/<int:ring_id>', Post.views.ring, name='Ring')
]
