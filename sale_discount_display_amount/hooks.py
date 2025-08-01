# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import SUPERUSER_ID
from odoo.api import Environment
from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)

COLUMNS = (
    ("sale_order", "price_total_no_discount"),
    ("sale_order", "discount_total"),
    ("sale_order_line", "price_total_no_discount"),
    ("sale_order_line", "discount_total"),
)


def pre_init_hook(env):
    for table, column in COLUMNS:
        if not column_exists(env.cr, table, column):
            _logger.info("Create discount column %s in database", column)
            create_column(env.cr, table, column, "numeric")


def post_init_hook(env):
    _logger.info("Compute discount columns")
    # env = Environment(env.cr, SUPERUSER_ID, {})

    query = """
    update sale_order_line
    set price_total_no_discount = price_total
    where discount = 0.0
    """
    env.cr.execute(query)

    query = """
        update sale_order
        set price_total_no_discount = amount_total
        """
    env.cr.execute(query)

    query = """
    select distinct order_id from sale_order_line where discount > 0.0;
    """

    env.cr.execute(query)
    order_ids = env.cr.fetchall()

    orders = env["sale.order"].search([("id", "in", order_ids)])
