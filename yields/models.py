from django.contrib.auth.models import User
from django.db import models

from yields.constants import TERM_CHOICES


class Order(models.Model):
    """
    The table that stores objects representing orders submissions. Orders are specific to certain terms (months),
    amounts (dollars), and yield rates (percentages). User is a foreign key to the Django User model. Submitted time
    is automatically set to the current time when the order object is created.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    rate = models.DecimalField(max_digits=1000, decimal_places=2)
    submitted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount_in_dollars} for {self.term_m_y} at {self.rate_in_percent}"

    @property
    def term_m_y(self):
        """Return the term in human-readable months or years, instead of just months"""
        return TERM_CHOICES[self.term]

    @property
    def amount_in_dollars(self):
        """Return the amount in a dollar string"""
        return f"${self.amount}"

    @property
    def rate_in_percent(self):
        """Return the rate in a percentage string"""
        return f"{self.rate}%"
