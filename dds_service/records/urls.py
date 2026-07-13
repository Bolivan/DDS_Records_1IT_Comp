from django.urls import path
from . import views

app_name = 'records' 

urlpatterns = [
    path('', views.RecordListView.as_view(), name='record_list'),
    path('create/', views.RecordCreateView.as_view(), name='record_create'),
    path('<int:pk>/edit/', views.RecordUpdateView.as_view(), name='record_update'),
    path('<int:pk>/delete/', views.RecordDeleteView.as_view(), name='record_delete'),
    path('ajax/get-categories/', views.get_categories_by_type, name='get_categories'),
    path('ajax/get-subcategories/', views.get_subcategories_by_category, name='get_subcategories'),
]