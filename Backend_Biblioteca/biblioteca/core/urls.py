from django.urls import path
from . import views
urlpatterns = [
 path('livros/', views.LivroList.as_view(), name='livros-list'),
 path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livrodetail'),
]