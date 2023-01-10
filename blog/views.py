from commons.python.helper import get_pagination, is_post_method
from commons.python.smtp import send_email
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .models import Post, Comment
from taggit.models import Tag
from .python.forms import EmailPostForm, CommentForm
# from .python.help.help import send_email


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def post_list(request, tag_slug=None):
    posts = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    posts = get_pagination(request=request, object_list=posts, per_page=3)
    return render(request, template_name='post/list.html', context={'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    if is_post_method(request):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}
    return render(request=request, template_name='post/detail.html', context=context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if is_post_method(request):
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cleaned_data.get("name")} recommends you read {post.title}'
            message = f"Read {post.title} at {post_url} \n\n " \
                      f"{cleaned_data.get('name')}\'s comments: {cleaned_data.get('comments')} "
            send_email(subject, message, cleaned_data.get('to'))
            messages.success(request, f'{post.title} was successfully sent to "{cleaned_data.get("to")}"')
    form = EmailPostForm()

    context = {'post': post, 'form': form, }
    return render(request=request, template_name='post/share.html', context=context)
