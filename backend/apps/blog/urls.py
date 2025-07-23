from django.urls import path

from .views import (
    PostListView, 
    PostDetailView, 
    PostHeadingView, 
    IncrementPostView
)


urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/headings/', PostHeadingView.as_view(), name='post-headings'),
    path('post/<slug:slug>/increment_clicks/', IncrementPostView.as_view(), name='increment-post-clickd')
    
]
