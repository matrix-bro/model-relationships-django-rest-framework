from django.urls import path

from app.views import AllAuthorView, AllPassportView, AllPersonView

urlpatterns = [
    path('person/', AllPersonView.as_view(), name='person-list'),
    path('passports/', AllPassportView.as_view(), name='passport-list'),

    path('authors/', AllAuthorView.as_view(), name='author-list'),
]
