from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django import utils



class Category(models.Model):
	name=models.CharField(verbose_name=u"Category",max_length=50,unique=True)

	def __str__(self):
		return "Category ---> "+str(self.name)

class Post(models.Model):

	post_category=models.ForeignKey(Category,on_delete=models.CASCADE)
	post_owner=models.ForeignKey(User,verbose_name=u"Owner",on_delete=models.CASCADE)
	post_topic=models.CharField(max_length=250)
	post_content=models.TextField(max_length=1000)
	post_date=models.DateTimeField(auto_now_add=True)
	post_likes=models.ManyToManyField(User,related_name="likes",blank=True)

	def get_absolute_url(self):
		return reverse('debate:detail',kwargs={'pk' : self.id})
	def __str__(self):
		return str(self.post_category)+"--->"+str(self.post_owner)+"--->"+str(self.post_topic)

	@property
	def total_likes(self):
		return self.post_likes.count()

class Comment(models.Model):
	comment_name=models.ForeignKey(User,verbose_name=u"Owner",on_delete=models.CASCADE)
	comment_post=models.ForeignKey(Post,verbose_name=u'Topic',on_delete=models.CASCADE)
	comment_text=models.TextField(max_length=1000)
	comment_time=models.DateTimeField(default=utils.timezone.now)
	parent=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="replies")

	def __str__(self):
		return str(self.id)+'-'+str(self.comment_name) + ' - ' + str(self.comment_text)

	def children(self):
		return Comment.objects.filter(parent=self)

	def all(self):
		return Comment.objects.filter(parent=None).order_by('-comment_time')

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True