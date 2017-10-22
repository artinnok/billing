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
