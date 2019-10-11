from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView
	)

from debate.models import Post
from .serializers import PostListSerializer,PostDetailSerializer


# http://127.0.0.1:8000/api/debate/?format=json #for json format

class PostListAPIView(ListAPIView):
	queryset=Post.objects.all()
	serializer_class=PostListSerializer


class PostDetailAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer

class PostUpdateAPIView(UpdateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer

class PostDeleteAPIView(DestroyAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer