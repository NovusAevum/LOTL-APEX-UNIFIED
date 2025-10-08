# Deferred Tactical Greeting
source "$HOME/.zsh/zsh-defer.zsh"
zsh-defer greet_lotl() {
  [[ "$LOTL_QUIET" == "1" || -n "$LOTLSH_GREETED" ]] && return
  local NOW=$(date "+%Y-%m-%d %H:%M:%S")
  local HOUR=$(date +"%H")
  local SALUTE="🌙 Good evening"
  (( HOUR < 12 )) && SALUTE="☀️ Good morning"
  (( HOUR >= 12 && HOUR < 18 )) && SALUTE="🌤️ Good afternoon"
  local QUOTES=(
    "🛰️ Map the data, or be mapped by it."
    "📡 Silence is your stealth. Emissions are exposure."
    "🧠 Every flag captured begins with a ping."
    "🔐 Authentication is negotiation in disguise."
  )
  local MISSIONS=(
    "🧪 Review Git diffs and validate PR pipeline"
    "📦 Check Docker container uptime and ports"
  )
  local QUOTE="${QUOTES[$((RANDOM % ${#QUOTES[@]}))]}"
  local MISSION="${MISSIONS[$((RANDOM % ${#MISSIONS[@]}))]}"
  if command -v figlet &>/dev/null && command -v lolcat &>/dev/null; then
    figlet -f slant "HANIS COMMAND CENTRE" | lolcat
  else
    echo "🔱 HANIS COMMAND CENTRE"
  fi
  echo "$SALUTE, Supreme Commander Hanis. 🎖️ LotL agents standing by."
  echo "$QUOTE"
  echo "$MISSION"
  echo ""
  mkdir -p "$HOME/.lotl_logs"
  echo "$NOW | $SALUTE | $QUOTE | $MISSION" >> "$HOME/.lotl_logs/lotl_sessions.log"
  export LOTLSH_GREETED=1
}
