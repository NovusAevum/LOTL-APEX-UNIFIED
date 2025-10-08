# -- AI Operations Module
function lotl() {
  ollama run mistral --system "You are Lotl..." --prompt "$*"
}
alias ai='ollama run mistral --prompt'
