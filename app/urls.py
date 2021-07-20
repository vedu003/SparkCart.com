from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('',views.ProductView.as_view(),name='home'),

    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('emptycart/', views.empty_cart, name='emptycart'),
    
    path('manageaddress/', views.manageaddress, name='manageaddress'),
    path('delete/<int:id>/', views.delete_address, name='deleteaddress'),
    path('update/<int:id>/', views.update_address, name='updateaddress'),
    path('profile/', views.profile, name='profile'),
    path('manageprofile/<int:id>/', views.manage_profile, name='manageprofile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('camera/', views.camera, name='camera'),
    path('camera/<slug:data>', views.camera, name='cameradata'),
    path('menwatches/', views.menWatches, name='menwatches'),
    path('menwatches/<slug:data>', views.menWatches, name='menwatchdata'),
    path('womenwatches/', views.womenWatches, name='womenwatches'),
    path('womenwatches/<slug:data>', views.womenWatches, name='womenwatchdata'),

    path('mentshirt/', views.mensTshirt, name='mentshirt'),
    path('womentshirt/', views.womensTshirt, name='womentshirt'),
    path('shirt/', views.shirt, name='shirt'),
    path('mjeans/', views.menJeans, name='mjeans'),
    path('wjeans/', views.womenJeans, name='wjeans'),
    path('msuit/', views.menSuit, name='msuit'),
    path('wsaree/', views.womenSaree, name='wsaree'),
    path('wkurti/', views.womenKurti, name='wkurti'),
    path('wtops/', views.womenTops, name='wtops'),
    path('mshoes/', views.menShoes, name='mshoes'),
    path('wshoes/', views.womenShoes, name='wshoes'),
    


    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),

] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
