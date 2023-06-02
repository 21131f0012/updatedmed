from django.urls import path

from . import views

urlpatterns=[
    #path("",views.home,name="home"),
    path("",views.prod,name="prod"),
    path("expi/",views.tim,name="expi"),
    path("product_detail",views.product_detail,name="product_detail"),
    path('expi/<int:id>/delete',views.delet,name="delet"),
    path('<int:id>/update',views.update,name="update"),
    path("expiring_products",views.expiring_products,name="expiring_products"),
    path("expiring_soon",views.expiring_soon,name="expiring_soon"),
    path("exp_60",views.exp_60,name="exp_60"),
    path("product_search",views.product_search,name="product_search"),
    path('orderby',views.ordered,name="orderby"),
    path('order',views.order,name="order"),
    path("bill",views.bill,name="bill"),
    path("success",views.success,name="success"),
    path('again', views.search_jav, name='search'),
    path('newpage', views.newpage, name='newpage'),
    path('nextpage', views.nextpage, name='nextpage'),
    path('submit_form',views.submit_form,name="bill"),

    path('add_medicine',views.insertbysupplier,name="add_medicine")
    

]