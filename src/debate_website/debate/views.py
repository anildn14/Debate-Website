from django.shortcuts import render
from .models import Category,Post,Comment
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from .forms import UserForm,PostForm,CategoryForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect




class UserFormView(View):
	form_class=UserForm
	template_name='debate/registration_form.html'


	def get(self,request):
		all_categories=Category.objects.all()
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form,'all_categories':all_categories})

	def post(self,request):
		all_categories=Category.objects.all()

		form=self.form_class(request.POST)

		if form.is_valid():
			user= form.save(commit=False) #not yet saved in DB due to commit=False

			username=form.cleaned_data['username']	#if username is email for logging in
			password=form.cleaned_data['password']
			user.set_password(password)
			user.save()


			user= authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request,user)
					return redirect('debate:index')
				else:
					return render(request, 'debate/index.html', {'all_posts': Post.objects.order_by('post_date'), 'all_categories':all_categories})
			else:
				messages.error(request,"Invalid Login")
				return redirect("debate:register")

		return render(request,self.template_name,{'form':form,'all_categories':all_categories})

def login_user(request):
	all_categories=Category.objects.all()
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				all_posts = Post.objects.order_by('post_date')
				if 'next' in request.POST:
					return redirect(request.POST.get('next'))
				else:
					return redirect('debate:index')
			else:
				messages.error(request,"Your account has been disabled")
				return redirect("debate:login_user")
		else:
			messages.error(request,"Invalid Login")
			return redirect("debate:login_user")
	return render(request, 'debate/login.html', {'all_categories':all_categories})

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		"form": form,
	}
	return redirect('debate:login_user')


def index(request):
	all_categories=Category.objects.all()
	all_posts=Post.objects.all()
	query = request.GET.get("q")
	if query:
		all_posts = all_posts.filter(
			Q(post_topic__icontains=query)
			| Q(post_category__name__icontains=query)
			| Q(post_owner__username__icontains=query)
		).distinct()
		print ("query_all_posts:",all_posts)
		print ("query_all_posts :",all_posts == None)
		print ("all_posts.count() :",all_posts.count())
		if all_posts.count()!=0:
			print ("all_posts :",all_posts)
			print ("all_posts is available")
			return render(request, 'debate/index.html', {'all_categories':all_categories,'all_posts': all_posts})
		else:
			messages.error(request,"No Post found for %s."%query)
			return redirect("debate:index")
	else:
		return render(request, 'debate/index.html', {'all_categories':all_categories,'all_posts': all_posts.order_by('-id')})

def my_posts(request,pk):
	all_categories=Category.objects.all()
	all_posts=Post.objects.filter(post_owner=pk)
	print("all_posts :",all_posts)
	query = request.GET.get("q")
	if query:
		all_posts = all_posts.filter(
			Q(post_topic__icontains=query)
			| Q(post_category__name__icontains=query)
			| Q(post_owner__username__icontains=query)
		).distinct()
		print ("query_all_posts:",all_posts)
		print ("query_all_posts :",all_posts == None)
		print ("all_posts.count() :",all_posts.count())
		if all_posts.count()!=0:
			print ("all_posts :",all_posts)
			print ("all_posts is available")
			return render(request, 'debate/index.html', {'all_categories':all_categories,'all_posts': all_posts})
		else:
			messages.error(request,"No Post found for %s."%query)
			return redirect("debate:index")
	else:
		return render(request, 'debate/index.html', {'all_categories':all_categories,'all_posts': all_posts.order_by('post_date')})

def categories(request,pk):
	all_categories=Category.objects.all()
	all_posts=Post.objects.filter(post_category=pk)
	print("all_posts :",all_posts)
	query = request.GET.get("q")
	if query:
		all_posts = all_posts.filter(
			Q(post_topic__icontains=query)
			| Q(post_category__name__icontains=query)
			| Q(post_owner__username__icontains=query)
		).distinct()
		print ("query_all_posts:",all_posts)
		print ("query_all_posts :",all_posts == None)
		print ("all_posts.count() :",all_posts.count())
		if all_posts.count()!=0:
			print ("all_posts :",all_posts)
			print ("all_posts is available")
			return render(request, 'debate/index.html', {'all_categories':all_categories,'all_posts': all_posts})
		else:
			messages.error(request,"No Post found for %s."%query)
			return redirect("debate:index")
	else:
		return render(request, 'debate/index.html', {'all_categories':all_categories,'all_posts': all_posts.order_by('post_date')})


