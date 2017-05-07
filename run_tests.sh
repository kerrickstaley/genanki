#!/bin/bash
# TODO make this cleaner / platform-independent
set -e
anki_test_revision=a98c20a22f3d6e5eb6039bb3e06288dc23c3dec4

install_pyaudio_system_deps() {
  sudo apt-get install -y python-all-dev portaudio19-dev \
  || sudo pacman -S --noconfirm portaudio
}

rm -rf anki_upstream
git clone https://github.com/dae/anki.git anki_upstream
( cd anki_upstream
  git reset --hard $anki_test_revision
  install_pyaudio_system_deps
  sudo pip3 install -r requirements.txt
)

exec python3 setup.py pytest --addopts tests
