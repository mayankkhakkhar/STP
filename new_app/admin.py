from django.contrib import admin
from .models import Article
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    title = Article.title


admin.site.register(Article, ArticleAdmin)
