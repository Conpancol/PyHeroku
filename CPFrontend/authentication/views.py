from django.contrib.auth import logout
from django.shortcuts import render, redirect

from common.FrontendTexts import FrontendTexts


view_texts = FrontendTexts('login')


def logout_view(request):
    logout(request)
    return redirect('/auth/login')
