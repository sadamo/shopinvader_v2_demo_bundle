# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import typing

from extendable_pydantic import StrictExtendableBaseModel


class Address(StrictExtendableBaseModel):
    id: int
    name: str | None = None
    street: str | None = None
    street2: str | None = None
    zip: str | None = None
    city: str | None = None
    phone: str | None = None
    mobile: str | None = None
    email: str | None = None
    state_id: int | None = None
    country_id: int | None = None
    company_type: typing.Literal["person", "company"] | None
    title_id: int | None = None

    @classmethod
    def from_res_partner(cls, odoo_rec):
        return cls.model_construct(
            id=odoo_rec.id,
            name=odoo_rec.name or None,
            street=odoo_rec.street or None,
            street2=odoo_rec.street2 or None,
            zip=odoo_rec.zip or None,
            city=odoo_rec.city or None,
            phone=odoo_rec.phone or None,
            mobile=odoo_rec.mobile or None,
            email=odoo_rec.email or None,
            state_id=odoo_rec.state_id.id or None,
            country_id=odoo_rec.country_id.id or None,
            company_type=odoo_rec.company_type or None,
            title_id=odoo_rec.title.id or None,
        )


class InvoicingAddress(Address):
    """
    Invoicing Address
    """

    vat: str | None = None

    @classmethod
    def from_res_partner(cls, odoo_rec):
        res = super().from_res_partner(odoo_rec)
        res.vat = odoo_rec.vat or None

        return res


class DeliveryAddress(Address):
    """
    Delivery Address
    """
