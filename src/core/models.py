from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name='юзер',
        on_delete=models.CASCADE,
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,
    )
    balance = models.DecimalField(
        verbose_name='баланс',
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'юзер'
        verbose_name_plural = 'юзеры'
