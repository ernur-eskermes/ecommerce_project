from modeltranslation.translator import register, TranslationOptions

from .models import (
    Author,
    Genre,
    Publisher,
    Product,
    Category,
)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Publisher)
class PublisherTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'book_series', 'binding', 'language')
