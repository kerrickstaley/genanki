#!/bin/bash
# TODO make this cleaner / platform-independent
set -e
anki_test_revision=a98c20a22f3d6e5eb6039bb3e06288dc23c3dec4

install_pyaudio() {
  # pyaudio requires other non-Python dependencies, so we install it through
  # the system package manager before installing Anki's Python dependencies
  # (it will get skipped by pip)
  sudo apt-get install -y python3-pyaudio \
  || sudo pacman -S --noconfirm python-pyaudio
}

rm -rf anki_upstream
git clone https://github.com/dae/anki.git anki_upstream
( cd anki_upstream
  git reset --hard $anki_test_revision
  install_pyaudio
  sudo pip install -r requirements.txt
)

exec python setup.py pytest --addopts tests
