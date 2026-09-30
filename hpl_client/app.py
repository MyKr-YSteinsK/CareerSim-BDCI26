"""Flet desktop UI. App startup never instantiates a real engine."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import flet as ft

from hpl_client.controller import HumanGameController
from hpl_client.cleanup import cleanup_success
from hpl_client.fixtures import fixture_controller
from hpl_client.export import readable_filename
from hpl_client.presentation import FONT_FAMILY, choice_disabled_reason, handbook_dialog
from scripts.hpl_play import _load_environment_manifest, resolve_layout


LABELS = {
    "health": "Health · 健康",
    "dignity": "Dignity · 尊严",
    "skill": "Skill · 技能",
    "network": "Network · 人脉",
    "output": "Output · 产出",
    "wealth": "Wealth · 财富",
    "energy": "Energy · 精力",
}
RESULT_LABELS = {
    "grade": "最终评级",
    "survival_months": "生存月份",
    "quantitative_score": "量化得分",
    "competition_partial_score": "竞赛部分得分",
    "outcome": "结局",
}


def panel(controls, *, spacing=16, **kwargs):
    return ft.Container(
        content=ft.Column(controls, spacing=spacing, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, **kwargs),
        padding=20,
        bgcolor="#FFFFFF",
        border_radius=18,
        animate_opacity=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
    )


def game_columns(left, event_content, choice_content):
    """Keep event text and the independently scrolling choice rail as siblings."""
    return ft.Row(
        [
            ft.Container(content=panel(left, spacing=6, scroll=ft.ScrollMode.AUTO), width=238),
            ft.Container(content=panel(event_content, scroll=ft.ScrollMode.AUTO), expand=True),
            ft.Container(content=panel(choice_content, scroll=ft.ScrollMode.AUTO), width=340),
        ],
        expand=True,
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )


def choice_card(choice, energy, on_select, *, disabled=False, index=1):
    reason = choice_disabled_reason(choice, energy)
    blocked = bool(reason) or disabled
    cost = choice.get("energy_cost")
    subtitle = f"需要精力 {cost}" if cost is not None else "可用行动"
    if reason:
        subtitle = reason.replace("，", "\n", 1)
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                f"{index:02d}",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color="#3E7168" if not blocked else "#66757A",
                            ),
                            bgcolor="#E8F1EF" if not blocked else "#EDF0F0",
                            border_radius=8,
                            padding=8,
                        ),
                        ft.Text(
                            choice["action"],
                            size=15,
                            weight=ft.FontWeight.W_600,
                            color="#243A40" if not blocked else "#58676D",
                            expand=True,
                            selectable=True,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Text(subtitle, size=12, color="#536D68" if not blocked else "#596A70", selectable=True),
            ],
            spacing=9,
        ),
        padding=14,
        bgcolor="#F6FAF9" if not blocked else "#F0F2F2",
        border_radius=13,
        border=ft.Border.all(1, "#DCE9E6" if not blocked else "#E1E5E5"),
        on_click=on_select if not blocked else None,
        ink=not blocked,
        animate_opacity=ft.Animation(140, ft.AnimationCurve.EASE_OUT),
    )


def launch(*, fixture=False, fixture_screen="active", smoke_seconds=0, smoke_report=None):
    layout = resolve_layout()
    _load_environment_manifest(layout)
    desktop = layout.sandbox_root / "venv" / "flet-desktop" / "flet"
    if not (desktop / "flet.exe").is_file():
        raise RuntimeError("HPL Flet 1.0.1 desktop runtime is missing; install it into the HPL venv before launch")
    os.environ["FLET_VIEW_PATH"] = str(desktop)
    # Ignore inherited web/Agent launch overrides. Desktop uses local IPC only.
    for name in ("FLET_FORCE_WEB_SERVER", "FLET_DISPLAY_URL_PREFIX", "FLET_SERVER_IP", "FLET_SERVER_PORT"):
        os.environ.pop(name, None)
    controller = (
        fixture_controller(ending=fixture_screen == "ended", energy=1 if fixture_screen == "energy" else 8)
        if fixture
        else HumanGameController()
    )

    async def main(page: ft.Page):
        page.title = "CareerSim Human" + (" · FIXTURE" if fixture else "")
        page.window.width = 1280
        page.window.height = 820
        page.window.min_width = 980
        page.window.min_height = 680
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(font_family=FONT_FAMILY, color_scheme_seed="#386B63", use_material3=True)
        page.bgcolor = "#F2F5FA"
        page.padding = 28
        if fixture and fixture_screen != "start":
            await controller.start()
            if fixture_screen == "ended":
                controller.export_path = Path(
                    readable_filename(
                        {"human_tag": "local", "ended_at": "2026-09-30T21:45:30+08:00"},
                        [controller.view.projection],
                    )
                )
                controller.export_message = "离线展示：以下为数据包文件名示例，未生成真实对局包。"

        @ft.component
        def Client():
            tick, refresh = ft.use_state(0)
            tag, set_tag = ft.use_state("local")
            pending, set_pending = ft.use_state(False)
            message, set_message = ft.use_state("")
            show_history, set_show_history = ft.use_state(False)

            async def start(_):
                if controller.busy:
                    return
                set_pending(True)
                set_message("")
                await asyncio.sleep(0)
                await controller.start(tag)
                set_pending(False)
                refresh(tick + 1)

            async def action(choice, revision, run_id):
                if controller.busy:
                    return
                set_pending(True)
                await asyncio.sleep(0)
                await controller.choose(choice, revision, run_id)
                set_pending(False)
                refresh(lambda value: value + 1)

            async def finalize(_):
                set_pending(True)
                try:
                    if fixture:
                        set_message("Fixture 不生成真实运行资料；ZIP 由离线测试验证。")
                    elif controller.finalization_status == "CLEANUP_PENDING" and controller.export_path:
                        await asyncio.to_thread(
                            cleanup_success, controller.recorder.root, controller.export_path, resolve_layout()
                        )
                        controller.finalization_status = "SUCCESSFULLY_FINALIZED_AND_EXPORTED"
                        controller.export_message = "临时文件已清理。"
                        set_message(controller.export_message + "\n" + str(controller.export_path))
                    else:
                        await controller.finish_export()
                        set_message(
                            controller.export_message
                            + ("\n" + str(controller.export_path) if controller.export_path else "")
                        )
                except Exception:
                    set_message("导出未完成，本局资料已保留。")
                finally:
                    set_pending(False)
                    refresh(lambda value: value + 1)

            def open_handbook(_):
                handbook_dialog(page, facts.get("handbook", ""))

            header = ft.Row(
                [
                    ft.Text("CareerSim Human", size=28, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text("Local  /  No LLM  /  HPL", color="#526480"),
                ]
            )
            footer = ft.Text(
                "所有资料保留在本机 · 由你选择每一步" + (" · FIXTURE / NO GAME" if fixture else ""),
                color="#526480",
                size=12,
            )
            if not controller.view:
                return ft.Column(
                    [
                        header,
                        ft.Container(height=32),
                        panel(
                            [
                                ft.Text("你的职业故事，从这里开始", size=32, weight=ft.FontWeight.BOLD),
                                ft.Text("阅读事件，做出选择，探索一条属于你的路线。", size=17),
                                ft.TextField(
                                    label="参与者标签（可选昵称）",
                                    value=tag,
                                    max_length=64,
                                    on_change=lambda e: set_tag(e.control.value),
                                ),
                                ft.Button(content="开始新游戏", on_click=start, disabled=pending),
                                ft.Text(controller.error, color="#B42318") if controller.error else ft.Text(""),
                            ]
                        ),
                        ft.Container(expand=True),
                        footer,
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )

            view = controller.view
            facts = view.facts
            state = facts["state"]
            title = f"Year {state.get('year', '—')} · Q{state.get('quarter', '—')} · Month {state.get('month', '—')}  /  {state.get('level', '—')}"
            stats = [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(label, size=12, color="#586B78"),
                            ft.Text(str(state.get(key, "—")), size=18, weight=ft.FontWeight.W_600, color="#23343D"),
                        ],
                        spacing=2,
                    ),
                    bgcolor="#F3F7F6",
                    border_radius=11,
                    padding=6,
                    animate_opacity=ft.Animation(140, ft.AnimationCurve.EASE_OUT),
                )
                for key, label in LABELS.items()
            ]
            left = [ft.Text("当前状态", size=18, weight=ft.FontWeight.W_600, color="#23343D"), *stats]

            event = facts.get("event", {})
            center = [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "本局完成" if controller.phase == "ENDED" else event.get("title", "事件"),
                                    size=25,
                                    weight=ft.FontWeight.W_600,
                                    color="#23343D",
                                ),
                                ft.Text("当前事件与公开反馈", size=13, color="#647780"),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ]
            if controller.phase != "ENDED" and event.get("description"):
                center.append(ft.Text(event["description"], size=16, color="#354951", selectable=True))
            if facts.get("warning"):
                center.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("公开反馈", size=13, weight=ft.FontWeight.W_600, color="#765820"),
                                ft.Text(facts["warning"], size=14, color="#594B2F", selectable=True, expand=True),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        bgcolor="#FFF7E5",
                        border_radius=12,
                        padding=14,
                    )
                )
            if controller.error:
                center.append(
                    ft.Container(
                        content=ft.Text(controller.error, size=14, color="#9E3F38"),
                        bgcolor="#FFF0EE",
                        border_radius=11,
                        padding=12,
                    )
                )
            if controller.phase == "ENDED":
                center.append(ft.Divider(height=12, color="#E7ECEA"))
                center.append(ft.Text("本局完成", size=24, weight=ft.FontWeight.W_600, color="#315F57"))
                center.append(ft.Text(f"最终职级 · {state.get('level', 'LNA')}", size=17, color="#315F57"))
                center.extend(
                    ft.Row(
                        [
                            ft.Text(RESULT_LABELS[key], size=14, color="#647780"),
                            ft.Container(expand=True),
                            ft.Text(str(value), size=17, weight=ft.FontWeight.W_600, color="#23343D"),
                        ]
                    )
                    for key, value in facts.get("final_result", {}).items()
                )
                if controller.finalization_status == "EXPORTING":
                    center.append(ft.ProgressBar())
                if controller.export_message:
                    center.append(ft.Text(controller.export_message, size=14, color="#315F57"))
                if controller.export_path:
                    center.append(ft.Text(str(controller.export_path), size=13, selectable=True, color="#354951"))
                if message:
                    center.append(ft.Text(message, selectable=True, color="#354951"))
            elif controller.phase == "TECHNICAL_FAILURE":
                center.extend(
                    [
                        ft.Text("本局资料已保留，技术失败局不会自动清理。", size=14, color="#765820"),
                        ft.Text(str(controller.recorder.root), size=13, selectable=True, color="#354951")
                        if controller.recorder
                        else ft.Text("本局尚未建立运行目录。"),
                        ft.Button(content="开始新游戏", on_click=start, disabled=pending or controller.busy),
                    ]
                )

            choices = [ft.Text("当前选择", size=18, weight=ft.FontWeight.W_600, color="#23343D")]
            if controller.rejection:
                choices.append(ft.Text(controller.rejection, size=13, color="#9B5146", selectable=True))
            if pending or controller.busy:
                choices.append(ft.ProgressBar())
            if controller.phase == "ACTIVE":
                for index, choice in enumerate(facts.get("choices", []), start=1):

                    async def select(_, value=choice["choice"], revision=view.revision, run_id=view.run_id):
                        await action(value, revision, run_id)

                    choices.append(
                        choice_card(
                            choice, state.get("energy"), select, disabled=pending or controller.busy, index=index
                        )
                    )
            if controller.phase == "ENDED":
                if controller.finalization_status != "SUCCESSFULLY_FINALIZED_AND_EXPORTED":
                    choices.append(
                        ft.TextButton(content="导出本局数据", on_click=finalize, disabled=pending or controller.busy)
                    )
                choices.append(ft.TextButton(content="重新开始", on_click=start, disabled=pending or controller.busy))
            if controller.phase == "TECHNICAL_FAILURE":
                choices.append(ft.Text("技术失败资料已留存", size=13, color="#765820"))
            if controller.phase == "ACTIVE":
                choices.append(ft.Divider(height=8, color="#E7ECEA"))
                choices.append(
                    ft.TextButton(
                        content=f"最近选择 · {len(controller.history)}",
                        on_click=lambda _: set_show_history(not show_history),
                    )
                )
                if show_history:
                    choices.extend(
                        ft.Text(item["action"], size=13, color="#586B78", selectable=True)
                        for item in reversed(controller.history)
                    )
            choices.append(ft.Text("Local · No LLM · HPL", size=12, color="#647780"))
            return ft.Column(
                [
                    header,
                    ft.Text(title, size=18, color="#526480"),
                    game_columns(left, center, choices),
                    ft.Row([ft.TextButton(content="查看入职手册", on_click=open_handbook), footer]),
                ],
                expand=True,
            )

        page.render(Client)
        if fixture and fixture_screen == "handbook":
            handbook_dialog(page, controller.view.facts.get("handbook", ""))
        if smoke_report:
            await asyncio.sleep(1)
            Path(smoke_report).write_text(
                json.dumps(
                    {
                        "fixture": fixture,
                        "phase": controller.phase,
                        "page_session_connected": True,
                        "real_engine_imported": "career_emulator.game" in sys.modules,
                    }
                ),
                encoding="utf-8",
            )
        if smoke_seconds:
            await asyncio.sleep(smoke_seconds)
            await page.window.close()

    ft.run(main, host="127.0.0.1", no_cdn=True, assets_dir=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument(
        "--fixture-screen", choices=("start", "active", "energy", "ended", "handbook"), default="active"
    )
    parser.add_argument("--smoke-seconds", type=int, default=0)
    parser.add_argument("--smoke-report")
    args = parser.parse_args()
    if (args.smoke_seconds or args.smoke_report) and not args.fixture:
        parser.error("smoke controls require --fixture; no real game is permitted")
    launch(
        fixture=args.fixture,
        fixture_screen=args.fixture_screen,
        smoke_seconds=args.smoke_seconds,
        smoke_report=args.smoke_report,
    )


if __name__ == "__main__":
    main()
