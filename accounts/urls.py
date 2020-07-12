from django.urls import path, include
import accounts.views as account_views


urlpatterns = [
    path('signup/', account_views.SignupView.as_view(),
         name="accounts-signup"),
    path('login/', account_views.LoginView.as_view(), name="accounts-login"),
    path('isloggedin/',
         account_views.IsLoggedInView.as_view(),
         name='accounts-isloggedin'),
    path('ispaiduser/',
         account_views.IsPaidUserView.as_view(),
         name='accounts-ispaiduser'),
    path('reset-password/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
]
