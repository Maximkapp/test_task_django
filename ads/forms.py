from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка на изображение (необязательно)'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('new', 'Новый'),
                ('used', 'Б/у'),
                ('broken', 'Требует ремонта'),
            ]),
        }
        labels = {
            'image_url': 'Ссылка на изображение',
        }

class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'comment']
        widgets = {
            'ad_receiver': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваше предложение...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя из аргументов
        super().__init__(*args, **kwargs)
        if user:
            # Фильтруем объявления: исключаем свои и уже участвующие в предложениях
            self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user).exclude(
                id__in=ExchangeProposal.objects.filter(ad_sender__user=user).values_list('ad_receiver_id', flat=True))