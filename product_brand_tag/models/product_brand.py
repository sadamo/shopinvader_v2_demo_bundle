
from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    tag_ids = fields.Many2many(
        comodel_name="product.brand.tag",
        relation="product_brand_tag_rel",
        column1="brand_id",
        column2="tag_id",
        string="Tags",
    )
