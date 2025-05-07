from django.shortcuts import render
from accounts.models import Book

def home(request):
    return render(request, 'main/home.html')

def landing_page(request):
    featured_books = Book.objects.all()[:5]
    new_books = Book.objects.all().order_by('-id')[:5]
    on_sale_books = Book.objects.filter(on_sale=True)

    context = {
        'featured_books': featured_books,
        'new_books': new_books,
        'on_sale_books': on_sale_books
    }
    return render(request, 'main/landing_page.html', context)
