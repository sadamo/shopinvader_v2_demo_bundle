# Copyright 2024 SX

from typing import Any

from fastapi import APIRouter, FastAPI

from odoo import api, fields, models

from odoo.addons.fastapi.dependencies import authenticated_partner_impl
from odoo.addons.shopinvader_api_address.routers.address_service import address_router
from odoo.addons.shopinvader_api_cart.routers import cart_router
from odoo.addons.shopinvader_api_customer.routers import customer_router
from odoo.addons.shopinvader_api_delivery_carrier.routers import (
    delivery_carrier_cart_router,
    delivery_carrier_router,
    delivery_router,
)
from odoo.addons.shopinvader_api_lead.routers import lead_router
from odoo.addons.shopinvader_api_payment.routers import payment_router
from odoo.addons.shopinvader_api_sale.routers import sale_router
from odoo.addons.shopinvader_api_sale_loyalty.routers import sale_loyalty_cart_router
from odoo.addons.shopinvader_api_settings.routers import settings_router
from odoo.addons.shopinvader_api_signin_jwt.routers import signin_router
from odoo.addons.shopinvader_fastapi_auth_jwt.dependencies import (
    auth_jwt_authenticated_or_anonymous_partner,
)

from ..dependencies import (
    auth_jwt_authenticated_or_anonymous_jwt_partner_autocreate as jpa,
)


class FastapiEndpoint(models.Model):
    _inherit = "fastapi.endpoint"

    app: str = fields.Selection(
        selection_add=[("express_sign_shop", "Express Sign Shop")],
        ondelete={"express_sign_shop": "cascade"},
    )

    auth_jwt_validator_id = fields.Many2one("auth.jwt.validator")

    def _get_fastapi_routers(self):
        if self.app == "express_sign_shop":
            return self._get_express_sign_shop_fastapi_routers()
        return super()._get_fastapi_routers()

    @api.model
    def _get_express_sign_shop_fastapi_routers(self) -> list[APIRouter]:
        if "address" not in address_router.tags:
            address_router.tags.append("address")
        return [
            lead_router,
            address_router,
            customer_router,
            sale_router,
            payment_router,
            delivery_carrier_router,
            delivery_router,
            settings_router,
            signin_router,
        ]

    def _get_express_sign_shop_tags(self, params) -> list:
        tags_metadata = params.get("openapi_tags", []) or []
        tags_metadata.append(
            {
                "name": "addresses",
                "description": "Set of services to manage addresses",
            }
        )
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        tags_metadata.append(
            {
                "name": "cart",
                "description": "Set of services to manage carts",
                "externalDocs": {
                    "description": "Cart services are available under "
                    "a specific authentication mechanism",
                    "url": f"{base_url}{self.root_path}/carts/docs",
                },
            }
        )
        tags_metadata.append(
            {
                "name": "loyalties",
                "description": "Set of services to manage rewards and loyalties",
            }
        )
        return tags_metadata

    def _prepare_fastapi_app_params(self) -> dict[str, Any]:
        params = super()._prepare_fastapi_app_params()
        if self.app == "express_sign_shop":
            params["openapi_tags"] = self._get_express_sign_shop_tags(params)
            # params[
            #     "swagger_ui_oauth2_redirect_url"
            # ] = "/kmee_shop/docs/oauth2-redirect"
            # params["swagger_ui_init_oauth"] = {
            #     "clientId": "demo16.sx.com",
            # }
        return params

    def _get_express_sign_shop_app_dependencies_overrides(self):
        return {
            authenticated_partner_impl: auth_jwt_authenticated_or_anonymous_partner,
        }

    def _get_express_sign_cart_app_dependencies_overrides(self):
        return {
            authenticated_partner_impl: jpa,
        }

    def _get_app(self):
        app = super()._get_app()
        if self.app == "express_sign_shop":
            app.dependency_overrides.update(
                self._get_express_sign_shop_app_dependencies_overrides()
            )
            cart_app = FastAPI()
            cart_app.include_router(cart_router)
            cart_app.include_router(delivery_carrier_cart_router)
            cart_app.include_router(sale_loyalty_cart_router)
            cart_app.dependency_overrides.update(self._get_app_dependencies_overrides())
            cart_app.dependency_overrides.update(
                self._get_express_sign_cart_app_dependencies_overrides()
            )
            app.mount("/carts", cart_app)
        return app
