from django.db import models
from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


class ProfileManager(models.Manager):
    def create_user(self, username, email, password, **kwargs):
        user = USER_MODEL.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        return self.create(
            user=user,
            **kwargs,
        )


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name='юзер',
        on_delete=models.CASCADE,
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        blank=True,
    )
    balance = models.DecimalField(
        verbose_name='баланс',
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    objects = ProfileManager()

    class Meta:
        verbose_name = 'юзер'
        verbose_name_plural = 'юзеры'
        ordering = ['pk']

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    sender = models.ForeignKey(
        'core.Profile',
        verbose_name='отправитель',
        related_name='sent_transaction_list',
    )
    amount = models.DecimalField(
        verbose_name='сумма',
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    receiver = models.ForeignKey(
        'core.Profile',
        verbose_name='получатель',
        related_name='received_transaction_list',
    )

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'

    def __str__(self):
        return 'Перевод от {sender} {receiver} в размере {amount}'.format(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
        )
