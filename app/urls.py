from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='home'),
    path('login/', login, name='login'),
    # path('register/',register,name = "register"),
    path('about/',about,name = "about"),
    path('contact/',contact,name = "contact"),
    path('service/',service,name = "service"),
    path('product/',product,name = "product"),
    path('product_list/',products_list,name = "products_list"),
    path('sum_view', sum_view, name='sum_view'),
    path('add_contact_detail',add_contact_detail,name='add_contact_detail'),
    path('show_product/<int:product_id>/',show_product,name='show_product'),
    path('add_inquiry', add_inquiry, name='add_inquiry'),
    path('register/', register_view, name='register'),
    path('logout', logout, name='logout'),
    path('admin/login', admin_login, name='admin_login'),
    path('admin/dashboard',dashboard,name='dashboard'),
    path('feedback/', submit_feedback, name='feedback'),
    path('admin/user/', user_list, name='user_list'),
    path('admin/users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('admin/products/', product_list, name='product_list'),
    path('admin/products/detail/<int:pk>/', product_detail, name='product_detail'),
    path('admin/products/delete/<int:pk>/', delete_product, name='product_delete'),
    path('admin/product/add/', store_product, name='add_product'),
    path('admin/product/update/<int:pk>/', update_product, name='product_update'),
    path('admin/inquiries/', inquiry_list, name='inquiry_list'),
    path('admin/inquiries/delete/<int:pk>/', delete_inquiry, name='delete_inquiry'),
    path('admin/feedback/', feedback_list, name='feedback_list'),
    path('admin/feedback/delete/<int:feedback_id>/', delete_feedback, name='delete_feedback')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)