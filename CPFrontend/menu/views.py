from django.shortcuts import render
from django.shortcuts import redirect

from common.FrontendTexts import FrontendTexts


def menu(request):
    menu_texts = FrontendTexts('menu')
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    else:
        return render(request, 'menu/menu.html', {'menu_text': menu_texts.getComponent()})
