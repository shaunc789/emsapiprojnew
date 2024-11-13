from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
#Create an instance of the DefaultRouter class
router = DefaultRouter()

#Register the mapping for url and views
# r for raw string - to escape special chars
router.register(r'departments',views.DepartmentViewSet)
router.register(r'employees',views.EmployeeViewSet)
router.register(r'users',views.UserViewSet)

#creating uls for login and signup api views
urlpatterns = [
    path("signup/",views.SignupAPIView.as_view(), name="user-signup"),
    path("login/",views.LoginAPIView.as_view(),name="user-login"),
]

#Create the urlpatterns list from thr router urls
urlpatterns += router.urls