from django.conf.urls import url,include
from . import views



app_name='debate'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^my_posts/(?P<pk>[0-9]+)$', views.my_posts,name='my_posts'),
    url(r'^categories/(?P<pk>[0-9]+)$', views.categories,name='categories'),
    url(r'^posts/(?P<pk>[0-9]+)$', views.detail,name='detail'),
   	url(r'^posts/create/$',views.CreatePost,name='post-create'),
   	url(r'^posts/(?P<pk>[0-9]+)/update/$',views.UpdatePost.as_view(),name='post-update'),
   	url(r'^posts/(?P<pk>[0-9]+)/delete/$',views.DeletePost,name='post-delete'),

    url(r'^categories/create/$',views.CreateCategory,name='category-create'),
    url(r'^categories/(?P<pk>[0-9]+)/delete/$',views.DeleteCategory,name='category-delete'),

    url(r'^posts/(?P<pk>[0-9]+)/comment/(?P<com_id>[0-9]+)$',views.delete_comment,name='delete-comment'),
    url(r'^like/$',views.like_post,name='like_post'),


   	url(r'^register/$',views.UserFormView.as_view(),name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

]
