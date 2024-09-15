from django.urls import path
from .views import UserRegisterView, UserLoginView, ContactListView, MarkSpamView, SearchView, CheckSpamView, DetailedSearchView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('mark-spam/<str:phone_number>/', MarkSpamView.as_view(), name='mark_spam'),
    path('check-spam/<str:phone_number>/', CheckSpamView.as_view(), name='check_spam'),
    path('search/', SearchView.as_view(), name='search'),
    path('search_details/<str:phone_number>/', DetailedSearchView.as_view(), name='search_details'),
]
