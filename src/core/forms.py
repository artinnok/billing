from django import forms

from core.models import Profile


class TransactionForm(forms.Form):
    sender = forms.MultipleChoiceField(
        choices=list(Profile.objects.all().values_list('user', 'inn')),
        label='Отправитель',
    )
    receiver_list = forms.CharField(
        label='Список получателей',
        help_text='Через запятую'
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Сумма перевода',
        help_text='С точностью до 2 знаков',
    )

    def clean_receiver_list(self, *args, **kwargs):
        receiver_list = self.cleaned_data['receiver_list'].split(',')

        return [item for item in receiver_list if item]

