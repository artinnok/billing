from django.views.generic import FormView

from core.forms import TransactionForm


class IndexView(FormView):
    template_name = 'core/index.html'
    form_class = TransactionForm
