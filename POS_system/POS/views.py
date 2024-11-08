from django.shortcuts import render, redirect
from .models import Product, CartItem, Order

def product_list(request):
    products = Product.objects.all()
    return render(request, 'pos/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def cart_view(request):
    cart_items = CartItem.objects.all()
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'pos/cart_view.html', {'cart_items': cart_items, 'total': total})

def checkout(request):
    cart_items = CartItem.objects.all()
    if cart_items:
        order = Order.objects.create()
        for item in cart_items:
            order.items.add(item)
        order.calculate_total()
        CartItem.objects.all().delete()  # Clear the cart
    return redirect('order_list')

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'pos/order_list.html', {'orders': orders})
