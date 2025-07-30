# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from extendable_pydantic import StrictExtendableBaseModel

from .country import Country
from .lang import Lang
from .partner_title import PartnerTitle


class Settings(StrictExtendableBaseModel):
    countries: list[Country] = []
    partner_titles: list[PartnerTitle] = []
    langs: list[Lang] = []

    # @classmethod
    # def from_shopinvader_backend(cls, odoo_rec):
    #     return cls.model_construct(countries=[], partner_titles=[], langs=[])
