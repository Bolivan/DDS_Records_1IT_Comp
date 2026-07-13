from django.db import models
from django.utils import timezone
from directories.models import Status, Type, Category, Subcategory

class CashFlowRecord(models.Model):
    date = models.DateField(
        'Дата создания', 
        default=timezone.now,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name='Тип'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        null=True,  
        blank=True  
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        null=True,  
        blank=True  
    )
    amount = models.DecimalField(
        'Сумма', 
        max_digits=12, 
        decimal_places=2,
        help_text='Сумма в рублях'
    )
    comment = models.TextField('Комментарий', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date} - {self.type.name} - {self.amount} руб."
    
    class Meta:
        verbose_name = 'Запись ДДС'
        verbose_name_plural = 'Записи ДДС'
        ordering = ['-date']