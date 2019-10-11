from django.conf.urls import url,include
from django.contrib import admin
# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
# debate.api.views
from .views import (
	PostListAPIView,
	PostDetailAPIView,
	PostUpdateAPIView,
	PostDeleteAPIView,
	)


urlpatterns = [
    url(r'^posts/$',PostListAPIView.as_view(),name='post-list'),
    url(r'^posts/(?P<pk>\d+)$',PostDetailAPIView.as_view(),name='post-detail'),
    url(r'^posts/(?P<pk>\d+)/update/$',PostUpdateAPIView.as_view(),name='post-update'),
    url(r'^posts/(?P<pk>\d+)/delete/$',PostDeleteAPIView.as_view(),name='post-delete'),
]