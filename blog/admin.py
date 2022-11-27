from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'create_date', 'publish', 'author')
    search_fields = ('title', 'body',)
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish',)
    # autocomplete the slug field when input something in the title field
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'create_date', 'active')
    list_filter = ('active', 'create_date', 'update_date')
    search_fields = ('name', 'email', 'body')
