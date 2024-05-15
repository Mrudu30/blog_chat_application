from django.urls import path
from . import views as v

# accounts/ urls.
urlpatterns = [
    path('sign-up/',v.signup_view,name='signup_account'),
    path('',v.login_view,name='login_account'),
    path('logout/',v.logout_view,name='logout_account'),
    path("edit_profile/", v.edit_profile, name="edit_profile")
]
