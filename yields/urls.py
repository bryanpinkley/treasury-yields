from django.urls import path

from . import views

app_name = "yields"
urlpatterns = [
    path("", views.yield_curve, name="yield_curve"),
    path("order/", views.OrderCreateView.as_view(), name="order"),
    path("history/", views.OrderListView.as_view(), name="history")
]
