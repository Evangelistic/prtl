from django.shortcuts import render
from django.conf import settings


# Create your views here.
def choose_view(request, name_views):
    print(name_views)
    return name_views(request)


def index(request):
    return render(request, 'portal/index.html', {'title': 'Security portal'})


def error404(request):
    return render(request, 'portal/404.html', {'title': '404'})


def about_us(request):
    return render(request, 'portal/about-us.html', {'title': 'About security'})


def base(request):
    return render(request, 'portal/base.html', {})


def blog(request):
    return render(request, 'portal/blog.html', {'title': 'Security blog'})


def blog_item(request):
    return render(request, 'portal/blog-item.html', {})


def contact_us(request):
    return render(request, 'portal/contact-us.html', {
        'title': 'Security contacts',
        'company_map': settings.COMPANY_MAP,
        'company_info': settings.COMPANY_INFO
    })


def portfolio(request):
    return render(request, 'portal/portfolio.html', {'title': 'Portfolio'})


def pricing(request):
    return render(request, 'portal/pricing.html', {'title': 'Pricing'})


def services(request):
    return render(request, 'portal/services.html', {'title': 'Security services'})


def shortcodes(request):
    return render(request, 'portal/shortcodes.html', {'title': 'Shortcodes'})
