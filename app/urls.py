from django.urls import path
from app.api.author import AllAuthorView
from app.api.book import AllBookView
from app.api.course import AllCourseView
from app.api.passport import AllPassportView
from app.api.person import AllPersonView
from app.api.student import AllStudentView


urlpatterns = [
    path('person/', AllPersonView.as_view(), name='person'),
    path('passport/', AllPassportView.as_view(), name='passport'),

    path('author/', AllAuthorView.as_view(), name='author'),
    path('book/', AllBookView.as_view(), name='book'),

    path('course/', AllCourseView.as_view(), name='course'),
    path('student/', AllStudentView.as_view(), name='student'),
]
