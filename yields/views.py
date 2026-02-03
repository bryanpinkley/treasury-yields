from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from yields.behaviors import get_yield_data
from yields.constants import TERM_CHOICES
from yields.models import Order


def yield_curve(request):
    """
    A function-based view to render the yield curve page with current yield data.
    """
    data = get_yield_data()
    date = data["date"]
    context = {"date": date, "data": data}
    return render(request, "yield_curve.html", context)


class OrderCreateView(generic.CreateView):
    """
    A class-based view to create new order instances.
    """
    model = Order
    fields = ["term", "amount"]
    template_name = "order_form.html"
    success_url = reverse_lazy("yields:yield_curve")

    def get_context_data(self, **kwargs):
        """
        This method is called before rendering the form.
        """
        context = super().get_context_data(**kwargs)

        data = get_yield_data()
        rates_by_term_value = {}

        for term_value, term_label in TERM_CHOICES.items():
            rates_by_term_value[str(term_value)] = data.get(term_label)

        context["yield_date"] = data.get("date")
        context["rates_by_term_value"] = rates_by_term_value
        return context

    def form_valid(self, form):
        """
        This method is called when a valid form is submitted.
        """
        # Get the object before saving to DB.
        order = form.save(commit=False)

        # Attach user to order instance. If the requesting user is anonymous, we sub in the superuser for now.
        if not self.request.user.is_authenticated:
            order.user = User.objects.get(id=1)
        else:
            order.user = self.request.user

        # Save the rate associated with the term.
        data = get_yield_data()
        term = TERM_CHOICES[order.term]
        order.rate = data[term]

        # Save order object to DB.
        order.save()

        return super().form_valid(form)


class OrderListView(generic.ListView):
    """
    A class-based view to view all Order instances.
    """
    template_name = "order_list.html"
    model = Order

    def get_queryset(self):
        """Gets all Order instances for the table."""
        return Order.objects.all().order_by("-submitted_time")
