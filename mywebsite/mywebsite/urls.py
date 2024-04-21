from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from news.sitemaps import ArticleSitemap

sitemaps = {
    "articles": ArticleSitemap
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("news/", include("news.urls", namespace="news")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
