from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ItemModel(models.Model):
    code = fields.CharField(20, unique=True)
    name = fields.CharField(200, unique=True)
    description = fields.TextField(null=True)
    purchase_price = fields.DecimalField(max_digits=6, decimal_places=2)
    sale_price = fields.DecimalField(max_digits=6, decimal_places=2)
    active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name


ItemSchema = pydantic_model_creator(ItemModel)
