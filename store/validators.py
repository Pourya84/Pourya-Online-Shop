from django.core.exceptions import ValidationError


def validate_product_price(value):

    if value <= 0:

        raise ValidationError(
            "Price must be greater than zero."
        )

    if value > 1000000000:

        raise ValidationError(
            "Price is too large."
        )