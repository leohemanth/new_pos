from django.contrib import admin
from models import *
from mksites.admin import SubdomainAdmin

class ArticleAdmin(SubdomainAdmin):
    date_hierarchy = 'updated'
    list_display = ('title', 'category', 'author', 'creation', 'updated')
admin.site.register(Article, ArticleAdmin)


class MenuAdmin(SubdomainAdmin):
    list_display = ('name', 'parent')
admin.site.register(Menu, MenuAdmin)


class CategoryAdmin(SubdomainAdmin):
    save_as=True
    list_display = ('short_title', 'title', 'menu', 'order', 'parent')
    list_filter = ('menu', 'parent')
admin.site.register(Category, CategoryAdmin)


class LinkAdmin(SubdomainAdmin):
    list_display = ('title', 'menu', 'category', 'url')
admin.site.register(Link, LinkAdmin)