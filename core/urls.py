from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('stock/', views.stock_view, name='stock'),
    path('about/', views.about_view, name='about'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:medicine_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('create-order/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
]