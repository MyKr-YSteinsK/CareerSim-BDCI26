"""Real installed Flet control contracts; synthetic content, no engine import."""

import subprocess
from pathlib import Path

from scripts.hpl_play import resolve_layout


def test_installed_flet_three_columns_wrap_gates_font_and_handbook():
    python = resolve_layout().sandbox_root / "venv/Scripts/python.exe"
    source = r"""
import sys
from types import SimpleNamespace
import flet as ft
from hpl_client.app import game_columns, choice_card
from hpl_client.presentation import FONT_FAMILY, handbook_dialog
assert ft.Theme(font_family=FONT_FAMILY).font_family == "Microsoft YaHei UI"
short = game_columns([ft.Text("state")], [ft.Text("event")], [ft.Text("choice")])
long = game_columns([ft.Text("state")], [ft.Text("event" * 1000)], [ft.Text("choice")])
for layout in (short, long):
    assert len(layout.controls) == 3 and layout.expand is True
    assert layout.controls[0].width == 238 and layout.controls[2].width == 340
    assert layout.controls[1].expand is True
    assert layout.vertical_alignment == ft.CrossAxisAlignment.STRETCH
    assert all(column.content.content.scroll == ft.ScrollMode.AUTO for column in layout.controls)
choice = {"choice": 1, "action": "很长的中文行动描述" * 30, "energy_cost": 2}
blocked = choice_card(choice, 1, lambda _: None)
valid = choice_card(choice, 2, lambda _: None)
assert blocked.on_click is None and valid.on_click is not None
assert "精力不足" in blocked.content.controls[1].value
text = valid.content.controls[0].controls[1]
assert text.expand is True and text.max_lines is None and text.no_wrap is not True
shown = []
page = SimpleNamespace(show_dialog=shown.append, pop_dialog=lambda: shown.append("closed"))
handbook_dialog(page, "已经过滤的公开手册")
dialog = shown[0]
assert isinstance(dialog, ft.AlertDialog) and dialog.modal
assert dialog.content.content.controls[0].value == "已经过滤的公开手册"
dialog.actions[0].on_click(None)
assert shown[-1] == "closed"
assert "career_emulator.game" not in sys.modules
print("six UI contracts PASS / NO GAME")
"""
    result = subprocess.run(
        [str(python), "-c", source],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "six UI contracts PASS" in result.stdout
