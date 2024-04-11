from django import forms
from mywebsite.news.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=255)
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
