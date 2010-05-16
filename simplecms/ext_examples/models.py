from django.db import models
from simplecms.cms.models import Category, Article

class Theme(models.Model):
    name = models.CharField(max_length = 100, unique=True)
    def __unicode__(self):
            return self.name
    def site_url(self):
        return '<a href=../../../%s/>voir</a>' % self.name
    site_url.allow_tags = True

class Template(models.Model):
    name = models.CharField(max_length = 100)
    theme = models.ForeignKey(Theme)
    file = models.FileField(upload_to='templates')


class RefArticle(models.Model):
    category = models.ForeignKey(Category)
    article = models.ForeignKey(Article)
    
    def title(self):
        return self.article.title
    
    def text(self):
        return self.article.text
    
    def author(self):
        return self.article.author
    
    def slug(self):
        return self.article.slug
    
    def __unicode__(self):
        return self.article.title;

    class Meta:
        verbose_name = 'Article reference'
        verbose_name_plural = 'Articles references'

# TODO: file uploader

# Rich Article

# menu bottom

# rich menu

# member access