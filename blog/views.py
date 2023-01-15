from commons.python.helper import get_pagination, is_post_method
from commons.python.smtp import send_email
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from taggit.models import Tag

from blog.models import Post
from blog.python import messages as msg
from blog.python.contexts.contexts import SearchFormContext, ListFormContext, PostDetailContext
from blog.python.forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def post_list(request, tag_slug=None):
    template = 'post/list.html'
    listform_context = ListFormContext(posts=Post.published.all())
    _filter_by_tag(listform_context, tag_slug)
    _paginate(request, listform_context)
    return render(request, template_name=template, context=listform_context.to_json())


def _filter_by_tag(listform_context: ListFormContext, tag_slug: str):
    if tag_slug:
        listform_context.tag = get_object_or_404(Tag, slug=tag_slug)
        listform_context.posts = listform_context.posts.filter(tags__in=[listform_context.tag])
    return listform_context


def _paginate(request, listform_context: ListFormContext):
    listform_context.posts = get_pagination(request, listform_context.posts, 3)
    return listform_context


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    postdetail_context = PostDetailContext(post=post, comments=post.comments.filter(active=True))

    if is_post_method(request):
        postdetail_context.comment_form = CommentForm(data=request.POST)
        if postdetail_context.is_valid_comment_form():
            _save_comment(request, postdetail_context)
            return redirect(post.get_absolute_url())
    _filter_similar_posts(postdetail_context)
    return render(request=request, template_name='post/detail.html', context=postdetail_context.to_json())


def _filter_similar_posts(postdetail_context: PostDetailContext):
    _filter_posts(postdetail_context)
    _aggregate_and_order(postdetail_context)


def _filter_posts(postdetail_context: PostDetailContext):
    postdetail_context.similar_posts = Post.objects.filter(
        tags__in=postdetail_context.get_post_id_list()).exclude(id=postdetail_context.post.id)


def _aggregate_and_order(postdetail_context: PostDetailContext):
    postdetail_context.similar_posts = postdetail_context.similar_posts.annotate(same_tags=Count('tags')).order_by(
        '-same_tags', '-publish')[:4]


def _save_comment(request, postdetail_context: PostDetailContext):
    new_comment = postdetail_context.comment_form.save(commit=False)
    new_comment.post = postdetail_context.post
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


# SearchVector e  SearchRank são específicos do postgres.
def post_search(request):
    search_context = SearchFormContext()
    if 'query' in request.GET:
        _filter_posts_if_valid_form(request, search_context)
    return render(request, template_name='post/search.html', context=search_context.to_json())


def _filter_posts_if_valid_form(request, searchform_context: SearchFormContext):
    searchform_context.form = SearchForm(request.GET)

    if searchform_context.form.is_valid():
        searchform_context.query = searchform_context.form
        search_vector = SearchVector('title', weight='A') + SearchVector('title', weight='B')
        search_query = SearchQuery(searchform_context.query)
        search_rank = SearchRank(search_vector, search_query)
        searchform_context.posts = Post.published.annotate(search=search_vector, rank=search_rank).filter(
            search=searchform_context.query).order_by('-rank')
    return searchform_context
