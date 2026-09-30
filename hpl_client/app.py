"""Flet desktop UI. App startup never instantiates a real engine."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import flet as ft

from hpl_client.controller import HumanGameController
from hpl_client.export import export_run
from hpl_client.fixtures import fixture_controller
from scripts.hpl_play import _load_environment_manifest, resolve_layout


LABELS = {
    "health": "健康",
    "dignity": "尊严",
    "skill": "技能",
    "network": "人脉",
    "output": "产出",
    "wealth": "财富",
    "energy": "精力",
}
RESULT_LABELS = {
    "grade": "等级",
    "survival_months": "生存月份",
    "quantitative_score": "量化得分",
    "competition_partial_score": "竞赛部分得分",
    "outcome": "结局",
}


def panel(controls, **kwargs):
    return ft.Container(
        content=ft.Column(controls, spacing=16, **kwargs), padding=24, bgcolor="#FFFFFF", border_radius=20
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
    controller = fixture_controller(ending=fixture_screen == "ended") if fixture else HumanGameController()

    async def main(page: ft.Page):
        page.title = "CareerSim Human" + (" · FIXTURE" if fixture else "")
        page.window.width = 1100
        page.window.height = 700
        page.window.min_width = 900
        page.window.min_height = 650
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = "#F2F5FA"
        page.padding = 28
        if fixture and fixture_screen != "start":
            await controller.start()

        @ft.component
        def Client():
            tick, refresh = ft.use_state(0)
            tag, set_tag = ft.use_state("local")
            pending, set_pending = ft.use_state(False)
            message, set_message = ft.use_state("")

            async def start(_):
                if controller.busy:
                    return
                set_pending(True)
                set_message("")
                await controller.start(tag)
                set_pending(False)
                refresh(tick + 1)

            async def action(choice, revision, run_id):
                if controller.busy:
                    return
                set_pending(True)
                await asyncio.sleep(0)  # Let Flet render the disabled/loading state.
                await controller.choose(choice, revision, run_id)
                set_pending(False)
                refresh(lambda value: value + 1)

            def export(_):
                try:
                    if fixture:
                        set_message("Fixture 不生成真实运行资料；ZIP 由离线测试验证。")
                    else:
                        set_message("已导出：" + str(export_run(controller.recorder.root)))
                except Exception:
                    set_message("导出验证未通过。请保留本地 evidence，不分享未验证资料。")

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
            left = panel(
                [ft.Text("当前状态", weight=ft.FontWeight.BOLD, size=18)]
                + [
                    ft.Row(
                        [
                            ft.Text(label, color="#526480"),
                            ft.Container(expand=True),
                            ft.Text(str(state.get(key, "—")), size=22, weight=ft.FontWeight.BOLD),
                        ]
                    )
                    for key, label in LABELS.items()
                ]
            )
            center = []
            if controller.error:
                center.append(ft.Text(controller.error, color="#B42318", size=16))
            if facts.get("warning"):
                center.append(
                    ft.Container(
                        content=ft.Text(facts["warning"], size=15), padding=16, bgcolor="#FFF4D6", border_radius=12
                    )
                )
            if controller.phase == "ENDED":
                center.extend(
                    [ft.Text("本局结束", size=28, weight=ft.FontWeight.BOLD)]
                    + [
                        ft.Text(f"{RESULT_LABELS[key]}: {value}", size=18)
                        for key, value in facts.get("final_result", {}).items()
                    ]
                )
            else:
                event = facts.get("event", {})
                center.extend(
                    [
                        ft.Text(event.get("title", "本局已停止"), size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(event.get("description", ""), size=17, selectable=True),
                    ]
                )
                for choice in facts.get("choices", []):

                    async def select(_, value=choice["choice"], revision=view.revision, run_id=view.run_id):
                        await action(value, revision, run_id)

                    cost = f"  ·  精力 {choice['energy_cost']}" if "energy_cost" in choice else ""
                    center.append(
                        ft.Button(
                            content=ft.Text(choice["action"] + cost, size=16),
                            on_click=select,
                            disabled=pending or controller.phase != "ACTIVE",
                        )
                    )
            if pending:
                center.append(ft.ProgressBar())
            if controller.phase in ("ENDED", "TECHNICAL_FAILURE"):
                center.extend(
                    [
                        ft.Button(content="导出本局数据", on_click=export),
                        ft.Button(content="开始新游戏", on_click=start, disabled=pending),
                    ]
                )
            if message:
                center.append(ft.Text(message, selectable=True))
            right = panel(
                [
                    ft.Text("入职手册", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(facts.get("handbook", ""), size=14, selectable=True),
                    ft.Text("最近选择", size=18, weight=ft.FontWeight.BOLD),
                ]
                + [ft.Text(item["action"], size=14) for item in controller.history]
                + [ft.Text("Run · " + view.run_id, size=11, selectable=True)],
                scroll=ft.ScrollMode.AUTO,
            )
            return ft.Column(
                [
                    header,
                    ft.Text(title, size=18, color="#526480"),
                    ft.Row(
                        [
                            ft.Container(content=left, width=205),
                            ft.Container(content=panel(center, scroll=ft.ScrollMode.AUTO), expand=True),
                            ft.Container(content=right, width=255),
                        ],
                        expand=True,
                        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    footer,
                ],
                expand=True,
            )

        page.render(Client)
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
    parser.add_argument("--fixture-screen", choices=("start", "active", "ended"), default="active")
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
