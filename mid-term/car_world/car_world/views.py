from django.shortcuts import get_object_or_404, render

from brand.models import Brand
from car.models import Car


def home(request, brand_slug=None):
    data = Car.objects.select_related('brand').order_by('-id')
    selected_brand = None
    if brand_slug is not None:
        selected_brand = get_object_or_404(Brand, slug=brand_slug)
        data = data.filter(brand=selected_brand)
    brands = Brand.objects.exclude(slug__isnull=True).exclude(slug='').order_by('name')
    return render(request, 'home.html', {
        'data': data,
        'brand': brands,
        'selected_brand': selected_brand,
    })
