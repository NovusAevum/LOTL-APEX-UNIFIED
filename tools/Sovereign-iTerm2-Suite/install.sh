#!/bin/bash

echo "🚀 Initializing Sovereign iTerm2 Elite Setup"

set -e

xcode-select --install 2>/dev/null || true

if ! command -v brew &> /dev/null; then
  echo "📦 Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install git zsh tmux fzf ripgrep fd bat htop wget curl jq exa neovim neofetch zoxide

brew tap homebrew/cask-fonts || true
brew install --cask font-meslo-lg-nerd-font

brew install --cask iterm2
brew install romkatv/powerlevel10k/powerlevel10k
brew install zsh-syntax-highlighting zsh-autosuggestions

if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo "🧠 Installing Oh My Zsh..."
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

cp zshrc ~/.zshrc
cp p10k.zsh ~/.p10k.zsh

echo 'source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc
echo 'source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc

echo 'export ZSH="$HOME/.oh-my-zsh"' >> ~/.zshrc
echo 'ZSH_THEME="powerlevel10k/powerlevel10k"' >> ~/.zshrc
echo 'plugins=(git zsh-autosuggestions zsh-syntax-highlighting)' >> ~/.zshrc
echo 'source $ZSH/oh-my-zsh.sh' >> ~/.zshrc

brew install --cask docker
brew install --cask visual-studio-code

brew install reattach-to-user-namespace
brew install pbpaste

npm install -g @githubnext/github-copilot-cli || true

echo "✅ Installation complete. Reloading shell..."
exec zsh