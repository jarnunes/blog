from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
from blog.models import Post
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('post/partials/_latest_posts.html')
def show_latest_posts(count=5):
    latest = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest}


@register.simple_tag
def get_most_commented_posts():
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='greaterthan')
def greater_than(list_object: list, arg):
    return True if list_object and len(list_object) > arg else False


@register.filter(name='count')
def count(list_object):
    return count(list_object)
