# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class FsProductMedia(models.Model):
    _name = "fs.product.media"
    _inherit = ["fs.product.media", "se.product.update.mixin"]

    def get_products(self):
        return self.mapped("product_tmpl_id")
