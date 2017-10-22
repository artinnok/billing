from django.views.generic import FormView
from django.http import JsonResponse

from core.forms import TransactionForm
from core.models import Profile, Transaction


class IndexView(FormView):
    template_name = 'core/index.html'
    form_class = TransactionForm

    def form_valid(self, form):
        receiver_list = Profile.objects.filter(inn__in=form.cleaned_data['receiver_list'])
        sender = Profile.objects.get(pk=form.cleaned_data['sender'])
        per_receiver_amount = form.cleaned_data['amount'] / receiver_list.count()

        for item in receiver_list:
            sender.balance -= per_receiver_amount
            sender.save()

            Transaction.objects.create(
                sender=sender,
                amount=per_receiver_amount,
                receiver=item,
            )

        return JsonResponse({
            'success': True,
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors,
        },
            status=400,
        )
