from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('customers/', views.customer_list, name='customer_list'),

    path('customers/add/', views.add_customer, name='add_customer'),

    path('customers/edit/<int:pk>/',
         views.edit_customer,
         name='edit_customer'),

    path('customers/delete/<int:pk>/', views.delete_customer,
         name='delete_customer'),  

    path(
        'orders/',
        views.order_list,
        name='order_list'
    ),

    path(
        'orders/add/',
        views.add_order,
        name='add_order'
   ),
    path(
       'orders/edit/<int:pk>/',
       views.edit_order,
       name='edit_order'
   ),
   path(
       'orders/delete/<int:pk>/',
       views.delete_order,
       name='delete_order'
   ),
   path(
     'services/',
     views.service_list,
     name='service_list'
   ), 
  path(
    'services/add/',
    views.add_service,
    name='add_service'
  ),
  path(
    'services/edit/<int:pk>/',
    views.edit_service,
    name='edit_service'
 ),
path(
    'services/delete/<int:pk>/',
    views.delete_service,
    name='delete_service'
),
# =========================
# PAYMENTS
# =========================

path(
    'payments/',
    views.payment_list,
    name='payment_list'
),

path(
    'payments/<int:pk>/receipt/',
    views.payment_receipt,
    name='receipt'
),

path(
    'payments/add/',
    views.add_payment,
    name='add_payment'
),

path(
    'payments/edit/<int:pk>/',
    views.edit_payment,
    name='edit_payment'
),

path(
    'payments/delete/<int:pk>/',
    views.delete_payment,
    name='delete_payment'
),

path('reports/', views.reports, name='reports'),

path('settings/', views.settings_page, name='settings'),

path('logout/', views.logout_view, name='logout'),

path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='laundry/login.html'
    ),
    name='login'
),
path(
    'logout/',
    auth_views.LogoutView.as_view(),
    name='logout'
),


]
