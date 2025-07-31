# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _play_onchanges_cart_line(self, vals):
        return self.sudo().play_onchanges(vals, vals.keys())

    def _prepare_cart_line_transfer_values(self):
        """
        Prepare the values to create a new cart line from a given cart line,
        in case of a cart transfer for example.
        """
        return {
            "product_id": self.product_id.id,
            "product_uom_qty": self.product_uom_qty,
        }

    def _match_cart_line(self, product_id, **kwargs):
        """
        Return True if the given sale order line matches the given fields.
        """
        return self.product_id.id == product_id
