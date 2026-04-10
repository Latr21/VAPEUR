from django.shortcuts import render, redirect
from django.contrib import messages
from .services.auth_service import AuthService

def home_view(request):
    # Mock games for the Steam-like library
    games = [
        {"id": 1, "title": "Cyberpunk 2077", "price": "59.99€", "image": "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?auto=format&fit=crop&q=80&w=400&h=250"},
        {"id": 2, "title": "Elden Ring", "price": "49.99€", "image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=400&h=250"},
        {"id": 3, "title": "The Witcher 3", "price": "29.99€", "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400&h=250"},
        {"id": 4, "title": "Hades II", "price": "24.99€", "image": "https://images.unsplash.com/photo-1542751110-97427bbecf20?auto=format&fit=crop&q=80&w=400&h=250"},
        {"id": 5, "title": "Red Dead Redemption 2", "price": "59.99€", "image": "https://images.unsplash.com/photo-1543332164-6e82f355badc?auto=format&fit=crop&q=80&w=400&h=250"},
        {"id": 6, "title": "Baldur's Gate 3", "price": "59.99€", "image": "https://images.unsplash.com/photo-1614027164847-1b2801438990?auto=format&fit=crop&q=80&w=400&h=250"},
    ]
    return render(request, 'gamestore/home.html', {'games': games})

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        success, user = AuthService.login_user(request, u, p)
        if success:
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'gamestore/login.html')

def signup_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        try:
            AuthService.register_user(u, e, p)
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
        except Exception as ex:
            messages.error(request, str(ex))
    return render(request, 'gamestore/signup.html')

def logout_view(request):
    AuthService.logout_user(request)
    messages.info(request, "Logged out.")
    return redirect('home')
