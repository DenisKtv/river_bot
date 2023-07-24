from django.contrib import admin

from .models import Group, Image, Post


class ImageInline(admin.TabularInline):
    model = Image


class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'short_text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'
    inlines = [ImageInline]


admin.site.register(Post, NewsAdmin)
admin.site.register(Group)
