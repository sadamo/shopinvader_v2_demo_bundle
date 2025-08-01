# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.sale_loyalty.tests.common import TestSaleCouponCommon

class TestSaleOrder(TestSaleCouponCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.immediate_promotion_program.active = False
        cls.order = cls.env["sale.order"].create({"partner_id": cls.steve.id})

    def _create_discount_program(self, product):
        return self.env["loyalty.program"].create(
            {
                "name": "50% on order if product bought",
                "program_type": "promotion",
                "trigger": "auto",
                "applies_on": "current",
                "company_id": self.env.company.id,
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "product_ids": [(4, product.id)],
                            "minimum_qty": 1,
                        },
                    )
                ],
                "reward_ids": [
                    (
                        0,
                        0,
                        {
                            "reward_type": "discount",
                            "discount": 50,
                            "required_points": 1,
                        },
                    ),
                ],
            }
        )

    def _create_discount_code_program(self):
        # ...existing code...
