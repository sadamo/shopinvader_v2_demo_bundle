# Copyright 2025 Akretion, GRAP, Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Stock State",
    "summary": "Compute the state of a product's stock based on stock level and sale_ok field",
    "version": "17.0.1.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, GRAP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_stock"],
    "data": [
        "security/res_groups.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "views/product_category_view.xml",
        "views/res_company_view.xml",
        "data/data.xml"
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_product.xml",
        "demo/product_category.xml"
    ],
    "qweb": [],
    "maintainers": ["sebastienbeau", "legalsylvain", "kevinkhao"]
}
