# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class ProductTemplateLinkType(models.Model):
    _name = "product.template.link.type"
    _description = "Product Template Link Type"

    name = fields.Char(required=True, translate=True)
    inverse_name = fields.Char(
        compute="_compute_inverse_name",
        inverse="_inverse_inverse_name",
        readonly=False,
        store=True,
        translate=True,
    )
    manual_inverse_name = fields.Char()
    is_symmetric = fields.Boolean(
        help="The relation meaning is the same from each side of the relation",
        default=True,
    )
    code = fields.Char(
        "Technical code",
        help="This code allows to provide a technical code to external systems identifying this link type",
    )
    inverse_code = fields.Char(
        "Technical code (inverse)",
        compute="_compute_inverse_code",
        inverse="_inverse_inverse_code",
        readonly=False,
        store=True,
        help="This code allows to provide a technical code to external systems identifying this link type",
    )
    manual_inverse_code = fields.Char()
    _sql_constraints = [
        ("name_uniq", "unique (name)", "Link type name already exists !"),
        ("inverse_name_uniq", "unique (inverse_name)", "Link type inverse name already exists !"),
        ("code_uniq", "EXCLUDE (code WITH =) WHERE (code is not null)", "Link code already exists !"),
        ("inverse_code_uniq", "EXCLUDE (inverse_code WITH =) WHERE (inverse_code is not null)", "Link inverse code already exists !"),
    ]
    display_name = fields.Char(compute="_compute_display_name")
