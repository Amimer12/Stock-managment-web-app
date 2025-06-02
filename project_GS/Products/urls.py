from django.urls import path
from . import views

urlpatterns = [
    path('get-product-price/<int:variant_id>/', views.get_product_price, name='get_product_price'),
]