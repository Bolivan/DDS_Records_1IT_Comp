from django import forms
from .models import CashFlowRecord
from directories.models import Category, Subcategory

class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].required = False
        self.fields['subcategory'].required = False
        
        
        if self.instance and self.instance.pk and self.instance.type:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
            if self.instance.category:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
    
    def clean(self):
        cleaned_data = super().clean()
        type_obj = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        
        
        if type_obj and type_obj.name == "Списание":
            if not category:
                self.add_error('category', 'Для типа "Списание" категория обязательна')
            if not subcategory:
                self.add_error('subcategory', 'Для типа "Списание" подкатегория обязательна')
        
        
        if category and type_obj:
            if category.type != type_obj:
                self.add_error('category', 'Выбранная категория не относится к выбранному типу')
        
        
        if category and subcategory:
            if subcategory.category != category:
                self.add_error('subcategory', 'Подкатегория не принадлежит выбранной категории')
        
        return cleaned_data