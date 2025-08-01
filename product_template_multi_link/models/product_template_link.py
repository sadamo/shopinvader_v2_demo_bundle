# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from contextlib import contextmanager
from psycopg2.extensions import AsIs
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ProductTemplateLink(models.Model):
    _name = "product.template.link"
    _order = "left_product_tmpl_id, right_product_tmpl_id"
    _description = "Product link"

    left_product_tmpl_id = fields.Many2one(
        string="Source Product",
        comodel_name="product.template",
        required=True,
        ondelete="cascade",
        index=True,
    )
    right_product_tmpl_id = fields.Many2one(
        string="Linked Product",
        comodel_name="product.template",
        required=True,
        ondelete="cascade",
        index=True,
    )
    type_id = fields.Many2one(
        string="Link type",
        comodel_name="product.template.link.type",
        required=True,
        ondelete="restrict",
        index=True,
    )
    link_type_name = fields.Char(related="type_id.name")
    link_type_inverse_name = fields.Char(related="type_id.inverse_name")
    is_link_active = fields.Boolean(compute="_compute_is_link_active")

    def _compute_is_link_active(self):
        for record in self:
            record.is_link_active = True

    @api.constrains("left_product_tmpl_id", "right_product_tmpl_id", "type_id")
    def _check_products(self):
        self.flush_recordset()
        if any(rec._check_product_not_different() for rec in self):
            raise ValidationError("Source and linked products must be different.")
        # ...continuação do método...
