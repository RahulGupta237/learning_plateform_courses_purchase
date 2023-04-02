"""learning_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import user_login, views
from django.conf import settings
from django.conf.urls.static import static

#Mahakaal@237
urlpatterns = [
    path("admin/", admin.site.urls),
    path("base",views.base,name='base'),
    path('',views.Home,name='home'),
    path('courses',views.SingleCourse,name='single_course'),
    path('my_course',views.MY_COURSE,name='my_course'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('search',views.SEARCH_COURSE,name='search_course'),
    path('course/<slug:slug>',views.course_detail,name='course_detail'),
    path('404',views.page_not_found,name='404'),
    path('contact',views.ContactUs,name='contact_us'),
    path('about',views.AboutUs,name='about_us'),
    path('accounts/register',user_login.Register,name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dologin',user_login.DOLOGIN,name='dologin'),
    path('accounts/profile',user_login.Profile,name='profile'),
    path('accounts/profile/update',user_login.Profile_Update,name='profile_update'),
    path('checkout/<slug:slug>',views.course_checkout,name='checkout'),
    path('verify_payment',views.VerifyPayment,name="verify_payment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

