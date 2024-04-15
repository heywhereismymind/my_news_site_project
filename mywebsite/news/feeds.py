import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Article


class LatestArticleFeed(Feed):
    title = "My news"
    link = reverse_lazy("news:article_list")
    description = "New articles of my news site."

    def items(self):
        return Article.published.all()[:3]

    def item_headline(self, item: Article):
        return item.headline

    def item_description(self, item: Article):
        return truncatewords_html(markdown.markdown(item.content), 30)

    def item_pubdate(self, item: Article):
        return item.publish
