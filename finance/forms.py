from django import forms
from django.forms import ModelForm
from finance.models import PaymentRequest, AdvanceRequest, VoucherRequest


class VoucherForm(ModelForm):
    class Meta:
        model = VoucherRequest
        fields = ['amount', 'purpose']


class PaymentForm(ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['amount', 'purpose']
        

class AdvanceForm(ModelForm):
    class Meta:
        model = AdvanceRequest
        fields = ['amount', 'purpose']
    