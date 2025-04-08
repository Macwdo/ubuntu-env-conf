# Linux Development Environment Setup Script

This repository contains scripts to automate the setup of a development environment on Linux, including the installation and configuration of various essential tools. The toolset includes:

- **Zsh** with **Oh My Zsh** and the **Powerlevel10k** theme
- **Git** with global configurations
- **Node.js** (via system package manager) and **pnpm**
- **Rust** (installed via rustup)
- **Docker**
- **Python**
- **Golang**
- Additional utilities and tools such as:  bat, htop, **lazygit**, **lazydocker**, **btop**, and **exa**

## How to Use

### Running the Setup Script

To set up the environment and verify the installation, execute the following steps:

1. Grant execution permission to the script:

    ```bash
    chmod +x run.sh
    ```

2. Run the script:

    ```bash
    ./run.sh
    ```

This script will perform the following actions:

- Request sudo access and keep your session active. **Note**: You may need to provide your password multiple times during the setup process.
- Update and upgrade system packages.
- Install essential packages and basic tools.
- Configure the Zsh shell, installing Oh My Zsh, plugins, and themes.
- Install and configure development tools (Node.js, Rust, Docker, Golang, etc.).
- Add necessary configurations to the `.zshrc` file, including aliases for tools like `exa` and `bat`.
- Verify that the environment has been set up correctly by checking:
  - The presence of essential binaries (such as Git, Zsh, Docker, Node.js, etc.).
  - The existence of configuration directories and files (like `.oh-my-zsh` and `.zshrc`).
  - Other necessary configurations to ensure the environment is ready for use.

The content of `run.sh` is as follows:

```bash
#!/bin/bash
# This script is used to run the Python scripts for installation and testing.

python3 script.py
python3 tests.py
```

To run the setup and tests, simply execute:

```bash
./run.sh
```

## Requirements

- Debian-based Linux distribution (e.g., Ubuntu)
- Sudo access to perform installation and configuration operations

## Notes

- **Script Review**: It is recommended to read and review the scripts (`script.py` and `tests.py`) before running them to understand the changes that will be applied to your system.
- **Terminal Restart**: After execution, restart the terminal to ensure all configurations (such as the Powerlevel10k theme) are applied correctly.
- **Customization**: Feel free to edit and adapt the scripts as needed to meet the requirements of your development environment.
- **Contributions**: If you encounter issues or have suggestions for improvements, contributions are welcome!

---

Download the updated README file below:
[Download README.md](./Readme.md)

# Fixes
- [] Lazydocker was not installed correctly. 
- [] The rust binary is just added after opening a new terminal. So the test fails.


# TODO
- [] Add Terraform
- [] Add Kubernetes (Think about it in WSL 2 Environment)
- [] Fix Script Duplication when set .zshrc plugins
- [] Add Tests.
- [] Add Aws Cli