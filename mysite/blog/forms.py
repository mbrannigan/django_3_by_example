"""forms for blog application."""
from django import forms


class EmailPostForm(forms.Form):
    """Form for sending blog entries via email."""

    name: forms.CharField = forms.CharField(max_length=25, label="Your Name")
    email: forms.EmailField = forms.EmailField(label="Your Email")
    to: forms.EmailField = forms.EmailField(label="Receipient Email")
    comments: forms.CharField = forms.CharField(required=False, widget=forms.Textarea)
