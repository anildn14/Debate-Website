from rest_framework.serializers import ModelSerializer
from debate.models import Post


class PostListSerializer(ModelSerializer):
    class Meta:
    	model = Post
    	fields="__all__"
    	# fields = [
    	# 'post_category','post_owner','post_topic','post_content','post_date','post_likes'
    	# ]

class PostDetailSerializer(ModelSerializer):
    class Meta:
    	model = Post
    	fields="__all__"