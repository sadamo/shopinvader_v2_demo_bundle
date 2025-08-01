
from odoo import fields, models

class ProductBrandTag(models.Model):
    _name = "product.brand.tag"
    _inherit = "product.brand.tag.mixin"
    _description = "Product Brand Tag"

    product_brand_ids = fields.Many2many(relation="product_brand_tag_rel")
