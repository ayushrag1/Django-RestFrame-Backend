from django.contrib import admin

from base.models import ContractPDF


class ContractPDFAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_at')
    search_fields = ('filename',)
    list_filter = ('uploaded_at',)


# Register your admin class with the associated model
admin.site.register(ContractPDF, ContractPDFAdmin)
