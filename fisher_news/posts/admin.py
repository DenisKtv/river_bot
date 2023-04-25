from django.contrib import admin
from .models import Post, Group


class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'


admin.site.register(Post, NewsAdmin)
admin.site.register(Group)
