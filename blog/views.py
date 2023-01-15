from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from commons.python.helper import get_pagination, is_post_method
from commons.python.smtp import send_email
from django.contrib import messages
from django.db.models import QuerySet, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from taggit.models import Tag

from .models import Post
from blog.python.forms import EmailPostForm, CommentForm, SearchForm
from blog.python import messages as msg


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def post_list(request, tag_slug=None):
    template = 'post/list.html'
    posts = Post.published.all()
    posts = _filter_by_tag(posts, tag_slug)
    posts = _paginate(request, posts)
    return render(request, template_name=template, context=posts)


def _filter_by_tag(posts: QuerySet, tag_slug: str) -> dict:
    retorno = {'posts': posts, 'tag': None}
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        retorno['posts'] = posts
        retorno['tag'] = tag
    return retorno


def _paginate(request, posts_tag) -> dict:
    posts_paginated = get_pagination(request, posts_tag.get('posts'), 3)
    posts_tag.update({'posts': posts_paginated})
    return posts_tag


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    if is_post_method(request):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            save_comment(request, post, comment_form)
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    similar_posts = _get_similar_posts(post)
    context = {'post': post, 'comments': comments,
               'comment_form': comment_form,
               'similar_posts': similar_posts}
    return render(request=request, template_name='post/detail.html', context=context)


def _get_similar_posts(post: Post):
    post_tags_ids = _get_ids_list(post)
    similar_posts = _filter_posts(post.id, post_tags_ids)
    return _aggregate_and_order_posts(similar_posts)


def _get_ids_list(post: Post):
    return post.tags.values_list('id', flat=True)


def _filter_posts(current_post_id, ids_list: list):
    return Post.objects.filter(tags__in=ids_list).exclude(id=current_post_id)


def _aggregate_and_order_posts(posts_list: QuerySet):
    return posts_list.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]


def save_comment(request, post: Post, form: CommentForm):
    new_comment = form.save(commit=False)
    new_comment.post = post
    new_comment.save()
    messages.success(request, msg.comment_success_save())


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if is_post_method(request):
        form = EmailPostForm(request.POST)
        _share_post_if_valid_form(request, form, post)
    form = EmailPostForm()

    context = {'post': post, 'form': form, }
    return render(request=request, template_name='post/share.html', context=context)


def _share_post_if_valid_form(request, form: EmailPostForm, post: Post):
    if form.is_valid():
        cleaned_data = form.cleaned_data
        url = _build_url(request, post)
        subject = msg.mail_subject(cleaned_data.get("name"), post.title)
        message = msg.mail_message(post.title, url, cleaned_data.get('name'), cleaned_data.get('comments'))

        send_email(subject, message, cleaned_data.get('to'))
        messages.success(request, not msg.mail_success_msg(post.title, cleaned_data.get("to")))


def _build_url(request, post):
    return request.build_absolute_uri(post.get_absolute_url())


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            search_rank = SearchRank(search_vector, search_query)
            results = Post.published.annotate(search=search_vector, rank=search_rank).filter(search=query).order_by(
                '-rank')
    context = {'form': form, 'query': query, 'posts': results}
    return render(request, template_name='post/search.html', context=context)
