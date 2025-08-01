# Copyright 2025 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools import float_repr

def float_round(value, dp):
    # be careful: odoo rounding implementation does not return the shortest
    # representation of a float. For example, if price_unit is 211.70,
    # you may get 211.70000000000002
    # See: https://gist.github.com/odony/5269a695545902e7e23e761e20a9ec8c
    return float(float_repr(value, dp))
