from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=255)
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)
