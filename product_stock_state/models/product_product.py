# Copyright 2025 GRAP, ACSONE SA/NV, Akretion, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare

class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_state = fields.Selection(
        selection=[
            ("in_stock", "In Stock"),
            ("in_limited_stock", "In Limited Stock"),
            ("resupplying", "Resupplying"),
            ("out_of_stock", "Out Of Stock"),
        ],
        compute="_compute_stock_state",
    )

    def _get_qty_available_for_stock_state(self):
        self.ensure_one()
        return self.qty_available

    def _stock_state_check_in_stock(self, qty, precision):
        return (
            float_compare(
                qty,
                self._get_stock_state_threshold(),
                precision_digits=precision,
            )
            == 1
        )

    def _stock_state_check_in_limited_stock(self, qty, precision):
        return float_compare(qty, 0, precision_digits=precision) == 1

    def _stock_state_check_resupplying(self, qty, precision):
        return float_compare(self.incoming_qty, 0, precision_digits=precision) == 1

    def _stock_state_check_out_of_stock(self, qty, precision):
        return True

    def _available_states(self):
        return [x[0] for x in self._fields["stock_state"].selection]

    # ...existing code...
