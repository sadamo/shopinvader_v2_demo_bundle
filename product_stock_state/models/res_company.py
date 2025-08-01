# Copyright 2025 GRAP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    stock_state_threshold = fields.Float(default=10, digits="Stock Threshold")
