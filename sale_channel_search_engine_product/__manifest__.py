# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Channel Search Engine Product",
    "summary": "Implement an export of category in search engine based on "
    "sale channel link",
    "version": "17.0.0.1.0",
    "development_status": "Alpha",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/sale-channel",
    "author": " Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_channel_search_engine",
        "sale_channel_product",
    ],
    "data": [
        "views/product_template_view.xml",
    ],
    "demo": [],
}
