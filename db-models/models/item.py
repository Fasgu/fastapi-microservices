from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ItemModel(models.Model):
    code = fields.TextField(max_length=20)
    name = fields.TextField()
    description = fields.TextField(null=True)
    purchase_price = fields.FloatField()
    sale_price = fields.FloatField(decimal_places=2)
    active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name


ItemSchema = pydantic_model_creator(ItemModel)
