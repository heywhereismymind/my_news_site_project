from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib import messages

from mywebsite.settings import EMAIL_HOST_USER

from .models import Article, Comment
from .forms import EmailPostForm, CommentForm, SearchForm

import redis
from django.conf import settings


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def article_share(request, article_id):
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())

            subject = f"{cd['name']} recommends you read {article.headline}"

            message = (
                f"Read {article.headline} at {article_url}\n\n"
                f"{cd['name']}'s comments: {cd['comment']}"
            )

            send_mail(subject, message, EMAIL_HOST_USER, [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        "news/article/share.html",
        {"article": article, "form": form, "sent": sent},
    )


def article_detail(request, year, month, day, article_slg):
    article = get_object_or_404(
        Article,
        status=Article.Status.PUBLISHED,
        slug=article_slg,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = article.comments.filter(active=True)
    form = CommentForm()

    article_tags_ids = article.tags.values_list("id", flat=True)
    similar_articles = Article.published.filter(tags__in=article_tags_ids).exclude(
        id=article.id
    )
    similar_articles = similar_articles.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:2]

    messages.success(request, "article_detail loaded successfully")

    total_views = r.incr(f"article:{article.id}:views")
    r.zincrby("article_ranks", 1, article.id)

    return render(
        request,
        "news/article/detail.html",
        {
            "article": article,
            "comments": comments,
            "form": form,
            "similar_articles": similar_articles,
            "total_views": total_views,
        },
    )


def article_list(request, tag_slug=None):
    article_list = Article.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        article_list = article_list.filter(tags__in=[tag])

    paginator = Paginator(article_list, 2)
    page_number = request.GET.get("page", 1)

    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    else:
        messages.success(request, "article_list loaded successfully")

    return render(request, "news/article/list.html", {"articles": articles, "tag": tag})


@require_POST
def article_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()

        messages.success(request, "article_comment loaded successfully")

    return render(
        request,
        "news/article/comment.html",
        {"article": article, "form": form, "comment": comment},
    )


def article_ranks(request):
    article_ranks = r.zrange("article-ranks", 0, -1, desc=True)[:5]

    article_ranks_ids = [int(id) for id in article_ranks]

    most_read_news = list(Article.objects.filter(id__in=article_ranks_ids))
    most_read_news.sort(key=lambda x: article_ranks_ids.index(x.id))

    return render(
        request,
        "news/article/ranks.html",
        {"most_read_news": most_read_news},
    )


def article_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]

            search_vector = SearchVector("headline", "content", config="russian")
            search_query = SearchQuery(query, config="russian")

            results = (
                Article.published.annotate(
                    similarity=TrigramSimilarity("headline", query),
                )
                .filter(similarity__lte=0.1)
                .order_by("-similarity")
            )

    return render(
        request,
        "news/article/search.html",
        {"form": form, "query": query, "results": results},
    )
