"""Small pure UI helpers shared by the declarative view and offline contracts."""

import math


FONT_FAMILY = "Microsoft YaHei UI"


def _valid_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def choice_disabled_reason(choice, energy):
    cost = choice.get("energy_cost")
    if not _valid_number(energy):
        return "当前精力状态不可用"
    if cost is None:
        return None
    if not _valid_number(cost) or cost < 0:
        return "选项数据无效"
    if cost > energy:
        return f"需要精力 {cost}，当前精力 {energy} · 精力不足"
    return None


def handbook_dialog(page, handbook):
    """Open the already-projected handbook without another engine observation."""
    import flet as ft

    page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("入职手册"),
            content=ft.Container(
                width=620,
                height=520,
                content=ft.Column([ft.Text(handbook, size=15, selectable=True)], scroll=ft.ScrollMode.AUTO),
            ),
            actions=[ft.TextButton(content="关闭", on_click=lambda _: page.pop_dialog())],
        )
    )
