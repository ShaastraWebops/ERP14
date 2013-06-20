from django.contrib import admin
from dept.models import Dept, Subdept


class SubdeptInline(admin.TabularInline):
    model=Subdept

class DeptAdmin(admin.ModelAdmin):
    inlines=[SubdeptInline,]


admin.site.register(Dept, DeptAdmin)