from commons.python.utils import value_or_default

from blog.models import Post
from blog.python.forms import SearchForm, CommentForm


class PostDetailContext:
    def __init__(self, post: Post, comments, comment_form: CommentForm = None, similar_posts=None):
        self._post = post
        self._comments = comments
        self._comment_form = value_or_default(comment_form, CommentForm())
        self._similar_posts = similar_posts

    @property
    def comment_form(self):
        return self._comment_form

    @comment_form.setter
    def comment_form(self, value):
        self._comment_form = value

    @property
    def post(self):
        return self._post

    @post.setter
    def post(self, value):
        self._post = value

    @property
    def similar_posts(self):
        return self._similar_posts

    @similar_posts.setter
    def similar_posts(self, value):
        self._similar_posts = value

    def is_valid_comment_form(self) -> bool:
        return self.comment_form and self.comment_form.is_valid()

    def get_post_id_list(self):
        return self._post.tags.values_list('id', flat=True)

    def to_json(self):
        return {'post': self._post, 'comments': self._comments, 'comment_form': self._comment_form,
                'similar_posts': self._similar_posts}


class FormContext:

    def __init__(self, form: SearchForm = None, posts: list = None, query: str = None, tag: str = None):
        self.__posts = value_or_default(posts, [])
        self.__form = value_or_default(form, SearchForm())
        self.__query = query
        self.__tag = tag

    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, value):
        self.__form = value

    @property
    def query(self):
        return self.__query

    @query.setter
    def query(self, value: SearchForm):
        self.__query = value.cleaned_data.get('query')

    @property
    def posts(self):
        return self.__posts

    @posts.setter
    def posts(self, value):
        self.__posts = value

    def to_json(self):
        return {'form': self.form, 'query': self.query, 'posts': self.posts, 'tag': self.__tag}
