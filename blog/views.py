from django.shortcuts import render, get_object_or_404
from .models import Post
from commons.python import helper


def post_list(request):
    posts = Post.published.all()
    posts = helper.get_pagination(request=request, object_list=posts, per_page=3)
    return render(request, template_name='post/list.html', context={'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request=request, template_name='post/detail.html', context={'post': post})
