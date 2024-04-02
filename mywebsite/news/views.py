from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from mywebsite.settings import EMAIL_HOST_USER

from .models import Article


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
        request, "news/article/share.html", {"article": article, "form": form}
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
    return render(request, "news/article/detail.html", {"article": article})


class ArticleListView(ListView):
    """
    View to display
    """

    queryset = Article.published.all()
    context_object_name = "articles"
    paginate_by = 2
    template_name = "news/article/list.html"
