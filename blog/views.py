from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.edit import DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy


# Create your views here.
def post_table(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_table.html', {'posts': posts})

def post_detail(request, pk):
    post=get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method =="POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form =PostForm()

    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)

    if request.method=="POST":
        form=PostForm(request.POST, instance=post)

        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form=PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form':form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post.delete()
            return redirect('blog:post_table')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_delete.html', {'form':form})


