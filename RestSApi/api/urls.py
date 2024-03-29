from django.urls import path,include
from . import customer
from rest_framework.routers import DefaultRouter

router_obj = DefaultRouter()
router_obj.register(r'customer',customer.CustomerViewset)

urlpatterns = [
    path("get_customer_info/",customer.get_info),
    path("create_customer/",customer.get_info),
    path("customer_crud/",customer.CustomerCrud.as_view()),
    path("customer_viewset/",include(router_obj.urls)),
    path("user_register/",customer.register_user),
    path("user_login/",customer.UserCrud.as_view()),
]
