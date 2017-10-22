from django import forms

from core.models import Profile


class TransactionForm(forms.Form):
    sender = forms.MultipleChoiceField(
        choices=Profile.objects.all().values_list('inn', flat=True),
    )
    receiver_list = forms.CharField()
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
