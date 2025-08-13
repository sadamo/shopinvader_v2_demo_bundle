# arquivo para carrinho sem pagamento


# from typing import Annotated

# from fastapi import Depends, HTTPException

# from odoo import api

# from odoo.addons.base.models.res_partner import Partner as ResPartner
# from odoo.addons.fastapi.dependencies import (
#     authenticated_partner,
#     authenticated_partner_env,
# )
# from odoo.addons.shopinvader_api_cart.routers import cart_router

# from ..schemas.cart import CartConfirmResponse


# @cart_router.post("/confirm")
# def confirm_cart(
#     env: Annotated[api.Environment, Depends(authenticated_partner_env)],
#     partner: Annotated["ResPartner", Depends(authenticated_partner)],
# ) -> CartConfirmResponse:
#     """Confirma o carrinho atual sem necessidade de pagamento."""
#     cart = env["sale.order"]._find_open_cart(partner.id)
#     if not cart:
#         raise HTTPException(status_code=404, detail="Carrinho não encontrado")

#     try:
#         cart.action_confirm_cart()
#         return CartConfirmResponse(
#             success=True,
#             message="Orçamento solicitado com sucesso",
#             order_id=cart.id,
#             order_name=cart.name,
#         )
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
