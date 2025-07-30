# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader Api Payment Provider Stripe",
    "summary": """
        Specific routes for Stripe payments from Shopinvader""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Shopinvader",
    "website": "https://github.com/shopinvader/odoo-shopinvader-payment",
    "depends": [
        "fastapi",
        "shopinvader_api_payment",
        "payment_stripe",
    ],
    "data": [],
    "demo": [],
}
