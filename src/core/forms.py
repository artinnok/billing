from django import forms

from core.models import Profile


def get_sender_choices():
    return list(Profile.objects.all().values_list('pk', 'inn'))


class TransactionForm(forms.Form):
    sender = forms.ChoiceField(
        label='Отправитель',
        help_text='Выберите ИНН отправителя',
        choices=get_sender_choices,
    )
    receiver_list = forms.CharField(
        label='Список получателей',
        help_text='Укажите ИНН получателей через запятую',
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Сумма перевода',
        help_text='С точностью до 2 знаков',
    )

    def clean_receiver_list(self):
        try:
            receiver_list = self.cleaned_data['receiver_list'].split(',')

            receiver_list = set([item for item in receiver_list if item])

            rel_receiver_list = set(Profile.objects.filter(inn__in=receiver_list).values_list('inn', flat=True))

            substract = receiver_list - rel_receiver_list

            if substract == set():
                return receiver_list

            raise forms.ValidationError(
                message='Users with this INN {} not found'.format(list(substract)),
                code='some_users_not_found',
            )

        except KeyError:
            pass

    def clean(self):
        try:
            profile = Profile.objects.get(pk=self.cleaned_data['sender'])

            if profile.balance < self.cleaned_data['amount']:
                raise forms.ValidationError(
                    message='Not enough funds',
                    code='not_enough_funds',
                )

            return self.cleaned_data

        except Profile.DoesNotExist:
            raise forms.ValidationError(
                message='Profile not found',
                code='profile_not_found',
            )

        except KeyError:
            pass
