import os
import subprocess
import shutil

from constants import (
    GREEN,
    BLUE,
    GREY,
    RED,
    YELLOW,
    RESET,
)


def logg(message, color=BLUE):
    print(f"{color}{message}{RESET}")


def check_command(cmd, description):
    """
    Executa um comando e, se concluir sem erro, considera o teste bem-sucedido.
    """
    try:
        logg(f"Testando: {description}\n  Comando: {cmd}", BLUE)
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logg(f"Sucesso: {description}", GREEN)
        return True
    except subprocess.CalledProcessError:
        logg(f"Falha: {description}", RED)
        return False


def check_path_exists(path, description):
    """
    Verifica se um caminho (diretório ou arquivo) existe.
    """
    logg(f"Verificando {description}: {path}", BLUE)
    if os.path.exists(path):
        logg(f"Sucesso: {description} encontrado.", GREEN)
        return True
    else:
        logg(f"Falha: {description} não encontrado.", RED)
        return False


def check_binary_exists(binary, description):
    """
    Verifica se um binário está presente no PATH.
    """
    logg(f"Verificando {description}: {binary}", BLUE)
    path = shutil.which(binary)
    if path:
        logg(f"Sucesso: {description} encontrado em: {path}", GREEN)
        return True
    else:
        logg(f"Falha: {description} não encontrado no PATH.", RED)
        return False


def clone_repo(repo_url, dest):
    if os.path.exists(dest):
        logg(f"The directory {dest} already exists, skipping clone.", YELLOW)
    else:
        run_command(f"git clone {repo_url} {dest}")


def run_command(cmd, env=None):
    try:
        logg(f"Running: {cmd}", GREY)
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            env=env,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,
        )

    except subprocess.CalledProcessError as e:
        logg(f"Command failed: {cmd}", RED)
        logg(f"Error: {e}", RED)

    except Exception as e:
        logg(f"Unexpected error: {e}", RED)
        raise


def get_user_home():
    """Get the home directory of the user who invoked sudo."""
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return os.path.expanduser(f"~{sudo_user}")

    return os.path.expanduser("~")
