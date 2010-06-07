from django.contrib import admin
from models import *

class RefArticleAdmin(admin.ModelAdmin):
    list_display = ('category', 'article')
admin.site.register(RefArticle, RefArticleAdmin)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'site_url')
admin.site.register(Theme, ThemeAdmin)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'file')
admin.site.register(Template, TemplateAdmin)