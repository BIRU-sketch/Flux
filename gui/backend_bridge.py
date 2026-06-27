"""The only file that talks to agent/ and tools/ - everything else goes through here"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.ai import AI
from tools.tools import tools


class BackendBridge:
    def __init__(self):
        self.ai = AI()
        self.tools = tools()
        self.history = []  # will later load from a persistent store

    def submit_task(self, prompt):
        """
        Plan + execute a task. Returns a dict with steps, status, results.
        For now this is synchronous - we'll move to QThread later to avoid freezing UI.
        """
        plan = self.ai.plan_task(prompt)

        if "error" in plan:
            return {"success": False, "error": plan["error"]}

        results = []
        for step in plan.get("steps", []):
            result = self.tools.execute_bash(step)
            results.append({"command": step, "result": result})

        entry = {
            "prompt": prompt,
            "plan": plan,
            "results": results,
        }
        self.history.append(entry)
        return {"success": True, "entry": entry}

    def get_history(self):
        return self.history