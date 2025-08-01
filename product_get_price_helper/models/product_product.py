# Copyright 2025 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2025 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import float_compare, float_is_zero
from ..utils import float_round

class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_price(
        self, qty=1.0, pricelist=None, fposition=None, company=None, date=None
    ):
        """Computes the product prices
        :param qty:         The product quantity, used to apply pricelist rules.
        :param pricelist:   Optional. Get prices for a specific pricelist.
        :param fposition:   Optional. Apply fiscal position to product taxes.
        :param company:     Optional.
        :param date:        Optional.
        :returns: A dictionary where keys are product IDs and values are dictionaries with:
            <value>                 The product unitary price
            <tax_included>          True if product taxes are included in <price>.
            If the pricelist.discount_policy is "without_discount":
            <original_value>        The original price (before pricelist is applied).
            <discount>              The discounted percentage.
        """
        AccountTax = self.env["account.tax"]
        DecimalPrecision = self.env["decimal.precision"]
        price_dp = DecimalPrecision.precision_get("Product Price")
        discount_dp = DecimalPrecision.precision_get("Discount")
        company = company or self.env.company
        product_context = dict(
            self.env.context,
            quantity=qty,
            pricelist=pricelist.id if pricelist else None,
            fiscal_position=fposition,
            date=date,
        )
        self = self.with_company(company).with_context(**product_context)
        self.read(["lst_price", "taxes_id"])
        taxes_map = {}
        for product in self:
            taxes = product.taxes_id.filtered(lambda tax: tax.company_id == company)
            if fposition:
                taxes = fposition.map_tax(taxes)
        # ...existing code...
