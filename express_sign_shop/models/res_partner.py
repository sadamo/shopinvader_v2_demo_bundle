# Copyright 2023 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models

from odoo.addons.fastapi_auth_jwt.dependencies import Payload


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _create_anonymous_partner__jwt(self, payload: Payload):
        partner = (
            self.env["res.partner"]
            .sudo()
            .create(
                {
                    "name": _("Anonymous (%s)", payload["sub"][:8]),
                    "anonymous_token": payload["sub"],
                    "active": False,
                }
            )
        )
        return partner

    @api.model
    def _get_anonymous_partner__jwt(self, payload: Payload):
        return (
            self.env["res.partner"]
            .sudo()
            .with_context(active_test=False)
            .search([("anonymous_token", "=", payload["sub"])], limit=1)
        )

    @api.model
    def _delete_anonymous_partner__jwt(self, payload: Payload):
        partner = self._get_anonymous_partner__jwt(payload)
        if partner:
            partner.unlink()
