from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path("chapter/", views.VggtChapterList.as_view()),
    path("chapter/<int:pk>/", views.VggtChapterDetail.as_view()),

    path("article/", views.VggtArticleList.as_view()),
    path("article/<int:pk>/", views.VggtArticleDetail.as_view()),

    path("variable/", views.VggtVariableList.as_view()),
    path("variable/<int:pk>/", views.VggtVariableDetail.as_view()),

    path("score/", views.DealScoreList.as_view()),
    path("score/<int:pk>/", views.DealScoreDetail.as_view()),

    path("score/variable/", views.DealVariableList.as_view()),
    path("score/variaable/<int:pk>/", views.DealVariableDetail.as_view()),
]