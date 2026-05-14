"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from payment import views as payment_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    # Include payment URLs at root so legacy/unprefixed reverses work in tests
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Legacy/unprefixed payment URL names (some tests expect these names without the 'payment:' namespace)
urlpatterns += [
    path('checkout/', payment_views.checkout, name='checkout'),
    path('process/', payment_views.process_payment, name='process_payment'),
    path('success/<int:order_id>/', payment_views.payment_success, name='payment_success'),
    path('failed/', payment_views.payment_failed, name='payment_failed'),
    path('orders/', payment_views.order_history, name='order_history'),
    path('order/<int:order_id>/', payment_views.order_detail, name='order_detail'),
]
