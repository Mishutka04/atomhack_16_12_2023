from django.urls import path
from .views import GenerateAnswerView


app_name = "atom_mvp"


urlpatterns = [
    path(
        'generate-answer/',
        GenerateAnswerView.as_view(),
        name='generate-answer'),
]
