from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import ProtectedError
from .models import Status, Type, Category, Subcategory
from .forms import StatusForm, TypeForm, CategoryForm, SubcategoryForm

# Статусы Statuses
class StatusListView(ListView):
    model = Status
    template_name = 'directories/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'directories/status_form.html'
    success_url = reverse_lazy('directories:status_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Статус "{form.instance.name}" успешно создан')
        return super().form_valid(form)

class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'directories/status_form.html'
    success_url = reverse_lazy('directories:status_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Статус "{form.instance.name}" успешно обновлен')
        return super().form_valid(form)

class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'directories/status_confirm_delete.html'
    success_url = reverse_lazy('directories:status_list')
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить статус, так как он используется в записях')
            return redirect('directories:status_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Статус "{self.get_object().name}" успешно удален')
        return super().delete(request, *args, **kwargs)

# Типы Types
class TypeListView(ListView):
    model = Type
    template_name = 'directories/type_list.html'
    context_object_name = 'types'

class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm
    template_name = 'directories/type_form.html'
    success_url = reverse_lazy('directories:type_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Тип "{form.instance.name}" успешно создан')
        return super().form_valid(form)

class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'directories/type_form.html'
    success_url = reverse_lazy('directories:type_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Тип "{form.instance.name}" успешно обновлен')
        return super().form_valid(form)

class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'directories/type_confirm_delete.html'
    success_url = reverse_lazy('directories:type_list')
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить тип, так как он используется в записях или имеет связанные категории')
            return redirect('directories:type_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Тип "{self.get_object().name}" успешно удален')
        return super().delete(request, *args, **kwargs)

# Категории Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'directories/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.select_related('type').all()

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'directories/category_form.html'
    success_url = reverse_lazy('directories:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Категория "{form.instance.name}" успешно создана для типа "{form.instance.type.name}"')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании категории. Проверьте правильность заполнения.')
        return super().form_invalid(form)

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'directories/category_form.html'
    success_url = reverse_lazy('directories:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Категория "{form.instance.name}" успешно обновлена')
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'directories/category_confirm_delete.html'
    success_url = reverse_lazy('directories:category_list')
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить категорию, так как она используется в записях или имеет связанные подкатегории')
            return redirect('directories:category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Категория "{self.get_object().name}" успешно удалена')
        return super().delete(request, *args, **kwargs)



# Подкатегории Subcategories
class SubcategoryListView(ListView):
    model = Subcategory
    template_name = 'directories/subcategory_list.html'
    context_object_name = 'subcategories'
    
    def get_queryset(self):
        return Subcategory.objects.select_related('category', 'category__type').all()

class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'directories/subcategory_form.html'
    success_url = reverse_lazy('directories:subcategory_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Подкатегория "{form.instance.name}" успешно создана для категории "{form.instance.category.name}"')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании подкатегории. Проверьте правильность заполнения.')
        return super().form_invalid(form)

class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'directories/subcategory_form.html'
    success_url = reverse_lazy('directories:subcategory_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Подкатегория "{form.instance.name}" успешно обновлена')
        return super().form_valid(form)

class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    template_name = 'directories/subcategory_confirm_delete.html'
    success_url = reverse_lazy('directories:subcategory_list')
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить подкатегорию, так как она используется в записях')
            return redirect('directories:subcategory_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Подкатегория "{self.get_object().name}" успешно удалена')
        return super().delete(request, *args, **kwargs)