def detail(request,pk):
	all_categories=Category.objects.all()
	posts=get_object_or_404(Post,id=pk)
	print("all_posts :",posts)
	print("dir(posts) :",dir(posts))
	all_comments=Comment.objects.filter(comment_post=pk,parent=None).order_by('-comment_time')
	print("all_comments :",all_comments)
	is_liked=False
	if posts.post_likes.filter(id=request.user.id).exists():
		is_liked=True
	query = request.GET.get("q")
	print ("request.method :",request.method)
	if request.method=='POST':
		print("POST FORM")

		if request.user.is_authenticated:
			form = CommentForm(request.POST or None)
			if form.is_valid():
				print("valid")
				comment = form.save(commit=False)
				comment.comment_text=request.POST.get('comment_text')
				comment.parent_id=request.POST.get('parent_id')
				comment_text=request.POST.get('comment_text')
				parent_qs=None
				try:
					parent_id=int(request.POST.get("parent_id"))
				except:
					parent_id=None
				if parent_id:
					parent_qs=Comment.objects.get(id=parent_id)
				comment=Comment.objects.create(comment_name=request.user,comment_post=posts,comment_text=comment.comment_text,parent=parent_qs)
				comment.save()
				return redirect('debate:detail',pk=pk)
		else:
			messages.error(request,"Login to comment")
			form=CommentForm()
	else:
		form=CommentForm()
		print("GET FORM")

	context={
				'posts': posts,
				'pk':pk,
				'is_liked':is_liked,
				'total_likes':posts.total_likes,
				'all_categories':all_categories,
				'all_comments':all_comments,
				'form':form,
			}

	return render(request, 'debate/detail.html', context)
	
@login_required(login_url='debate:login_user')
def CreateCategory(request):
	all_categories=Category.objects.all()
	form = CategoryForm(request.POST or None)
	if request.user.is_superuser:
		if form.is_valid():
			category = form.save(commit=False)
			category.save()
			return redirect("debate:index")
	else:
		messages.error(request,"User must me admin to add category")
	context = {
		"form": form,'all_categories':all_categories
	}
	return render(request, 'debate/post_form.html', context)


@login_required(login_url='debate:login_user')
def DeleteCategory(request,pk):
	category=Category.objects.get(id=pk)
	if request.user.is_superuser:
		category.delete()
		messages.success(request,str(category.name)+ " category deleted successfully")
		return redirect('debate:index')
	else:
		messages.error(request,"User must be admin to delete a category")
		return redirect('debate:index')

@login_required(login_url='debate:login_user')
def CreatePost(request):
	all_categories=Category.objects.all()
	form = PostForm(request.POST or None)#, request.FILES or None)

	if form.is_valid():
		post = form.save(commit=False)
		post.post_owner=request.user
		post.save()
		return redirect("debate:index")
	context = {
		"form": form,'all_categories':all_categories
	}
	return render(request, 'debate/post_form.html', context)

class UpdatePost(UserPassesTestMixin,UpdateView):#LoginRequiredMixin,UserPassesTestMixin,UpdateView):#,UserPassesTestMixin,PermMixin,PermissionRequiredMixin
	model=Post
	# fields='__all__'
	fields=['post_topic','post_category','post_content']
	def test_func(self):
		post=self.get_object()
		print ("self.request.user.is_superuser :",self.request.user.is_superuser)
		print ("self.request.user :",self.request.user)
		print ("post.post_owner :",post.post_owner)
		print ("self.request.user == post.post_owner :",self.request.user == post.post_owner)
		if self.request.user == post.post_owner :
			return True
		else:
			messages.error(self.request,"User must be owner of this post to update")
			return False
			return redirect("debate:detail",pk=post.id)

def DeletePost(request, pk):
	post = Post.objects.get(id=pk)
	if request.user == post.post_owner:
		post.delete()
		return redirect('debate:index')

	else:
		messages.error(request,"User must be owner of this post to delete")
		return redirect("debate:detail",pk=pk)

@login_required(login_url='rap:login_user')
def delete_comment(request,pk,com_id):
	comment = Comment.objects.get(pk=com_id)
	com_name=Comment.objects.get(pk=com_id).comment_name
	print ("com_name :",com_name)
	print("request.user.username :",request.user.username)
	print("com_name == request.user.username :",com_name == request.user)
	if com_name == request.user: #or request.user.is_superuser:
		comment.delete()
		messages.success(request,"Comment deleted successfully")
		return redirect('debate:detail',pk=pk)
	else:
		messages.error(request,"User must be owner of this comment to delete")
		return redirect("debate:detail",pk=pk)

def like_post(request):
	posts=get_object_or_404(Post,id=request.POST.get('posts_id'))
	is_liked=False
	if posts.post_likes.filter(id=request.user.id).exists():
		posts.post_likes.remove(request.user)
		is_liked=False
	else:
		posts.post_likes.add(request.user)
		is_liked=True

	print("posts :",posts)
	print("request.user :",request.user)
	return HttpResponseRedirect(posts.get_absolute_url())