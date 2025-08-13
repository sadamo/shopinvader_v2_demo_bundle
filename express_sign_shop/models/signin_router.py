# Copyright 2024 SX


from odoo import api, models

from odoo.addons.shopinvader_fastapi_auth_jwt.dependencies import Payload


class ShopinvaderApSigninJwtRouterHelper(models.AbstractModel):
    _inherit = "shopinvader_api_signin_jwt.signin_router.helper"

    @api.model
    def _get_partner_create_vals(self, payload: Payload):
        data = {
            "name": payload.get("name") or payload.get("sub") or payload.get("email"),
            "ref": payload.get("sub"),
            "email": payload.get("email"),
            "phone": payload.get("phone"),
        }

        if payload.get("user_metadata"):
            user_metadata = payload.get("user_metadata")
            if user_metadata.get("full_name"):
                data["name"] = user_metadata.get("full_name")
        return data
