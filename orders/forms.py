from django import forms

from orders.utils import (
    physical_document_number_validator,
    juridical_document_number_validator,
)
from orders import models
from django.utils.translation import gettext as _


class ProviderForm(forms.ModelForm):
    class Meta:
        model = models.Provider
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data["person_type"]
        document_number = cleaned_data["document_number"]
        if (
            person_type == models.PersonType.PHYSICAL
            and not physical_document_number_validator(document_number)
        ):
            raise forms.ValidationError(_("The document number is invalid."))
        elif (
            person_type == models.PersonType.JURIDICAL
            and not juridical_document_number_validator(document_number)
        ):
            raise forms.ValidationError(_("The document number is invalid."))
        return cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        article = cleaned_data.get("article")

        if quantity <= 0:
            raise forms.ValidationError(_("The quantity must be greater than zero."))

        if quantity and article:
            if quantity > article.stock:
                raise forms.ValidationError(
                    _("The quantity cannot exceed the available stock.")
                )
        return cleaned_data
