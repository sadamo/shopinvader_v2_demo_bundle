from odoo.addons.shopinvader_api_customer.schemas.customer import (
    Customer,
    CustomerUpdate,
)


class CustomerWithVat(Customer, extends=True):
    vat: str | None = None

    @classmethod
    def from_res_partner(cls, odoo_rec):
        obj = super().from_res_partner(odoo_rec)
        obj.vat = odoo_rec.vat or None
        return obj


class CustomerUpdateWithVat(CustomerUpdate, extends=True):
    vat: str | None = None

    def _get_partner_update_fields(self):
        fields = super()._get_partner_update_fields()
        fields.append("vat")
        return fields
