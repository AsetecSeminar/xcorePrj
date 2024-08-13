from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('abc-analysis/', views.abc_analysis, name='abc_analysis'),
]
