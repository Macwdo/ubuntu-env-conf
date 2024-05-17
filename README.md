# ubuntu-env-conf
- This repository is basiclly my ubuntu env configuration

# Updating everything
sudo apt update -y
sudo apt upgrade -y

```bash
sudo apt install \
    build-essential \
    curl \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev
```
# Installing vscode and discord
```
snap install code 

snap install discord
```
# Basic tools
```
sudo apt install zsh git wget curl
```

# Installing  Oh my zsh
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

# Auto suggestions
```
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

# Syntax Highlighting
```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```

# Asdf plugin
```
https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/asdf
```

# Add oh my zsh plugins
plugins=(
    git
    asdf
    docker
    docker-compose
    python
    celery
    zsh-autosuggestions
    zsh-syntax-highlighting 
    )

# Install p10k
```
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

# Add theme
ZSH_THEME="powerlevel10k/powerlevel10k"

# Install nerd fonts
https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf

https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf

https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf

https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# Install Jet brains font
https://www.jetbrains.com/pt-br/lp/mono/

# Install docker 
https://docs.docker.com/engine/install/ubuntu/

# Install Rust and tools
cargo install exa bat

# Bash Top

https://github.com/aristocratos/bashtop




