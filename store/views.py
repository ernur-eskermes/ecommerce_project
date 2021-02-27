from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm, ContactForm
from .models import Product, Category, Publisher, Review
from .tasks import send_spam_email


def search_books(request):
    """Поискавик"""
    products = Product.objects.filter(
        name__icontains=request.GET.get('q').strip()
    )
    return products


def pagination(request, products: list, max_prod: int):
    """Пагинация"""
    paginator = Paginator(products, max_prod)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return products


def product_filter(request, products):
    """Фильтрация продуктов."""
    sort_param = request.GET.get('sort')
    if sort_param == 'newer':
        products = products.order_by('-created')
    elif sort_param == 'descending':
        products = products.order_by('-price')
    elif sort_param == 'ascending':
        products = products.order_by('price')
    elif sort_param == 'reviews':
        products = sorted(products, key=lambda p: p.get_rate, reverse=True)

    price_range = request.GET.get('price_range')
    if price_range == '0_1000':
        products = products.filter(price__gt=0, price__lte=1000)
    elif price_range == '1001_2500':
        products = products.filter(price__gt=1001, price__lte=2500)
    elif price_range == '2501_5000':
        products = products.filter(price__gt=2501, price__lte=5000)
    elif price_range == '5001_7500':
        products = products.filter(price__gt=5001, price__lte=7500)
    elif price_range == '7501_10000':
        products = products.filter(price__gt=7501, price__lte=10000)
    elif price_range == '10001_15000':
        products = products.filter(price__gt=10001, price__lte=15000)
    return products


def product_list(request, category_slug=None, publisher_slug=None):
    """Список продуктов."""
    category = None
    publisher = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if publisher_slug:
        publisher = get_object_or_404(Publisher, slug=publisher_slug)
        products = products.filter(publisher=publisher)

    if request.GET.get('q'):
        products = search_books(request)

    if request.GET.get('price_range') or request.GET.get('sort'):
        products = product_filter(request, products)

    if request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            data = contact_form.save(commit=False)
            try:
                data.user = request.user
            except ValueError:
                pass
            data.save()
            email = contact_form.cleaned_data['email']
            send_spam_email.delay(email)
            return redirect('/')
    else:
        contact_form = ContactForm()

    categories = Category.objects.all()
    publishers = Publisher.objects.all()
    products = pagination(request, products=products, max_prod=9)
    return render(request, 'store/product-list.html',
                  {'category': category, 'products': products, 'categories': categories,
                   'publisher': publisher, 'publishers': publishers, 'contact_form': contact_form})


def create_review(request, product_id):
    product = Product.objects.get(id=product_id)
    """Создание комментариев."""
    if request.method == 'POST':
        create_review_form = ReviewForm(request.POST)
        if create_review_form.is_valid():
            data = create_review_form.save(commit=False)
            data.product = product
            data.user = request.user
            data.rate = request.POST.get('simple-rating', 0)
            data.save()
            return redirect('store:detail', product.id, product.slug)


def update_review(request, review_id):
    """Обновление или удаление комментариев."""
    review = Review.objects.get(id=review_id)
    if request.method == 'POST' and 'delete_button' in request.POST:
        review.delete()
        return redirect('store:detail', review.product.id, review.product.slug)
    elif request.method == 'POST' and 'save_update_button' in request.POST:
        update_review_form = ReviewForm(data=request.POST, instance=review)
        if update_review_form.is_valid():
            data = update_review_form.save(commit=False)
            data.rate = request.POST.get('simple-rating', review.rate)
            data.save()
            return redirect('store:detail', review.product.id, review.product.slug)


def detail(request, pk: int, slug: str):
    """Вывод продукта."""
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=pk, slug=slug, available=True)
    related_products_by_genre = Product.objects.filter(genre=product.genre)
    if len(related_products_by_genre) < 4:
        related_products_by_genre = None

    try:
        review = Review.objects.get(product=product, user=request.user)
    except Review.DoesNotExist:
        review = None

    if review:
        update_review_form = ReviewForm(instance=review)
        create_review_form = None
    else:
        create_review_form = ReviewForm()
        update_review_form = None

    publishers = Publisher.objects.all()
    reviews = Review.objects.filter(product=product)
    return render(request, 'store/single-product.html', {
        'product': product, 'categories': categories,
        'related_products': related_products_by_genre, 'publishers': publishers,
        'create_review_form': create_review_form,
        'reviews': reviews, 'update_review_form': update_review_form
    })


def contact(request):
    """Информации о магазине."""
    return render(request, 'store/contact.html')
