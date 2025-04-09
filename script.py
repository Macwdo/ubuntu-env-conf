import os
import re
import subprocess
import sys
import shutil

from constants import (
    GREEN,
    BLUE,
    RED,
    YELLOW,
    RESET,
)
from utils import logg, run_command, get_user_home


def clone_repo(repo_url, dest):
    """
    Clone a git repository to the destination directory only if not already present.
    """
    if os.path.exists(dest) and os.listdir(dest):
        logg(f"Repository already exists at {dest}. Skipping clone.", YELLOW)
        return
    logg(f"Starting clone of repository {repo_url} to {dest}...", BLUE)
    try:
        run_command(f"git clone {repo_url} {dest}")
        logg(f"Repository cloned to {dest}.", GREEN)
    except Exception as e:
        logg(f"Error cloning repository {repo_url}: {e}", RED)


def update_upgrade():
    logg("Starting update and upgrade of packages...", BLUE)
    try:
        # Check if apt update/upgrade are needed (could parse output, for now always run)
        run_command("apt update -y")
        run_command("apt upgrade -y")
        logg("Packages updated and upgraded successfully.", GREEN)
    except Exception as e:
        logg(f"Error during update/upgrade: {e}", RED)


def install_packages():
    logg("Starting installation of essential packages...", BLUE)
    apt_packages = (
        "build-essential curl libbz2-dev libffi-dev liblzma-dev libncursesw5-dev "
        "libreadline-dev libsqlite3-dev libssl-dev libxml2-dev libxmlsec1-dev llvm "
        "make tk-dev wget xz-utils zlib1g-dev"
    )
    try:
        # We could check if dpkg -l shows these packages but here we assume idempotence
        run_command(f"apt install -y {apt_packages}")
        logg("Essential packages installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing essential packages: {e}", RED)


def install_basic_tools():
    logg("Starting installation of basic tools...", BLUE)
    try:
        run_command("apt install -y zsh git wget curl unzip")
        logg("Basic tools installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing basic tools: {e}", RED)


