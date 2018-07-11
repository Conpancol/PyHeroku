from django.shortcuts import render
from django.shortcuts import redirect


def menu(request):

    if not request.user.is_authenticated:
        return redirect('/auth/login')
    else:
        return render(request, 'menu/menu.html')
