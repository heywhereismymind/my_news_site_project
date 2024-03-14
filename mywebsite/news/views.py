from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Article


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'news/article/detail.html', {'article': article})


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'news/article/list.html', {'articles': articles})
