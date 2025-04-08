#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import shutil
import time

# Códigos de cores ANSI
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

import atexit
import signal
import subprocess
import threading

def keep_sudo_alive():
    """Mantém a sessão sudo viva em background"""
    def run():
        try:
            while True:
                subprocess.run(["sudo", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(60)
        except:
            pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

def request_sudo():
    """Solicita sudo uma vez no início e mantém a sessão ativa"""
    try:
        subprocess.run(["sudo", "-v"], check=True)
        keep_sudo_alive()
        atexit.register(lambda: subprocess.run(["sudo", "-k"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    except subprocess.CalledProcessError:
        log("Falha ao obter acesso sudo. Encerrando...", RED)
        exit(1)

def log(message, color=BLUE):
    print(f"{color}{message}{RESET}")

def run_command(cmd, env=None):
    log(f"Executando: {cmd}", GREEN)
    subprocess.run(cmd, shell=True, check=True, env=env)

def update_upgrade():
    log("Passo: Atualizando e atualizando pacotes...", BLUE)
    run_command("sudo apt update -y")
    run_command("sudo apt upgrade -y")

def install_packages():
    log("Passo: Instalando pacotes essenciais...", BLUE)
    apt_packages = (
        "build-essential curl libbz2-dev libffi-dev liblzma-dev libncursesw5-dev "
        "libreadline-dev libsqlite3-dev libssl-dev libxml2-dev libxmlsec1-dev llvm "
        "make tk-dev wget xz-utils zlib1g-dev"
    )
    run_command(f"sudo apt install -y {apt_packages}")

def install_basic_tools():
    log("Passo: Instalando ferramentas básicas...", BLUE)
    run_command("sudo apt install -y zsh git wget curl unzip")

def change_default_shell():
    log("Passo: Alterando shell padrão para zsh...", BLUE)
    try:
        subprocess.run("chsh -s $(which zsh)", shell=True, check=True, timeout=10)
    except subprocess.TimeoutExpired:
        log("chsh travou. Por favor, altere o shell manualmente com 'chsh -s $(which zsh)'", YELLOW)
    except KeyboardInterrupt:
        log("Alteração de shell cancelada pelo usuário. Execute 'chsh -s $(which zsh)' manualmente se desejar.", YELLOW)
    except subprocess.CalledProcessError as e:
        log(f"Falha ao alterar shell: {e}", RED)

def install_oh_my_zsh():
    log("Passo: Instalando Oh My Zsh...", BLUE)
    home = os.path.expanduser("~")
    ohmyzsh_dir = os.path.join(home, ".oh-my-zsh")
    if os.path.exists(ohmyzsh_dir):
        log("O diretório do Oh My Zsh já existe. Pulando instalação.", YELLOW)
        return

    env = os.environ.copy()
    env["RUNZSH"] = "no"
    env["CHSH"] = "no"
    run_command('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"', env=env)

def clone_repo(repo_url, dest):
    if os.path.exists(dest):
        log(f"O diretório {dest} já existe, pulando clone.", YELLOW)
    else:
        run_command(f"git clone {repo_url} {dest}")

def setup_zsh_plugins():
    log("Passo: Configurando plugins do Zsh...", BLUE)
    home = os.path.expanduser("~")
    custom_plugins_dir = os.path.join(home, ".oh-my-zsh", "custom", "plugins")
    os.makedirs(custom_plugins_dir, exist_ok=True)

    plugins = {
        "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions.git",
        "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting.git"
    }

    for name, repo_url in plugins.items():
        dest = os.path.join(custom_plugins_dir, name)
        if os.path.isdir(dest):
            log(f"Plugin {name} já instalado, pulando.", YELLOW)
        else:
            try:
                run_command(f"git clone {repo_url} {dest}")
                log(f"Plugin {name} instalado com sucesso.", GREEN)
            except subprocess.CalledProcessError:
                log(f"Erro ao clonar o plugin {name}.", RED)

def setup_asdf():
    log("Passo: Instalando asdf...", BLUE)
    home = os.path.expanduser("~")
    asdf_dir = os.path.join(home, ".asdf")
    if os.path.exists(asdf_dir):
        log("asdf já está instalado, pulando clone.", YELLOW)
    else:
        run_command("git clone https://github.com/asdf-vm/asdf.git ~/.asdf")

def update_zshrc():
    log("Passo: Atualizando .zshrc com plugins e tema...", BLUE)
    home = os.path.expanduser("~")
    zshrc = os.path.join(home, ".zshrc")
    plugins_line = "plugins=( git docker docker-compose python celery zsh-autosuggestions zsh-syntax-highlighting )"
    theme_line = 'ZSH_THEME="powerlevel10k/powerlevel10k"'
    added = False
    if os.path.exists(zshrc):
        with open(zshrc, "r") as f:
            contents = f.read()
        if plugins_line not in contents:
            with open(zshrc, "a") as f:
                f.write("\n# Plugins adicionados automaticamente\n")
                f.write(plugins_line + "\n")
            added = True
        if theme_line not in contents:
            with open(zshrc, "a") as f:
                f.write("\n# Tema adicionado automaticamente\n")
                f.write(theme_line + "\n")
            added = True
    else:
        with open(zshrc, "w") as f:
            f.write(plugins_line + "\n")
            f.write(theme_line + "\n")
        added = True
    if added:
        log("Arquivo .zshrc atualizado.", GREEN)
    else:
        log("Arquivo .zshrc já estava configurado.", YELLOW)

def install_powerlevel10k():
    log("Passo: Instalando Powerlevel10k...", BLUE)
    home = os.path.expanduser("~")
    omz_custom = os.path.join(home, ".oh-my-zsh", "custom")
    themes_dir = os.path.join(omz_custom, "themes")
    os.makedirs(themes_dir, exist_ok=True)
    dest = os.path.join(themes_dir, "powerlevel10k")
    clone_repo("https://github.com/romkatv/powerlevel10k.git --depth=1", dest)

def configure_powerlevel10k_theme():
    """
    Define o tema do Zsh no arquivo .zshrc para usar o Powerlevel10k.
    Essa função verifica se já existe uma linha começando com ZSH_THEME= e a substitui,
    ou adiciona a linha ao final do arquivo.
    """
    log("Passo: Configurando o tema Powerlevel10k no .zshrc...", BLUE)
    home = os.path.expanduser("~")
    zshrc_path = os.path.join(home, ".zshrc")
    theme_line = 'ZSH_THEME="powerlevel10k/powerlevel10k"'
    try:
        # Se o .zshrc já existir, lê as linhas
        if os.path.exists(zshrc_path):
            with open(zshrc_path, "r") as f:
                lines = f.readlines()
            found = False
            # Atualiza a linha que define o tema ou adiciona ao final
            for i, line in enumerate(lines):
                if line.startswith("ZSH_THEME="):
                    lines[i] = theme_line + "\n"
                    found = True
                    break
            if not found:
                lines.append("\n" + theme_line + "\n")
            with open(zshrc_path, "w") as f:
                f.writelines(lines)
            log("Tema Powerlevel10k configurado no .zshrc com sucesso.", GREEN)
        else:
            with open(zshrc_path, "w") as f:
                f.write(theme_line + "\n")
            log("Arquivo .zshrc criado e tema Powerlevel10k configurado com sucesso.", GREEN)
    except Exception as e:
        log(f"Erro ao configurar o tema Powerlevel10k: {e}", RED)

def install_fonts():
    log("Passo: Instalando fontes (Nerd Fonts e JetBrains Mono)...", BLUE)
    home = os.path.expanduser("~")
    fonts_dir = os.path.join(home, ".local", "share", "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    
    fonts = {
        "MesloLGS NF Regular.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf",
        "MesloLGS NF Bold.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf",
        "MesloLGS NF Italic.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf",
        "MesloLGS NF Bold Italic.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf"
    }
    for filename, url in fonts.items():
        dest_file = os.path.join(fonts_dir, filename)
        if os.path.exists(dest_file):
            log(f"Fonte {filename} já instalada, pulando.", YELLOW)
        else:
            run_command(f"wget -O \"{dest_file}\" \"{url}\"")
    run_command("fc-cache -fv")
    
    # Instala a fonte JetBrains Mono
    jetbrains_zip = os.path.join("/tmp", "jetbrains-mono.zip")
    jetbrains_url = "https://download.jetbrains.com/fonts/JetBrainsMono-2.242.zip"
    run_command(f"wget -O {jetbrains_zip} \"{jetbrains_url}\"")
    extract_dir = os.path.join("/tmp", "jetbrains-mono")
    os.makedirs(extract_dir, exist_ok=True)
    run_command(f"unzip -o {jetbrains_zip} -d {extract_dir}")
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.lower().endswith((".ttf", ".otf")):
                full_path = os.path.join(root, file)
                shutil.copy(full_path, fonts_dir)
    run_command("fc-cache -fv")

def install_docker():
    log("Passo: Instalando Docker...", BLUE)
    run_command("sudo apt install -y docker.io")
    run_command("sudo systemctl enable --now docker")
    run_command("sudo usermod -aG docker $USER")
    log("Docker instalado. Faça logout/login para aplicar as mudanças.", GREEN)

def update_rust_env():
    log("Passo: Atualizando ambiente do Rust...", BLUE)
    rust_bin = os.path.expanduser("~/.cargo/bin")
    if os.path.isdir(rust_bin):
        os.environ["PATH"] = f"{rust_bin}:" + os.environ["PATH"]
        log("Ambiente do Rust atualizado.", GREEN)
    else:
        log("Diretório do Rust não encontrado. Verifique a instalação.", RED)

def install_rust():
    log("Passo: Instalando Rust...", BLUE)
    run_command("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
    update_rust_env()
    run_command("cargo install exa bat")

def install_uv():
    log("Passo: Instalando UV (depende do Rust)...", BLUE)
    run_command("cargo install --git https://github.com/astral-sh/uv uv")

def install_node_pnpm():
    log("Passo: Instalando Node.js, npm e pnpm...", BLUE)
    run_command("sudo apt install -y nodejs npm")
    run_command("sudo npm install -g pnpm")

def install_golang():
    log("Passo: Instalando Golang...", BLUE)
    run_command("sudo apt install -y golang-go")

def install_btop():
    log("Passo: Instalando btop...", BLUE)
    run_command("sudo apt install -y btop")

def install_lazygit():
    log("Passo: Instalando LazyGit...", BLUE)
    try:
        # Obtém o JSON da release mais recente
        version_json = subprocess.check_output(
            'curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest"',
            shell=True
        ).decode()
        # Extrai exatamente como no comando grep -Po '"tag_name": *"v\K[^"]*'
        match = re.search(r'"tag_name":\s*"v?([^"]+)"', version_json)
        if not match:
            raise RuntimeError("Não foi possível extrair a versão do LazyGit.")
        lazygit_version = match.group(1)
        # Constrói a URL
        url = f"https://github.com/jesseduffield/lazygit/releases/download/v{lazygit_version}/lazygit_{lazygit_version}_Linux_x86_64.tar.gz"
        log(f"Baixando LazyGit v{lazygit_version}...", BLUE)
        # Executa os comandos
        run_command(f"curl -Lo lazygit.tar.gz {url}")
        run_command("tar xf lazygit.tar.gz lazygit")
        run_command("sudo install lazygit -D -t /usr/local/bin/")
        run_command("rm lazygit lazygit.tar.gz")
        log("LazyGit instalado com sucesso!", BLUE)
    except Exception as e:
        log(f"Erro ao instalar LazyGit: {e}", RED)

def install_lazydocker():
    log("Passo: Instalando lazydocker...", BLUE)
    run_command("curl -s https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash")

def configure_aliases():
    log("Passo: Configurando aliases para exa e bat...", BLUE)
    home = os.path.expanduser("~")
    zshrc = os.path.join(home, ".zshrc")
    aliases = [
        "alias ls='exa --icons'",
        "alias cat='bat'"
    ]
    try:
        if not os.path.exists(zshrc):
            open(zshrc, 'w').close()  # cria .zshrc se não existir
        with open(zshrc, 'r') as file:
            content = file.read()
        with open(zshrc, 'a') as file:
            for alias in aliases:
                if alias not in content:
                    file.write(f"\n{alias}")
        log("Aliases adicionados com sucesso ao .zshrc ✅", GREEN)
    except Exception as e:
        log(f"Erro ao configurar aliases: {e}", RED)

def set_powerlevel10k_theme():
    log("Passo: Configurando o tema Powerlevel10k no .zshrc...", BLUE)
    home = os.path.expanduser("~")
    zshrc_path = os.path.join(home, ".zshrc")
    theme_line = 'ZSH_THEME="powerlevel10k/powerlevel10k"'
    try:
        if os.path.exists(zshrc_path):
            with open(zshrc_path, "r") as f:
                lines = f.readlines()
            found = False
            for i, line in enumerate(lines):
                if line.startswith("ZSH_THEME="):
                    lines[i] = theme_line + "\n"
                    found = True
                    break
            if not found:
                lines.append("\n" + theme_line + "\n")
            with open(zshrc_path, "w") as f:
                f.writelines(lines)
            log("Tema Powerlevel10k configurado no .zshrc com sucesso.", GREEN)
        else:
            with open(zshrc_path, "w") as f:
                f.write(theme_line + "\n")
            log("Arquivo .zshrc criado e tema Powerlevel10k configurado com sucesso.", GREEN)
    except Exception as e:
        log(f"Erro ao configurar o tema Powerlevel10k: {e}", RED)

def set_zsh_plugins():
    log("Passo: Configurando plugins no .zshrc...", BLUE)
    home = os.path.expanduser("~")
    zshrc_path = os.path.join(home, ".zshrc")
    plugins_line = "plugins=( git docker docker-compose python celery zsh-autosuggestions zsh-syntax-highlighting )"
    try:
        if os.path.exists(zshrc_path):
            with open(zshrc_path, "r") as f:
                lines = f.readlines()
            found = False
            for i, line in enumerate(lines):
                if line.startswith("plugins="):
                    lines[i] = plugins_line + "\n"
                    found = True
                    break
            if not found:
                lines.append("\n" + plugins_line + "\n")
            with open(zshrc_path, "w") as f:
                f.writelines(lines)
            log("Plugins configurados no .zshrc com sucesso.", GREEN)
        else:
            with open(zshrc_path, "w") as f:
                f.write(plugins_line + "\n")
            log("Arquivo .zshrc criado e plugins configurados com sucesso.", GREEN)
    except Exception as e:
        log(f"Erro ao configurar plugins no .zshrc: {e}", RED)


def main():
    try:
        request_sudo()
        
        update_upgrade()
        
        install_packages()
        install_basic_tools()
        
        change_default_shell()
        
        install_oh_my_zsh()
        
        setup_zsh_plugins()
        setup_asdf()
        
        update_zshrc()
        
        install_powerlevel10k()
        install_fonts()
        install_docker()
        
        install_rust()
        install_node_pnpm()
        install_golang()
        
        install_uv()
        
        install_btop()
        
        install_lazygit()
        install_lazydocker()
        
        configure_aliases()
        
        set_zsh_plugins()  
        set_powerlevel10k_theme()  # Função para setar o tema no .zshrc
        log("Configuração concluída com sucesso!", GREEN)
    except subprocess.CalledProcessError as e:
        log(f"Ocorreu um erro ao executar o comando: {e.cmd}", RED)
        sys.exit(1)


if __name__ == "__main__":
    main()
