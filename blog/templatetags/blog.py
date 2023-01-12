from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
from blog.models import Post
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('post/partials/lastest_posts.html')
def show_latest_posts(count=5):
    latest = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:5]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
