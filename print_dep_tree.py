import json
import sys
import os

# Para modo gráfico, instale: pip install graphviz
try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

# Cores ANSI para terminal
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

ODOO_CORE_MODULES = {
    'base', 'web', 'mail', 'auth_signup', 'portal', 'board', 'fetchmail', 'bus', 'web_editor',
    'web_tour', 'web_kanban', 'web_settings_dashboard', 'web_unsplash', 'web_gantt', 'web_diagram',
    'web_mobile', 'web_responsive', 'web_enterprise', 'web_studio', 'web_planner', 'web_map'
    # Adicione outros módulos core conforme necessário
}

def print_tree(tree, prefix="", is_last=True):
    module = tree.get('module')
    manifest_path = tree.get('manifest_path', '')
    missing = tree.get('missing', False)
    external = tree.get('external_python', [])
    name = module if module else manifest_path.split(os.sep)[-2] if manifest_path else "root"
    status = f"{RED}[MISSING]{RESET}" if missing else ""
    branch = "└── " if is_last else "├── "
    print(f"{prefix}{branch}{BOLD}{name}{RESET} {status}")
    # Dependências externas
    for i, lib in enumerate(external):
        ext_branch = "└── " if i == len(external) - 1 else "├── "
        print(f"{prefix}    {BLUE}{ext_branch}(python) {lib}{RESET}")
    # Dependências de módulos
    depends = tree.get('depends', {})
    dep_keys = list(depends.keys())
    for idx, dep in enumerate(dep_keys):
        subtree = depends[dep]
        last = idx == len(dep_keys) - 1
        print_tree(subtree, prefix + ("    " if is_last else "│   "), last)

def build_graph(tree, dot=None, parent=None):
    if dot is None:
        dot = Digraph(comment="Árvore de dependências")
    module = tree.get('module')
    manifest_path = tree.get('manifest_path', '')
    missing = tree.get('missing', False)
    external = tree.get('external_python', [])
    name = module if module else manifest_path.split(os.sep)[-2] if manifest_path else "root"
    label = f"{name}{' [MISSING]' if missing else ''}"
    dot.node(label, label, color="red" if missing else "black")
    if parent:
        dot.edge(parent, label)
    for lib in external:
        lib_label = f"(python) {lib}"
        dot.node(lib_label, lib_label, shape="box", color="blue")
        dot.edge(label, lib_label)
    depends = tree.get('depends', {})
    for dep, subtree in depends.items():
        build_graph(subtree, dot, label)
    return dot

def collect_missing(tree, missing=None):
    if missing is None:
        missing = set()
    if tree.get('missing', False):
        module = tree.get('module')
        if module and module not in ODOO_CORE_MODULES:
            missing.add(module)
    for dep_tree in tree.get('depends', {}).values():
        collect_missing(dep_tree, missing)
    return missing

if __name__ == "__main__":
    # Uso: python3 print_dep_tree.py deps.json [--graph]
    if len(sys.argv) < 2:
        print("Uso: python3 print_dep_tree.py deps.json [--graph]")
        sys.exit(1)
    show_graph = "--graph" in sys.argv
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read().strip()
            print(f"[DEBUG] Início do conteúdo do arquivo JSON: {content[:100]!r}")
            if not content:
                print("[ERRO] O arquivo JSON está vazio. Gere a saída corretamente com validate_dependencies.py.")
                sys.exit(1)
            if content.startswith("'") or content.startswith("#"):
                print("[ERRO] O arquivo não está em formato JSON válido. Verifique se foi gerado com json.dumps.")
                print("Conteúdo bruto do arquivo:")
                print(content)
                sys.exit(1)
            try:
                tree = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"[ERRO] Falha ao carregar JSON: {e}")
                erro_pos = e.pos
                contexto_inicio = max(0, erro_pos - 10)
                contexto_fim = min(len(content), erro_pos + 10)
                print(f"\n[DEBUG] Contexto do erro (pos {erro_pos}):")
                print(content[contexto_inicio:contexto_fim])
                print(f"[DEBUG] Linha: {e.lineno}, Coluna: {e.colno}")
                print("Verifique se há aspas simples, vírgulas extras, ou sintaxe inválida no JSON.")
                sys.exit(1)
    except Exception as e:
        print(f"[ERRO] Falha ao abrir o arquivo: {e}")
        sys.exit(1)

    if show_graph:
        if not GRAPHVIZ_AVAILABLE:
            print("[ERRO] graphviz não está instalado. Instale com: pip install graphviz")
            sys.exit(1)
        dot = build_graph(tree)
        dot.render('dep_tree', view=True, format='png')
        print("Árvore de dependências gerada em dep_tree.png")
    else:
        print_tree(tree)
        # Exibe módulos faltantes ao final
        missing_mods = collect_missing(tree)
        if missing_mods:
            print("\nMÓDULOS FALTANTES:")
            for mod in sorted(missing_mods):
                print(f"  - {mod}")
        else:
            print("\nNenhum módulo faltante detectado.")

