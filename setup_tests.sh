#!/bin/bash
# TODO make this cleaner / platform-independent
set -e
anki_test_revision=ed8340a4e3a2006d6285d7adf9b136c735ba2085

# Checks if the first argument is a valid executable in a POSIX-compatible way
command_exists() {
    command -v "$1" >/dev/null
}

# fallback to doas if sudo is not installed
if command_exists sudo; then
    elevator="sudo"
elif command_exists doas; then
    elevator="doas"
else
    echo "error: neither sudo nor doas is installed" 1>&2
    exit 1
fi

# install pyaudio system deps
if command_exists apt-get; then
    $elevator apt-get -y update
    $elevator apt-get install -y python-all-dev portaudio19-dev ripgrep moreutils
elif command_exists pacman; then
    $elevator pacman -S pacman -S --noconfirm --needed portaudio python-virtualenv ripgrep moreutils
elif command_exists xbps-install; then
    $elevator xbps-install --sync --yes portaudio python3-virtualenv ripgrep moreutils
else
    echo "error: couldn't find a suitable package manager"
    exit 1
fi

# enter venv if needed
if [[ -z "$VIRTUAL_ENV" ]]; then
  rm -rf tests_venv
  virtualenv -p python3 tests_venv
  source tests_venv/bin/activate
fi
pip --isolated install .
pip --isolated install 'pytest>=6.0.2'

# clone Anki upstream at specific revision, install dependencies
rm -rf anki_upstream
git clone https://github.com/ankitects/anki.git anki_upstream
( cd anki_upstream
  git reset --hard $anki_test_revision
  pip --isolated install -r requirements.txt
  # patch in commit d261d1e
  rg --replace 'from shutil import which as find_executable' --passthru --no-line-number --multiline 'from distutils\.spawn import[^)]*\)' anki/mpv.py | sponge anki/mpv.py
)
