import os
from utils import logg, check_path_exists, check_binary_exists, get_user_home

# Códigos de cores ANSI para log
from constants import (
    GREEN,
    BLUE,
    RED,
    YELLOW,
)


def main():
    logg("Iniciando testes de ambiente...", BLUE)
    tests_passed = 0
    tests_failed = 0

    # 1. Verifica a existência do Git
    if check_binary_exists("git", "Git"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 2. Verifica a existência do shell Zsh
    if check_binary_exists("zsh", "Shell Zsh"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 3. Verifica o diretório do Oh My Zsh
    home = get_user_home()
    ohmyzsh_dir = os.path.join(home, ".oh-my-zsh")
    if check_path_exists(ohmyzsh_dir, "Diretório Oh My Zsh"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 4. Verifica a existência dos plugins do Zsh
    plugins = ["zsh-autosuggestions", "zsh-syntax-highlighting"]
    plugins_success = True
    for plugin in plugins:
        plugin_path = os.path.join(ohmyzsh_dir, "custom", "plugins", plugin)
        if not check_path_exists(plugin_path, f"Plugin {plugin}"):
            plugins_success = False
    if plugins_success:
        tests_passed += 1
    else:
        tests_failed += 1

    # 5. Verifica a existência do diretório do asdf
    asdf_dir = os.path.join(home, ".asdf")
    if check_path_exists(asdf_dir, "Diretório asdf"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 6. Verifica se o arquivo .zshrc foi configurado corretamente
    zshrc_path = os.path.join(home, ".zshrc")
    if check_path_exists(zshrc_path, "Arquivo .zshrc"):
        with open(zshrc_path, "r") as f:
            contents = f.read()
        expected_theme = 'ZSH_THEME="powerlevel10k/powerlevel10k"'
        expected_plugin = "zsh-autosuggestions"
        if expected_theme in contents and expected_plugin in contents:
            logg("Sucesso: .zshrc configurado corretamente.", GREEN)
            tests_passed += 1
        else:
            logg(
                "Falha: .zshrc não contém configurações esperadas (tema/plugins).", RED
            )
            tests_failed += 1
    else:
        tests_failed += 1

    # 7. Verifica a instalação das fontes (ex.: MesloLGS NF Regular)
    fonts_dir = os.path.join(home, ".local", "share", "fonts")
    font_file = os.path.join(fonts_dir, "MesloLGS NF Regular.ttf")
    if check_path_exists(font_file, "Fonte MesloLGS NF Regular.ttf"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 8. Verifica a existência do Docker
    if check_binary_exists("docker", "Docker"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 9. Verifica se o ambiente do Rust está instalado (diretório .cargo e cargo no PATH)
    cargo_dir = os.path.join(home, ".cargo")
    if check_path_exists(cargo_dir, "Diretório .cargo (Rust)"):
        if check_binary_exists("cargo", "Cargo (Rust)"):
            tests_passed += 1
        else:
            tests_failed += 1
    else:
        tests_failed += 1

    # 10. Verifica Node.js, npm e pnpm
    if check_binary_exists("node", "Node.js"):
        tests_passed += 1
    else:
        tests_failed += 1
    if check_binary_exists("npm", "npm"):
        tests_passed += 1
    else:
        tests_failed += 1
    if check_binary_exists("pnpm", "pnpm"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 11. Verifica a instalação do Golang (binary "go")
    if check_binary_exists("go", "Golang (go)"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 12. Verifica o btop
    if check_binary_exists("btop", "btop"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 13. Verifica o LazyGit
    if check_binary_exists("lazygit", "LazyGit"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 14. Verifica o LazyDocker
    if check_binary_exists("lazydocker", "LazyDocker"):
        tests_passed += 1
    else:
        tests_failed += 1

    # 15. Verifica o Aws CLI
    if check_binary_exists("aws", "AWS CLI"):
        tests_passed += 1
    else:
        tests_failed += 1

    logg("--------------------------------------------------", BLUE)
    total = tests_passed + tests_failed
    logg(
        f"Teste concluído. Total de testes: {total}, Sucessos: {tests_passed}, Falhas: {tests_failed}",
        YELLOW,
    )
    if tests_failed == 0:
        logg("Ambiente está configurado corretamente!", GREEN)
    else:
        logg("Alguns testes falharam. Verifique as mensagens acima.", RED)


if __name__ == "__main__":
    main()
