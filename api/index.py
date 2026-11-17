"""Função da Vercel que serve a API Flask em /api.

O front-end (React) e a API ficam no mesmo endereço: o vercel.json manda
/api/* para cá e o resto para o build do React. Localmente nada muda:
o servidor continua em backend/ (flask run).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from app import create_app  # noqa: E402

app = create_app()
