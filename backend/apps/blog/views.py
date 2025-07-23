from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException

from .models import Post, Heading, PostView, PostAnalytics

from .serializers import PostListSerializer, PostSerializer, HeadingSerializer

from .utils import get_client_ip

#class PostListView(ListAPIView):
#    queryset = Post.post_objects.all()
#    serializer_class = PostListSerializer
#
#    def get(self, request, *args, **kwargs):
#        posts = self.get_queryset()
#        serializer = self.get_serializer(posts, many=True)
#        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostListView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.post_objects.all()
            
            if not posts.exists():
                return NotFound(detail="No posts found.")
            serialized_post = PostListSerializer(posts, many=True).data
        except Post.DoesNotExist:
            raise NotFound(detail="No posts found.")
        except Exception as e:
            raise APIException(detail=f"An unexpected error occurred: {str(e)}")
            
            
        return Response(serialized_post, status=status.HTTP_200_OK)


#class PostDetailView(RetrieveAPIView):
#    queryset = Post.post_objects.all()
#    serializer_class = PostSerializer
#    lookup_field = 'slug'
#
#    def get(self, request, *args, **kwargs):
#        post = self.get_object()
#        serializer = self.get_serializer(post)
#        return Response(serializer.data, status=status.HTTP_200_OK)

class PostDetailView(RetrieveAPIView):
    def get(self, request, slug):
        try:
            post = get_object_or_404(Post.post_objects, slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="The requested post does not exist.")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurreed: {str(e)}")
        
        try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.increment_view(request)  # ✅ Ahora guarda los cambios
        except PostAnalytics.DoesNotExist:
            raise NotFound(detail="Analytics for this post does not exist.")
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updating post analytics: {str(e)}")   
            
        serializer = PostSerializer(post)
        return Response(serializer.data)

    
class PostHeadingView(ListAPIView):
    serializer_class = HeadingSerializer
    
    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter(post__slug = post_slug)
    
class IncrementPostView(APIView):
    
    def post(self, request, slug):
        
        """"
        Incrementa el contador de clicks de un  post basado en su slug
        """
        try:
            post = Post.post_objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="Te requested post does not exist.")
        
        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(detail=f"An error occurred while incrementing the view: {str(e)}")
        return Response({
            "message": "Post view incremented successfully.",
            "clicks": post_analytics.clicks, },
                        status= status.HTTP_200_OK)