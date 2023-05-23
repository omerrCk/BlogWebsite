from django.urls import path
from . import views
from .views import CreatePostView, PostDetailView 

urlpatterns = [
    path('', views.main, name='main'),
    path("blog/", views.blog_list, name="blog_list"),
    path('blog/create', CreatePostView.as_view(),name='blog_create'),
    path('blog/edit/<slug:slug>', views.edit_post, name='post-edit'),
    path("blog/<slug:slug>", PostDetailView.as_view(), name="post_detail"),
    path('blogpost-like/<slug:slug>', views.BlogPostLike, name="blogpost_like")
]



