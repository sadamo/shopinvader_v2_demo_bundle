# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader Api Payment Cart",
    "summary": """
        Adds logic to be able to pay current cart""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Shopinvader",
    "website": "https://github.com/shopinvader/odoo-shopinvader-payment",
    "depends": [
        # Odoo
        "account_payment",
        # Shopinvader
        "fastapi",
        "sale_cart",
        "shopinvader_api_payment",
        "shopinvader_api_cart",
    ],
    "data": [
        "views/payment_provider.xml",
    ],
}
