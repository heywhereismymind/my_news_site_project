from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = "news"
router = DefaultRouter()
router.register("articles", views.ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("articles/", views.ArticleList.as_view(), name="article_list"),
    path("articles/<pk>/", views.ArticleDetail.as_view(), name="article_detail"),
]
