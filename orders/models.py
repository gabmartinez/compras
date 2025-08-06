from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    def __str__(self):
        return self.name


class Brand(models.Model):
    description = models.CharField(
        max_length=150, unique=True, verbose_name=_("Description")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    def __str__(self):
        return self.description


class UnitMeasure(models.Model):
    description = models.CharField(
        max_length=150, unique=True, verbose_name=_("Description")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    def __str__(self):
        return self.description


class PersonType(models.TextChoices):
    JURIDICAL = "JURIDICAL", _("Juridical")
    PHYSICAL = "PHYSICAL", _("Physical")


class Provider(models.Model):
    document_number = models.CharField(
        max_length=15, unique=True, verbose_name=_("Document Number")
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    person_type = models.CharField(
        max_length=15,
        choices=PersonType.choices,
        default=PersonType.JURIDICAL,
        verbose_name=_("Person Type"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    def __str__(self):
        return self.name


class Article(models.Model):
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name=_("Brand"),
    )
    unit_measure = models.ForeignKey(
        UnitMeasure,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name=_("Unit of Measure"),
    )
    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"))
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    def __str__(self):
        return self.description


class Order(models.Model):
    order_number = models.CharField(
        max_length=45, unique=True, verbose_name=_("Order Number")
    )
    order_date = models.DateField(verbose_name=_("Order Date"))
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Provider"),
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Article"),
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    unit_measure = models.ForeignKey(
        UnitMeasure,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Unit of Measure"),
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
        default=0.00,
        validators=[MinValueValidator(0)],
    )
    accounting_entry_number = models.CharField(
        max_length=75,
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("Accounting Entry Number"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity


class UnpublishedOrder(Order):
    class Meta:
        verbose_name = _("Unpublished Order")
        verbose_name_plural = _("Unpublished Orders")
        proxy = True

    def __str__(self):
        return f"Unpublished Order #{self.id}"
