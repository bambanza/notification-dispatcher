from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

_TEMPLATE_ROOT = Path(__file__).resolve().parent.parent / "templates"

env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_ROOT)),
    autoescape=select_autoescape(["html", "xml"]),
    undefined=StrictUndefined,
)


def render_template(template_name: str, context: dict) -> str:
    return env.get_template(template_name).render(**context)
