from django.db import models
from django.core.exceptions import ValidationError


class Status(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    type = models.ForeignKey(
        Type,  
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип'
    )
    
    class Meta:
        
        unique_together = ['name', 'type']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def clean(self):
        
        if Category.objects.filter(name=self.name, type=self.type).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Категория "{self.name}" уже существует для типа "{self.type.name}"'
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    name = models.CharField('Название', max_length=50)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )
    
    class Meta:
        
        unique_together = ['name', 'category']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
    
    def clean(self):
        
        if Subcategory.objects.filter(name=self.name, category=self.category).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Подкатегория "{self.name}" уже существует для категории "{self.category.name}"'
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"