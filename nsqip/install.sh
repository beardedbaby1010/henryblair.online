#!/bin/zsh
# NSQIP research kit — one-line installer
#   curl -fsSL https://henryblair.online/nsqip/install.sh | zsh
# Downloads the kit into ~/Documents/NSQIP/NSQIP_ZIP, then runs its setup (run_this_first.zsh).
# Safe to run again: it replaces only the kit folder, never your projects, data, or Google sign-in.
# MIT License · © 2026 Henry M. Blair · henryblair.online

# Everything is inside main(), which only runs on the last line — so a download cut off
# halfway through can never run half a script.
main(){
  emulate -L zsh
  setopt err_return pipe_fail
  local url="${NSQIP_KIT_URL:-https://henryblair.online/nsqip/NSQIP_ZIP.zip}"
  local nsqip="$HOME/Documents/NSQIP" tmp
  local blue=$'\e[38;5;111m' mint=$'\e[38;5;158m' red=$'\e[38;5;203m' c0=$'\e[0m'

  print -r -- "${blue}NSQIP kit installer${c0}"
  [[ $(uname) == Darwin || -n $NSQIP_TEST ]] || { print -r -- "${red}  ✘ this kit is for macOS${c0}"; return 1 }

  # ---- 1. download ----
  tmp=$(mktemp -d)
  print -r -- "${blue}▸ downloading the kit${c0}"
  curl -fSL --progress-bar "$url" -o "$tmp/kit.zip" ||
    { print -r -- "${red}  ✘ couldn't download $url — check your internet and try again${c0}"; return 1 }

  # ---- 2. unzip into ~/Documents/NSQIP (swap the old kit folder only after the new one is complete) ----
  print -r -- "${blue}▸ unpacking into $nsqip${c0}"
  mkdir -p "$nsqip"
  rm -rf "$tmp/x"; mkdir "$tmp/x"
  ditto -x -k "$tmp/kit.zip" "$tmp/x" 2>/dev/null || unzip -q "$tmp/kit.zip" -d "$tmp/x" ||
    { print -r -- "${red}  ✘ the download isn't a valid zip${c0}"; return 1 }
  [[ -f $tmp/x/NSQIP_ZIP/run_this_first.zsh ]] ||
    { print -r -- "${red}  ✘ the zip doesn't contain NSQIP_ZIP/run_this_first.zsh${c0}"; return 1 }
  rm -rf "$nsqip/NSQIP_ZIP.old"
  [[ -d $nsqip/NSQIP_ZIP ]] && mv "$nsqip/NSQIP_ZIP" "$nsqip/NSQIP_ZIP.old"
  mv "$tmp/x/NSQIP_ZIP" "$nsqip/NSQIP_ZIP"
  rm -rf "$nsqip/NSQIP_ZIP.old" "$tmp"
  print -r -- "${mint}  ✔ kit is in $nsqip/NSQIP_ZIP${c0}"

  # ---- 3. run setup, talking to the keyboard (stdin here is the piped script, not you) ----
  print -r -- "${blue}▸ starting setup${c0}"; print
  zsh "$nsqip/NSQIP_ZIP/run_this_first.zsh" < /dev/tty
}
main "$@"
