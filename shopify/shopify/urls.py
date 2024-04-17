
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include(arg=('shop.urls','shop'), namespace='shop')),
    path('cart/', include(arg=('cart.urls','cart'), namespace='cart')),
    path('account/', include(arg=('account.urls','account'), namespace='account')),
    path('payment/', include(arg=('payment.urls','payment'), namespace='payment')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)