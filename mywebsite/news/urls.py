from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .feeds import LatestArticlesFeed
from .sitemaps import ArticleSitemap

sitemaps = {
    'static': ArticleSitemap,
}

app_name = "news"
urlpatterns = [
    path("", views.article_list, name="article_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:article_slg>",
        views.article_detail,
        name="article_detail",
    ),
    path("<int:article_id>/share", views.article_share, name="article_share"),
    path("<int:article_id>/comment/", views.article_comment, name="article_comment"),
    path("tag/<slug:tag_slug>", views.article_list, name="article_list_by_tag"),
    path("feed/", LatestArticlesFeed(), name="article_feed"),
    path("search/", views.article_search, name="article_search"),
    path("ranks/", views.article_ranks, name="article_ranks"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
