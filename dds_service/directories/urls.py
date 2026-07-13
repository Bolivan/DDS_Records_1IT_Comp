from django.urls import path
from . import views

app_name = 'directories'

urlpatterns = [
    #Statuses
    path('statuses/', views.StatusListView.as_view(), name='status_list'),
    path('statuses/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    #Types
    path('types/', views.TypeListView.as_view(), name='type_list'),
    path('types/create/', views.TypeCreateView.as_view(), name='type_create'),
    path('types/<int:pk>/edit/', views.TypeUpdateView.as_view(), name='type_update'),
    path('types/<int:pk>/delete/', views.TypeDeleteView.as_view(), name='type_delete'),
    #Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    #Subcategories
    path('subcategories/', views.SubcategoryListView.as_view(), name='subcategory_list'),
    path('subcategories/create/', views.SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategories/<int:pk>/edit/', views.SubcategoryUpdateView.as_view(), name='subcategory_update'),
    path('subcategories/<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]