def change_default_shell():
    logg("Starting change of default shell to zsh...", BLUE)
    try:
        # Check if the shell is already zsh
        current_shell = os.environ.get("SHELL", "")
        if "zsh" in current_shell:
            logg("Default shell is already zsh. Skipping change.", YELLOW)
            return
        subprocess.run(
            "chsh -s $(which zsh)",
            shell=True,
            check=True,
            timeout=10,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logg("Default shell changed to zsh successfully.", GREEN)
    except subprocess.TimeoutExpired:
        logg(
            "chsh timed out. Please change the shell manually with 'chsh -s $(which zsh)'.",
            YELLOW,
        )
    except KeyboardInterrupt:
        logg(
            "Shell change canceled by user. Run 'chsh -s $(which zsh)' manually if desired.",
            YELLOW,
        )
    except subprocess.CalledProcessError as e:
        logg(f"Error while changing shell: {e}", RED)
    except Exception as e:
        logg(f"Unexpected error while changing shell: {e}", RED)


def install_oh_my_zsh():
    logg("Starting installation of Oh My Zsh...", BLUE)
    try:
        home = get_user_home()
        ohmyzsh_dir = os.path.join(home, ".oh-my-zsh")
        if os.path.exists(ohmyzsh_dir):
            logg("Oh My Zsh directory already exists. Skipping installation.", YELLOW)
            return
        env = os.environ.copy()
        env["RUNZSH"] = "no"
        env["CHSH"] = "no"
        run_command(
            'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
            env=env,
        )
        logg("Oh My Zsh installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing Oh My Zsh: {e}", RED)


def install_zsh_plugins():
    logg("Starting configuration of Zsh plugins...", BLUE)
    try:
        home = get_user_home()
        custom_plugins_dir = os.path.join(home, ".oh-my-zsh", "custom", "plugins")
        os.makedirs(custom_plugins_dir, exist_ok=True)

        plugins = {
            "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions.git",
            "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting.git",
        }

        for name, repo_url in plugins.items():
            dest = os.path.join(custom_plugins_dir, name)
            if os.path.isdir(dest) and os.listdir(dest):
                logg(f"Plugin '{name}' already installed. Skipping.", YELLOW)
            else:
                try:
                    run_command(f"git clone {repo_url} {dest}")
                    logg(f"Plugin '{name}' installed successfully.", GREEN)
                except Exception as e:
                    logg(f"Error cloning plugin '{name}': {e}", RED)
        logg("Zsh plugins configured successfully.", GREEN)
    except Exception as e:
        logg(f"Error configuring Zsh plugins: {e}", RED)


def install_powerlevel10k():
    logg("Starting installation of Powerlevel10k...", BLUE)
    try:
        home = get_user_home()
        omz_custom = os.path.join(home, ".oh-my-zsh", "custom")
        themes_dir = os.path.join(omz_custom, "themes")
        os.makedirs(themes_dir, exist_ok=True)
        dest = os.path.join(themes_dir, "powerlevel10k")
        if os.path.exists(dest) and os.listdir(dest):
            logg("Powerlevel10k is already installed. Skipping.", YELLOW)
        else:
            clone_repo("https://github.com/romkatv/powerlevel10k.git --depth=1", dest)
        logg("Powerlevel10k installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing Powerlevel10k: {e}", RED)


def install_fonts():
    logg("Starting installation of fonts (Nerd Fonts and JetBrains Mono)...", BLUE)
    try:
        home = get_user_home()
        fonts_dir = os.path.join(home, ".local", "share", "fonts")
        os.makedirs(fonts_dir, exist_ok=True)

        fonts = {
            "MesloLGS NF Regular.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf",
            "MesloLGS NF Bold.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf",
            "MesloLGS NF Italic.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf",
            "MesloLGS NF Bold Italic.ttf": "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf",
        }
        for filename, url in fonts.items():
            dest_file = os.path.join(fonts_dir, filename)
            if os.path.exists(dest_file):
                logg(f"Font '{filename}' already installed. Skipping.", YELLOW)
            else:
                run_command(f'wget -O "{dest_file}" "{url}"')
                logg(f"Font '{filename}' downloaded successfully.", GREEN)
        run_command("fc-cache -fv")
        logg("Font cache updated for Nerd Fonts.", GREEN)

        # Install JetBrains Mono font
        jetbrains_zip = os.path.join("/tmp", "jetbrains-mono.zip")
        jetbrains_url = "https://download.jetbrains.com/fonts/JetBrainsMono-2.242.zip"
        run_command(f'wget -O {jetbrains_zip} "{jetbrains_url}"')
        extract_dir = os.path.join("/tmp", "jetbrains-mono")
        os.makedirs(extract_dir, exist_ok=True)
        run_command(f"unzip -o {jetbrains_zip} -d {extract_dir}")
        for root, _, files in os.walk(extract_dir):
            for file in files:
                if file.lower().endswith((".ttf", ".otf")):
                    full_path = os.path.join(root, file)
                    shutil.copy(full_path, fonts_dir)
                    logg(f"Copied font '{file}' to fonts directory.", BLUE)
        run_command("fc-cache -fv")
        logg("Font cache updated for JetBrains Mono.", GREEN)
    except Exception as e:
        logg(f"Error installing fonts: {e}", RED)


def install_docker():
    logg("Starting installation of Docker...", BLUE)
    try:
        # A deeper check could be done (e.g. check if docker daemon is running)
        run_command("apt install -y docker.io")
        run_command("systemctl enable --now docker")
        run_command("usermod -aG docker $USER")
        logg(
            "Docker installed successfully. Please log out/in to apply changes.", GREEN
        )
    except Exception as e:
        logg(f"Error installing Docker: {e}", RED)


def install_aws_cli():
    logg("Starting installation of AWS CLI...", BLUE)
    try:
        run_command(
            'curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"'
        )
        run_command("unzip awscliv2.zip")
        run_command("./aws/install")
        run_command("rm awscliv2.zip")
        run_command("rm -rf aws")
        logg("AWS CLI installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing AWS CLI: {e}", RED)


def _update_rust_env():
    logg("Starting update of Rust environment...", BLUE)
    try:
        rust_bin = os.path.expanduser("~/.cargo/bin")
        if os.path.isdir(rust_bin):
            os.environ["PATH"] = f"{rust_bin}:" + os.environ["PATH"]
            logg("Rust environment updated successfully.", GREEN)
        else:
            logg("Rust directory not found. Check the installation.", RED)
    except Exception as e:
        logg(f"Error updating Rust environment: {e}", RED)


def install_rust():
    logg("Starting installation of Rust...", BLUE)
    try:
        run_command(
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
        )
        _update_rust_env()
        run_command("cargo install exa bat")
        logg("Rust and additional packages (exa, bat) installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing Rust: {e}", RED)


def install_uv():
    logg("Starting installation of UV (requires Rust)...", BLUE)
    try:
        run_command("cargo install --git https://github.com/astral-sh/uv uv")
        logg("UV installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing UV: {e}", RED)


def install_node_pnpm():
    logg("Starting installation of Node.js, npm, and pnpm...", BLUE)
    try:
        run_command("apt install -y nodejs npm")
        run_command("npm install -g pnpm")
        logg("Node.js, npm, and pnpm installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing Node.js, npm, or pnpm: {e}", RED)


def install_golang():
    logg("Starting installation of Golang...", BLUE)
    try:
        run_command("apt install -y golang-go")
        logg("Golang installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing Golang: {e}", RED)


def install_btop():
    logg("Starting installation of btop...", BLUE)
    try:
        run_command("apt install -y btop")
        logg("btop installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing btop: {e}", RED)


def install_lazygit():
    logg("Starting installation of LazyGit...", BLUE)
    try:
        version_json = subprocess.check_output(
            'curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest"',
            shell=True,
        ).decode()
        match = re.search(r'"tag_name":\s*"v?([^"]+)"', version_json)
        if not match:
            logg("Error: Unable to find LazyGit version.", RED)

        lazygit_version = match.group(1)
        url = f"https://github.com/jesseduffield/lazygit/releases/download/v{lazygit_version}/lazygit_{lazygit_version}_Linux_x86_64.tar.gz"
        logg(f"Downloading LazyGit v{lazygit_version}...", BLUE)
        run_command(f"curl -Lo lazygit.tar.gz {url}")
        run_command("tar xf lazygit.tar.gz lazygit")
        run_command("install lazygit -D -t /usr/local/bin/")
        run_command("rm lazygit lazygit.tar.gz")
        logg("LazyGit installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing LazyGit: {e}", RED)


def install_lazydocker():
    logg("Starting installation of lazydocker...", BLUE)
    try:
        run_command(
            "curl -s https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash"
        )
        logg("lazydocker installed successfully.", GREEN)
    except Exception as e:
        logg(f"Error installing lazydocker: {e}", RED)


def configure_aliases():
    logg("Starting configuration of aliases for exa and bat...", BLUE)
    try:
        home = get_user_home()
        zshrc = os.path.join(home, ".zshrc")
        aliases = ["alias ls='exa --icons'", "alias cat='bat'"]
        if not os.path.exists(zshrc):
            open(zshrc, "w").close()
            logg("Created new .zshrc file.", BLUE)
        with open(zshrc, "r") as file:
            content = file.read()
        with open(zshrc, "a") as file:
            for alias in aliases:
                if alias not in content:
                    file.write(f"\n{alias}")
                    logg(f"Alias added: {alias}", BLUE)
        logg("Aliases configured successfully in .zshrc.", GREEN)
    except Exception as e:
        logg(f"Error configuring aliases: {e}", RED)


def set_powerlevel10k_theme():
    logg("Starting configuration of Powerlevel10k theme in .zshrc...", BLUE)
    try:
        home = get_user_home()
        zshrc_path = os.path.join(home, ".zshrc")
        theme_line = 'ZSH_THEME="powerlevel10k/powerlevel10k"'
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
            logg("Powerlevel10k theme configured in .zshrc successfully.", GREEN)
        else:
            with open(zshrc_path, "w") as f:
                f.write(theme_line + "\n")
            logg(
                ".zshrc file created and Powerlevel10k theme configured successfully.",
                GREEN,
            )
    except Exception as e:
        logg(f"Error configuring Powerlevel10k theme: {e}", RED)


def set_zsh_plugins():
    logg("Starting configuration of plugins in .zshrc...", BLUE)
    try:
        home = get_user_home()
        zshrc_path = os.path.join(home, ".zshrc")
        plugins_line = "plugins=( git docker docker-compose python celery zsh-autosuggestions zsh-syntax-highlighting )"
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
            logg("Plugins configured in .zshrc successfully.", GREEN)
        else:
            with open(zshrc_path, "w") as f:
                f.write(plugins_line + "\n")
            logg(".zshrc file created and plugins configured successfully.", GREEN)
    except Exception as e:
        logg(f"Error configuring plugins in .zshrc: {e}", RED)


def main():
    logg("Starting full configuration...", BLUE)
    try:
        update_upgrade()
        install_packages()
        install_basic_tools()
        change_default_shell()
        install_oh_my_zsh()
        install_zsh_plugins()
        install_powerlevel10k()
        install_fonts()
        # Uncomment if Docker installation is required
        # install_docker()
        install_aws_cli()
        install_rust()
        install_node_pnpm()
        install_golang()
        install_uv()
        install_btop()
        install_lazygit()
        install_lazydocker()
        configure_aliases()
        set_zsh_plugins()
        set_powerlevel10k_theme()
        logg("Configuration completed successfully!", GREEN)
    except subprocess.CalledProcessError as e:
        logg(f"An error occurred while executing a command: {e.cmd}", RED)
        sys.exit(1)
    except Exception as e:
        logg(f"Configuration failed: {e}", RED)
        sys.exit(1)


if __name__ == "__main__":
    main()
