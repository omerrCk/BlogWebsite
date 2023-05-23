from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Count
from django.urls import reverse
from django.template import loader
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from .forms import PostForm
from django.contrib import messages

def main(request):
    trendingPosts = Post.objects.values('title', 'slug').annotate(
        likecount=Count('likes')).order_by('-likecount')[:3]
    posts = Post.objects.all()
    template = loader.get_template('main.html')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(posts , 3) 
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'trendingPosts': trendingPosts,
    }
    return HttpResponse(template.render(context, request))


def blog_list(request):
    posts = Post.objects.all()
    template = loader.get_template('blog_list.html')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(posts , 4) 
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
    }
    return HttpResponse(template.render(context, request))

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','photo','body','status'] 
    template_name = 'blog_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog_list")

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'slug': slug}
        return render(request,'blog_edit.html',context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect("blog_list")
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'blog_edit.html',{'form':form})

def BlogPostLike(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))