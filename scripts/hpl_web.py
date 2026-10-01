"""HPL-05 local launcher. Defaults to fixture; server startup never creates a game."""

import argparse
import json
import os
import sys
import webbrowser
from pathlib import Path

WORKTREE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKTREE))

from hpl_client.controller import HumanGameController  # noqa: E402
from hpl_client.web import LocalWebServer, WebApplication, fixture_controller, web_human_factory  # noqa: E402
from scripts.hpl_web_runtime import loaded_native_modules, runtime_root, startup_check  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--human", action="store_true", help="Future explicitly authorized user Start only")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--ready-file", type=Path, help="Trusted local smoke evidence path")
    args = parser.parse_args()
    root = runtime_root()
    app = server = None
    try:
        startup_check()
        # Import only: prove the direct runtime can load; never construct GameEngine.
        from career_emulator.game import GameEngine  # noqa: F401

        controller = HumanGameController(web_human_factory) if args.human else fixture_controller(root)
        app = WebApplication(controller, fixture=not args.human)
        server = LocalWebServer(app)
        if args.ready_file:
            target = args.ready_file.absolute()
            if not target.resolve().is_relative_to(root.resolve()) or target.exists():
                raise RuntimeError("Ready evidence must be a fresh file inside HPL-05 runtime")
            target.write_text(
                json.dumps(
                    {
                        "url": server.origin,
                        "pid": os.getpid(),
                        "native_modules": loaded_native_modules(),
                        "mode": "HUMAN" if args.human else "FIXTURE / NON_GAME",
                    }
                ),
                encoding="utf-8",
            )
        print(
            f"HPL Web ready: {server.origin} ({'HUMAN start screen' if args.human else 'FIXTURE / NON_GAME'})",
            flush=True,
        )
        if not args.no_browser:
            if not webbrowser.open(server.origin):
                print("Browser did not open; use the exact URL above.", flush=True)
        try:
            server.serve_forever(poll_interval=0.1)
        except KeyboardInterrupt:
            pass
        return 0
    except Exception as error:
        print(f"HPL Web startup failed: {error}", file=sys.stderr, flush=True)
        return 1
    finally:
        if server is not None:
            server.server_close()
        if app is not None:
            app.close()


if __name__ == "__main__":
    raise SystemExit(main())
