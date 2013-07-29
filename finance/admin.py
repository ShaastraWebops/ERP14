from django.contrib import admin
from finance.models import Vendor, VoucherRequest, AdvanceRequest, FinUniqueID, PaymentRequest

admin.site.register(Vendor)
admin.site.register(VoucherRequest)
admin.site.register(AdvanceRequest)
admin.site.register(PaymentRequest)
admin.site.register(FinUniqueID)
