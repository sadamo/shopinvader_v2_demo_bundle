# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

class ProductTemplateLinker(models.TransientModel):
    """
    Wizard used to link product template together in one shot
    """
    _name = "product.template.linker"
    _description = "Product template linker wizard"

    operation_type = fields.Selection(
        selection=[
            ("unlink", "Remove existing links"),
            ("link", "Link these products"),
        ],
        string="Operation",
        required=True,
        help="Remove existing links: will remove every existing link on each selected products;\nLink these products: will link all selected products together.",
    )
    product_ids = fields.Many2many(
        comodel_name="product.template",
        string="Products",
    )
    type_id = fields.Many2one(
        string="Link type",
        comodel_name="product.template.link.type",
        ondelete="restrict",
    )

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        ctx = self.env.context
        active_ids = ctx.get("active_ids", ctx.get("active_id", []))
        products = []
        if ctx.get("active_model") == self.product_ids._name and active_ids:
            products = [(6, False, list(active_ids))]
        result.update({"product_ids": products})
        return result

    def action_apply(self):
        if self.operation_type == "link":
            self.action_apply_link()
        elif self.operation_type == "unlink":
            self.action_apply_unlink()
        # ...continuação do método...
