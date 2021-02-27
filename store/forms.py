from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Contact, Review, Product


class ProductAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget)
    description_en = forms.CharField(label='Descrition', widget=CKEditorUploadingWidget)

    class Meta:
        model = Product
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('email',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('subject', 'comment')
        widgets = {
            'subject': forms.TimeInput(attrs={'placeholder': 'Subject'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Comment'})
        }
