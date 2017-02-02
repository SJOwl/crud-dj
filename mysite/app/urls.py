from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign_up$', views.sign_up, name='sign_up'),
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^log_out$', views.log_out, name='log_out'),
    # url(r'^sign_problems$', views.sign_in, name='sign_problems$'),
    url(r'^products$', views.products, name='products'),
    url(r'^products/add$', views.add_product, name='add_product'),
    url(r'^products/save$', views.save_product, name='save_product'),
    url(r'^products/edit/([0-9]+)$', views.edit_product, name='edit_product'),
    url(r'^products/remove/([0-9]+)$', views.remove_product, name='remove_product'),
]
