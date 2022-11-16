from django.contrib import admin
from .models import Post


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
