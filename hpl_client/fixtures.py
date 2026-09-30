"""Synthetic no-game UI fixtures, deliberately disconnected from CareerSim."""

from types import SimpleNamespace

from hpl_client.controller import HumanGameController
from hpl_client.game_adapter import PublicGameAdapter


class FixtureEngine:
    def __init__(self, ending=False, energy=8):
        self.ending = ending
        self.energy = energy
        self.action_calls = 0

    async def new_game(self):
        return SimpleNamespace(session_id="fixture-session", error="")

    async def enrollment_handbook(self):
        return "员工入职手册（合成展示）\n阅读事件，选择适合你的行动。\n这是离线 fixture，不会创建真实游戏。"

    async def observe(self, session_id):
        return SimpleNamespace(
            current_state={
                "session_id": session_id,
                "time": {"current_month": 5, "current_quarter": 2, "current_year": 1},
                "status": {
                    "level": "P3",
                    "health": 78,
                    "dignity": 70,
                    "skill": 42,
                    "network": 36,
                    "output": 55,
                    "wealth": 12000,
                    "energy": self.energy,
                },
            },
            current_event={
                "title": "项目评审 · 离线展示",
                "description": "团队正在准备下季度计划。\n" + "你需要在协作与个人成长之间安排精力。" * 8,
            },
            choices=[]
            if self.ending
            else [
                {"choice": 1, "action": "与同事梳理项目计划", "energy_cost": 2},
                {"choice": 2, "action": "预留时间学习新技能", "energy_cost": 3},
            ],
            warning="季度回顾：团队感谢你的贡献。（合成展示）",
            ending_score={
                "completed": True,
                "grade": "A",
                "survival_months": 48,
                "quantitative_score": 82,
                "competition_partial_score": 45,
            }
            if self.ending
            else None,
        )

    async def take_action(self, session_id, choice, notes=""):
        self.action_calls += 1
        return SimpleNamespace(success=True, error=None)


class FixtureRecorder:
    root = None

    def transition(self, *args):
        pass

    def journal(self, *args):
        pass

    def submission(self, selection):
        self.journal("submission_intent", selection)

    def failure(self, *args):
        pass


def fixture_controller(ending=False, energy=8):
    return HumanGameController(
        lambda tag: (PublicGameAdapter(FixtureEngine(ending, energy), "fixture-no-game"), FixtureRecorder())
    )
