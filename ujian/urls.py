from django.urls import path
from .views import *

urlpatterns = [
    path('', ujian_list, name="ujian_list"),
    path('<int:pk>/', ujian_detail, name="ujian_detail"),
    path('<int:pk>/take/<int:question_id>/', ujian_take, name='ujian_take'), 
    path('<int:pk>/result/', ujian_result, name='ujian_result'),  
    path('<int:pk>/reset/', ujian_reset, name='ujian_reset'),

]
