curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv pip install -r requirements.txt

make create-venv && make activate-venv && make install && make collectstatic && make migrate