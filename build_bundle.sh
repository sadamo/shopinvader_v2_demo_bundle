#!/bin/bash
# Script para montar o bundle shopinvader_v2_demo_bundle
# Copia módulos e dependências, sinaliza ausentes

set -e
BUNDLE_DIR="$(dirname "$0")"
EXPRESS_SIGN="/home/sadamo/kmee/projetos/odoo17/addons/express-sign"
MISSING="$BUNDLE_DIR/MISSING_MODULES.txt"

# Lista de dependências diretas do shopinvader_v2_app_demo
MODULES=(
    connector_elasticsearch
    fastapi
    sale_channel_search_engine_category
    sale_channel_search_engine_product
    shopinvader_anonymous_partner
    shopinvader_api_address
    shopinvader_api_cart
    shopinvader_api_customer
    shopinvader_api_delivery_carrier
    shopinvader_api_payment_cart
    shopinvader_api_payment_provider_custom
    shopinvader_api_payment_provider_sips
    shopinvader_api_payment_provider_stripe
    shopinvader_api_sale_loyalty
    shopinvader_api_sale
    shopinvader_api_settings
    shopinvader_api_signin_jwt
    shopinvader_api_wishlist
    shopinvader_fastapi_auth_jwt
    shopinvader_product_brand_tag
    shopinvader_product_brand
    shopinvader_product_description
    shopinvader_product_seo
    shopinvader_product_url
    shopinvader_product
    shopinvader_search_engine_image
    shopinvader_search_engine_product_brand_image
    shopinvader_search_engine_product_price
    shopinvader_search_engine_product_stock_state
    shopinvader_search_engine_update_image
    shopinvader_search_engine_update_product_brand_image
    shopinvader_search_engine_update_product_brand
    shopinvader_search_engine_update_product_media
    shopinvader_search_engine_update_product_template_multi_link
    shopinvader_search_engine
)

# Função para buscar e copiar módulo
copy_module() {
    local mod="$1"
    local found=""
    # Buscar em express-sign raiz
    if [[ -d "$EXPRESS_SIGN/$mod" ]]; then
        cp -r "$EXPRESS_SIGN/$mod" "$BUNDLE_DIR/"
        found=1
    fi
    # Buscar em submódulos
    for sub in brand delivery-carrier odoo-shopinvader rest-framework sale-channel search-engine product-attribute sale-workflow reporting-engine storage; do
        if [[ -d "$EXPRESS_SIGN/$sub/$mod" ]]; then
            cp -r "$EXPRESS_SIGN/$sub/$mod" "$BUNDLE_DIR/"
            found=1
        fi
    done
    # Buscar em odoo-shopinvader
    if [[ -d "$EXPRESS_SIGN/odoo-shopinvader/$mod" ]]; then
        cp -r "$EXPRESS_SIGN/odoo-shopinvader/$mod" "$BUNDLE_DIR/"
        found=1
    fi
    # Sinalizar ausente
    if [[ -z "$found" ]]; then
        echo "$mod" >> "$MISSING"
    fi
}

# Limpar lista de ausentes
> "$MISSING"

# Copiar shopinvader_v2_app_demo
copy_module shopinvader_v2_app_demo

# Copiar dependências diretas
for mod in "${MODULES[@]}"; do
    copy_module "$mod"
done

echo "Bundle montado. Verifique $MISSING para módulos ausentes."
