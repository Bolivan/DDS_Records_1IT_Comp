from django.http import JsonResponse
from directories.models import Category, Subcategory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CashFlowRecord
from .forms import CashFlowRecordForm

class RecordListView(ListView):
    model = CashFlowRecord
    template_name = 'records/record_list.html'
    context_object_name = 'records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        type = self.request.GET.get('type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status:
            queryset = queryset.filter(status_id=status)
        if type:
            queryset = queryset.filter(type_id=type)
        if category:
            queryset = queryset.filter(category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from directories.models import Status, Type, Category, Subcategory
        
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['filters'] = self.request.GET
        
        return context

class RecordCreateView(CreateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('records:record_list')
    
    def get_initial(self):
        """Устанавливаем начальные значения для полей"""
        initial = super().get_initial()
        from django.utils import timezone
        initial['date'] = timezone.now().date()
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from directories.models import Category, Subcategory
        context['all_categories'] = Category.objects.all()
        context['all_subcategories'] = Subcategory.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно создана')
        return super().form_valid(form)

class RecordUpdateView(UpdateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('records:record_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена')
        return super().form_valid(form)

class RecordDeleteView(DeleteView):
    model = CashFlowRecord
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('records:record_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена')
        return super().delete(request, *args, **kwargs)

def get_categories_by_type(request):
    """Возвращает категории для выбранного типа"""
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)

def get_subcategories_by_category(request):
    """Возвращает подкатегории для выбранной категории"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)