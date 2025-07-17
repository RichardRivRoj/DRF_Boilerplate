from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Post

from .serializers import PostListSerializer, PostSerializer

class PostListView(ListAPIView):
    queryset = Post.post_objects.all()
    serializer_class = PostListSerializer

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostDetailView(RetrieveAPIView):
    queryset = Post.post_objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)