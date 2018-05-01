# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from .forms import ContactForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import F

def post_inquiry(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'projectblog/post_inquiry.html', {'form': form})

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'projectblog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'projectblog/post_detail.html', {'post': post})
def post_new(request):
    form = PostForm()
    return render(request, 'projectblog/post_edit.html', {'form': form})  
def post_delete(request):
    post = get_object_or_404(Post, pk=pk)    
    return render(request, 'projectblog/post_delete.html', {'form': form})  
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'projectblog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'projectblog/post_edit.html', {'form': form})
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        post.delete()
        return redirect('post_list')

    else:
        form = PostForm(instance=post)
    return render(request, 'projectblog/post_delete.html', {'form': form})
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'projectblog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.upvotes += 1
    return redirect('post_list', pk=pk)

def downvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.upvotes -= 1
    return redirect('post_list', pk=pk)