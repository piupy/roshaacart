
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('contact', views.contact),
    path('product/<int:myid>', views.product),
	path('checkout', views.checkout),
	path('tracker', views.tracker),
	path('handlerequest',views.handlerequest),
	path('search', views.search),
]
