from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'),
        ('furniture', 'Мебель'),
        ('home_appliances', 'Бытовая техника'),
        ('sport', 'Спорт/Отдых'),
        ('children', 'Детские товары'),
        ('auto', 'Автотовары'),
        ('tools', 'Инструменты'),
        ('cosmetics', 'Косметика/Уход'),
        ('art', 'Искусство/Хобби'),
        ('collectibles', 'Коллекционные предметы'),
        ('musical', 'Музыкальные инструменты'),
        ('plants', 'Растения'),
        ('pet_supplies', 'Товары для животных'),
        ('services', 'Услуги'),
        ('real_estate', 'Недвижимость'),
        ('other', 'Другое')  # Всегда оставляем "Другое" в конце
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обмен от {self.ad_sender.user} к {self.ad_receiver.user}"
