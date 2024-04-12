from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Article


register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_most_commented_articles(count=3):
    return Article.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


@register.simple_tag
def total_articles():
    return Article.published.count()


@register.inclusion_tag("news/article/latest_articles.html")
def show_latest_articles(count=3):
    latest_articles = Article.published.order_by("-publish")[:count]
    return {"latest_articles": latest_articles}
