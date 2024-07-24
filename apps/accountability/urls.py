from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("", views.index, name="index"),

    path("chapter/", views.VggtChapterList.as_view()),
    path("chapter/<int:pk>/", views.VggtChapterDetail.as_view()),

    path("article/", views.VggtArticleList.as_view()),
    path("article/<int:pk>/", views.VggtArticleDetail.as_view()),

    path("variable/", views.VggtVariableList.as_view()),
    path("variable/<int:pk>/", views.VggtVariableDetail.as_view()),

    path("deal/", views.DealScoreList.as_view({'get':'list'})),
    path("deal/<int:pk>/", views.DealScoreDetail.as_view()),

    # path("deal/variable/", views.DealVariableList.as_view()),
    # path("deal/variable/<int:pk>/", views.DealVariableDetail.as_view()),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]