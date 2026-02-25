curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv venv

source .venv/bin/activate

uv pip install -r requirements.txt

make install && make collectstatic && make migrate