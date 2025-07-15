from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Подробное описание товара'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg (необязательно)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'  # Обратите внимание на form-select вместо form-control
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'image_url': 'Ссылка на изображение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем choices для поля category из модели
        self.fields['category'].choices = Ad.CATEGORY_CHOICES
        # Определяем choices для поля condition
        self.fields['condition'].choices = [
            ('new', 'Новый'),
            ('used', 'Б/у'),
            ('broken', 'Требует ремонта'),
        ]

class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        ad_sender = cleaned_data.get('ad_sender')

        if not self.user:
            raise forms.ValidationError('Пользователь не авторизован.')

        if not ad_sender:
            raise forms.ValidationError('Выберите объявление.')

        if ad_sender.user != self.user:
            raise forms.ValidationError('Можно использовать только свои объявления для обмена.')

        return cleaned_data


