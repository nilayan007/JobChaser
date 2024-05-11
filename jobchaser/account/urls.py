
from django.urls import path, include
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView, UserProfileUpdateView, UserRegistrationView,UserLoginView,UserProfileView,AlgorithmView,FindAlgorithmView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(),name='chnagepassword'),
    path('send-reset-password/', SendPasswordResetEmailView.as_view(),name='send-reset-passwordemail'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(),name='reset-password'),
    path('algorithmview/', AlgorithmView.as_view(),name='algoview'),
    path('findbysearchalgorithm/', FindAlgorithmView.as_view(),name='findalgoview'),
    path('userprofileupdate/', UserProfileUpdateView.as_view(),name='profileupdate'),
]
