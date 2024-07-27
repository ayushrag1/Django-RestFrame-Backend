from datetime import datetime

from django.db import models


def get_contract_path(instance, filename, **kwargs):
    curr_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conract_{curr_datetime}_{filename}" if filename else f"conract_{curr_datetime}"
    return filename


class ContractPDF(models.Model):
    ALLOWED_TYPES = ['pdf']  # Update allowed types as needed
    image = models.ImageField(upload_to=get_contract_path, null=False)
    filename = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename or 'Unnamed Contract'
