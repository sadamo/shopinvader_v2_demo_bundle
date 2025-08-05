"""
Como rodar este script:

1. Abra o terminal.
2. Navegue até a pasta do script:
   cd /home/sadamo/kmee/projetos/odoo17/shopinvader_v2_demo_bundle
3. Execute o script com Python 3:
   python3 validate_dependencies.py

O resultado será exibido no terminal em formato de árvore JSON.
"""

import os
import ast
import json

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def find_manifest(module_name):
    found_dirs = []
    for root, dirs, files in os.walk(BASE_PATH):
        if module_name in dirs:
            dir_path = os.path.join(root, module_name)
            found_dirs.append(dir_path)
            manifest_path = os.path.join(dir_path, '__manifest__.py')
            if os.path.exists(manifest_path):
                print(f"[DEBUG] Manifest encontrado para '{module_name}' em: {manifest_path}")
                return manifest_path
            else:
                print(f"[DEBUG] Diretório encontrado para '{module_name}' em: {dir_path}")
                print(f"[DEBUG] __manifest__.py NÃO existe em: {manifest_path}")
                print(f"[DEBUG] Conteúdo do diretório: {os.listdir(dir_path)}")
    if found_dirs:
        print(f"[DEBUG] Diretórios encontrados para '{module_name}': {found_dirs}")
    else:
        print(f"[DEBUG] Módulo '{module_name}' não encontrado em nenhum diretório dentro de {BASE_PATH}")
    return None

def parse_manifest(manifest_path):
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            print(f"[DEBUG] O arquivo {manifest_path} está vazio.")
            return [], []
        manifest = ast.literal_eval(content)
        depends = manifest.get('depends', [])
        external = manifest.get('external_dependencies', {}).get('python', [])
        print(f"[DEBUG] Manifest lido de {manifest_path}: depends={depends}, external={external}")
        return depends, external
    except Exception as e:
        print(f"[DEBUG] Erro ao ler/parsing manifest {manifest_path}: {e}")
        return [], []

ODOO_CORE_MODULES = {
    'base', 'web', 'mail', 'auth_signup', 'portal', 'board', 'fetchmail', 'bus', 'web_editor',
    'web_tour', 'web_kanban', 'web_settings_dashboard', 'web_unsplash', 'web_gantt', 'web_diagram',
    'web_mobile', 'web_responsive', 'web_enterprise', 'web_studio', 'web_planner', 'web_map',
    'web_google_maps', 'web_google_drive', 'web_google_calendar', 'web_google_gmail', 'web_google_contacts',
    'web_google_auth', 'web_google_analytics', 'web_google_spreadsheet', 'web_google_tag_manager',
    'web_google_ads', 'web_google_search_console', 'web_google_my_business', 'web_google_translate',
    'web_google_cloud', 'web_google_api', 'web_google_pay', 'web_google_wallet', 'web_google_places',
    'web_google_recaptcha', 'web_google_fonts', 'web_google_optimize', 'web_google_data_studio',
    'web_google_bigquery', 'web_google_cloud_storage', 'web_google_cloud_functions', 'web_google_cloud_run',
    'web_google_cloud_tasks', 'web_google_cloud_scheduler', 'web_google_cloud_pubsub', 'web_google_cloud_vision',
    'web_google_cloud_nlp', 'web_google_cloud_speech', 'web_google_cloud_translation', 'web_google_cloud_talent',
    'web_google_cloud_video', 'web_google_cloud_iot', 'web_google_cloud_dialogflow', 'web_google_cloud_firestore',
    'web_google_cloud_datastore', 'web_google_cloud_spanner', 'web_google_cloud_sql', 'web_google_cloud_memorystore',
    'web_google_cloud_redis', 'web_google_cloud_bigtable', 'web_google_cloud_dlp', 'web_google_cloud_kms',
    'web_google_cloud_secret_manager', 'web_google_cloud_security', 'web_google_cloud_monitoring',
    'web_google_cloud_logging', 'web_google_cloud_trace', 'web_google_cloud_debugger', 'web_google_cloud_error_reporting',
    'web_google_cloud_profiler', 'web_google_cloud_apigee', 'web_google_cloud_endpoints', 'web_google_cloud_apigee_x',
    'web_google_cloud_app_engine', 'web_google_cloud_compute', 'web_google_cloud_functions_v2',
    'web_google_cloud_run_v2', 'web_google_cloud_tasks_v2', 'web_google_cloud_scheduler_v2', 'web_google_cloud_pubsub_v2',
    'web_google_cloud_vision_v2', 'web_google_cloud_nlp_v2', 'web_google_cloud_speech_v2', 'web_google_cloud_translation_v2',
    'web_google_cloud_talent_v2', 'web_google_cloud_video_v2', 'web_google_cloud_iot_v2', 'web_google_cloud_dialogflow_v2',
    'web_google_cloud_firestore_v2', 'web_google_cloud_datastore_v2', 'web_google_cloud_spanner_v2', 'web_google_cloud_sql_v2',
    'web_google_cloud_memorystore_v2', 'web_google_cloud_redis_v2', 'web_google_cloud_bigtable_v2', 'web_google_cloud_dlp_v2',
    'web_google_cloud_kms_v2', 'web_google_cloud_secret_manager_v2', 'web_google_cloud_security_v2', 'web_google_cloud_monitoring_v2',
    'web_google_cloud_logging_v2', 'web_google_cloud_trace_v2', 'web_google_cloud_debugger_v2', 'web_google_cloud_error_reporting_v2',
    'web_google_cloud_profiler_v2', 'web_google_cloud_apigee_v2', 'web_google_cloud_endpoints_v2', 'web_google_cloud_apigee_x_v2',
    'web_google_cloud_app_engine_v2', 'web_google_cloud_compute_v2'
}

