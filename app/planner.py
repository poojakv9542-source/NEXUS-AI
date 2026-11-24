
from dataclasses import dataclass, field
from typing import List


@dataclass
class Action:
    action_type: str
    description: str
    requires_approval: bool = False
    parameters: dict = field(default_factory=dict)


@dataclass
class TaskPlan:
    objective: str
    actions: List[Action]
    requires_approval: bool = False


class NexusPlanner:

    def create_plan(self, instruction: str) -> TaskPlan:
        instruction = instruction.strip()

        if not instruction:
            raise ValueError("Employee instruction cannot be empty.")

        # Initial safe planning logic.
        # Ollama will later replace this rule-based decision layer.

        plan = TaskPlan(
            objective=instruction,
            actions=[
                Action(
                    action_type="ANALYZE",
                    description="Analyze the employee instruction."
                )
            ]
        )

        return plan
