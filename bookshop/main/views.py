from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Book
from django.contrib.auth.decorators import login_required
from accounts.models import CartItem
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST", "GET"])
def user_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect('home')
    
def home(request):
    books = Book.objects.all()
    for book in books:
        book.check_and_update_sale_status()
    query = request.GET.get('query')
    featured_books = Book.objects.all()[:5]
    new_books = Book.objects.all().order_by('-id')[:5]
    on_sale_books = Book.objects.filter(on_sale=True)
    search_results = []

    if query:
        search_results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )

    context = {
        'featured_books': featured_books,
        'new_books': new_books,
        'on_sale_books': on_sale_books,
        'search_results': search_results,
        'query': query
    }
    return render(request, 'main/home.html', context)
    
def landing_page(request):
    books = Book.objects.all()
    for book in books:
        book.check_and_update_sale_status()
    query = request.GET.get('query')
    featured_books = Book.objects.all()[:5]
    new_books = Book.objects.all().order_by('-id')[:5]
    on_sale_books = Book.objects.filter(on_sale=True)
    search_results = []

    if query:
        search_results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )

    context = {
        'featured_books': featured_books,
        'new_books': new_books,
        'on_sale_books': on_sale_books,
        'search_results': search_results,
        'query': query
    }
    return render(request, 'main/landing_page.html', context)
    
def add_to_cart(request, book_id):
    cart = request.session.get('cart', {})
    cart[str(book_id)] = cart.get(str(book_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')
    
def cart_view(request):
    cart = request.session.get('cart', {})
    books = Book.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for book in books:
        quantity = cart[str(book.id)]
        total = book.current_price() * quantity
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'total': total
        })
        total_price += total

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'main/cart.html', context)
    
@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)  # Assuming the cart is user-specific
    total = sum(item.total for item in cart_items)  # Calculate the total price

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'main/checkout.html', context)

@login_required(login_url='login')
def process_checkout(request):
    if 'cart' in request.session:
        del request.session['cart']
        return render(request, 'main/checkout_success.html')
    return render(request, 'main/checkout_success.html') 
    