def build_tree(module_name, visited=None):
    if visited is None:
        visited = set()
    if module_name in visited:
        print(f"[DEBUG] Módulo '{module_name}' já visitado, evitando ciclo.")
        return {'cycle': True, 'module': module_name}
    visited.add(module_name)
    # Ignora módulos core do Odoo
    if module_name in ODOO_CORE_MODULES:
        print(f"[DEBUG] Módulo '{module_name}' é core do Odoo, ignorando como faltante.")
        return {
            'depends': {},
            'external_python': [],
            'missing': False,
            'module': module_name,
            'core': True
        }
    manifest_path = find_manifest(module_name)
    if not manifest_path:
        print(f"[DEBUG] Não foi possível localizar o manifest para '{module_name}'.")
        return {
            'missing': True,
            'module': module_name,
            'debug': f"Manifest não encontrado para '{module_name}'",
            'search_path': BASE_PATH
        }
    depends, external = parse_manifest(manifest_path)
    tree = {
        'depends': {},
        'external_python': external,
        'missing': False,
        'manifest_path': manifest_path
    }
    print(f"[DEBUG] Processando dependências de '{module_name}': {depends}")
    if not depends:
        print(f"[DEBUG] Módulo '{module_name}' não possui dependências.")
    for dep in depends:
        tree['depends'][dep] = build_tree(dep, visited)
    return tree

def find_all_manifests():
    manifests = []
    for root, dirs, files in os.walk(BASE_PATH):
        if '__manifest__.py' in files:
            manifests.append(os.path.join(root, '__manifest__.py'))
    return manifests

def check_versions():
    manifests = find_all_manifests()
    not_17 = []
    for manifest_path in manifests:
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            manifest = ast.literal_eval(content)
            version = manifest.get('version', '')
            if not version.startswith('17'):
                not_17.append((manifest.get('name', manifest_path), version, manifest_path))
        except Exception as e:
            print(f"[ERRO] Falha ao ler/parsing {manifest_path}: {e}")
    if not_17:
        print("\n[AVISO] Módulos que NÃO são da versão 17:")
        for name, version, path in not_17:
            print(f"  - {name} | version: {version} | {path}")
    else:
        print("\nTodos os módulos encontrados são da versão 17.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Valida dependências e gera árvore em JSON.")
    parser.add_argument('--out', help='Arquivo de saída JSON', default=None)
    parser.add_argument('--module', help='Módulo raiz', default='shopinvader_v2_app_demo')
    parser.add_argument('--check-versions', action='store_true', help='Verifica versões dos módulos')
    args = parser.parse_args()

    if args.check_versions:
        check_versions()
        return

    root_module = args.module
    tree = build_tree(root_module)
    json_str = json.dumps(tree, indent=2)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"[INFO] Árvore de dependências salva em {args.out}")
    else:
        print(json_str)

if __name__ == '__main__':
    main()
