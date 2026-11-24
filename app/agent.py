
from app.memory import NexusMemory
from app.planner import NexusPlanner
from app.executor import NexusExecutor


class NexusAgent:
    

    def execute_existing_task(self, task_id: int):
        task = self.memory.get_task(task_id)

        if not task:
            raise ValueError(f"Task #{task_id} was not found.")

        if task["status"] == "RUNNING":
            raise ValueError(f"Task #{task_id} is already running.")

        self.memory.update_task(task_id, "RUNNING")

        try:
            plan = self.planner.create_plan(task["instruction"])
            execution_results = []
            approval_needed = False
            execution_failed = False

            for action in plan.actions:
                if action.requires_approval:
                    approval_needed = True
                    execution_results.append({
                        "action": action.action_type,
                        "success": False,
                        "message": "Employee approval is required."
                    })
                    continue

                result = self.executor.execute(action, approved=False)

                execution_results.append({
                    "action": action.action_type,
                    **result
                })

                if not result["success"]:
                    if "approval is required" in result.get(
                        "message", ""
                    ).lower():
                        approval_needed = True
                    else:
                        execution_failed = True

            if approval_needed:
                status = "AWAITING_APPROVAL"
            elif execution_failed:
                status = "FAILED"
            else:
                status = "COMPLETED"

            # The current ANALYZE action is only a placeholder.
            if all(a.action_type.upper() == "ANALYZE" for a in plan.actions):
                status = "FAILED"
                execution_results.append({
                    "action": "AI_ANALYSIS",
                    "success": False,
                    "message": (
                        "AI reasoning is not connected yet. "
                        "Connect Ollama to generate a genuine AI result."
                    )
                })

            saved_result = {
                "objective": plan.objective,
                "execution_results": execution_results
            }

            self.memory.update_task(
                task_id,
                status,
                result=str(saved_result),
                error=(
                    "AI engine not connected."
                    if status == "FAILED" else None
                )
            )

            return {
                "task_id": task_id,
                "status": status,
                "objective": plan.objective,
                "execution_results": execution_results
            }

        except Exception as error:
            self.memory.update_task(
                task_id,
                "FAILED",
                error=str(error)
            )
            raise


    def __init__(self):
        self.memory = NexusMemory()
        self.planner = NexusPlanner()
        self.executor = NexusExecutor()

    def process_instruction(self, instruction: str):

        print("\nNEXUS is analyzing your instruction...")

        task_id = self.memory.create_task(instruction)

        try:
            self.memory.update_task(task_id, "RUNNING")

            # Generate the plan
            plan = self.planner.create_plan(instruction)

            execution_results = []
            approval_needed = False
            execution_failed = False

            # Execute permitted actions
            for action in plan.actions:

                if action.requires_approval:
                    approval_needed = True
                    execution_results.append({
                        "action": action.action_type,
                        "success": False,
                        "message": "Employee approval is required."
                    })
                    continue

                result = self.executor.execute(
                    action,
                    approved=False
                )

                execution_results.append({
                    "action": action.action_type,
                    **result
                })

                if not result["success"]:
                    if "approval is required" in result.get(
                        "message", ""
                    ).lower():
                        approval_needed = True
                    else:
                        execution_failed = True

            # Update task status
            if execution_failed:
                status = "FAILED"

            else:
                # Plan review is still required before the actual task.
                status = "AWAITING_APPROVAL"

            self.memory.update_task(
                task_id,
                status,
                result=str({
                    "plan": plan.objective,
                    "execution_results": execution_results,
                    "note": "Plan prepared; actual task work has not been completed."
                })
            )

            return {
                "task_id": task_id,
                "objective": plan.objective,
                "actions": plan.actions,
                "execution_results": execution_results,
                "status": status,
                "approval_needed": approval_needed
            }

        except Exception as error:
            self.memory.update_task(
                task_id,
                "FAILED",
                error=str(error)
            )
            raise

    def close(self):
        self.memory.close()
