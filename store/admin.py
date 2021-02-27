from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .forms import ProductAdminForm
from .models import (
    Author,
    Genre,
    Publisher,
    Product,
    Category,
    Image,
    Contact,
    Review,
)


@admin.register(Author)
class AuthorAdmin(TranslationAdmin):
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    search_fields = ('name',)
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Publisher)
class PublisherAdmin(TranslationAdmin):
    search_fields = ('name',)
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    search_fields = ('name',)
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     pass


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('get_image', 'name', 'price',
                    'author', 'genre', 'available')
    list_filter = ('available', 'created')
    list_editable = ('available',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'author__name', 'genre__name')
    inlines = [ImageInline]
    save_on_top = True
    list_display_links = ('get_image', 'name')
    readonly_fields = ('get_image',)
    form = ProductAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.base_photo.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('id', 'subject', 'status')


admin.site.site_title = 'Aroma shop administration'
admin.site.site_header = 'Aroma shop administration'
