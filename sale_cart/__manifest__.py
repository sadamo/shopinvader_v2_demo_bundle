# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Cart",
    "summary": "Carrinho de vendas para Odoo",
    "version": "17.0.1.0.0",
    "author": "Seu Nome ou Empresa",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "sales_team"
        # Adicione outros módulos necessários e remova os que não existem no Odoo 17
    ],
    "data": [
        # Adicione arquivos XML, CSV, etc. necessários para o módulo funcionar
    ],
    "external_dependencies": {
        "python": [
            "openupgradelib"
        ]
    },
    "installable": True,
    "application": False,
    # "assets": {
    #     "web.assets_backend": [
    #         # Adicione arquivos JS/CSS se necessário
    #     ],
    # },
}
