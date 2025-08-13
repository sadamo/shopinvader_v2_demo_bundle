from odoo import models

from odoo.addons.sale.models.sale_order import SaleOrder

from .schemas.cart import CartUpdateInput


class ShopinvaderApiCartRouterHelper(models.AbstractModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    def _prepare_update_cart_vals(self, data: CartUpdateInput, cart: SaleOrder):
        vals = super()._prepare_update_cart_vals(data, cart)
        if data.current_step or data.next_step:
            step_data = cart._cart_step_update_vals(
                current_step=data.current_step, next_step=data.next_step
            )
            vals.update(step_data)
        return vals
