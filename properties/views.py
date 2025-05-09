from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Property

def index(request):
    return property_listings(request)

def property_listings(request):
    # Start with all properties
    properties = Property.objects.all()

    # Read filters from the GET request
    search = request.GET.get('search_filter')
    zip_code = request.GET.get('zip')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    type_filter = request.GET.get('type')
    order_by = request.GET.get('order_by')

    # Apply filters if provided
    if search:
        properties = properties.filter(title__icontains=search)

    if zip_code:
        properties = properties.filter(zip=zip_code)

    if price_min:
        properties = properties.filter(price__gte=price_min)

    if price_max:
        properties = properties.filter(price__lte=price_max)

    if type_filter:
        properties = properties.filter(type__iexact=type_filter)

    if order_by == "price":
        properties = properties.order_by('price')
    elif order_by == "name":
        properties = properties.order_by('title')

    # If it's an AJAX (fetch) request, return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        properties_data = [{
            'id': prop.id,
            'title': prop.title,
            'size': prop.size,
            'price': f"{prop.price:,.0f}".replace(',', '.'),
            'rooms': prop.rooms,
            'status': prop.status,
            'image_url': str(prop.image_url),
        } for prop in properties]
        return JsonResponse({'data': properties_data})

    # Otherwise, render the HTML page
    return render(request, "properties/property_listings.html", {
        "properties": properties
    })

def property_details(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, "properties/property_details.html", {
        "property": property
    })
