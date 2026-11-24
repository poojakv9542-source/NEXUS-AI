
from pathlib import Path

from app.security import NexusSecurity


class NexusExecutor:

    def __init__(self):
        self.security = NexusSecurity()

        # Restrict file operations to the NEXUS project directory.
        self.workspace = Path(__file__).resolve().parent.parent

    def _safe_path(self, relative_path):
        target = (self.workspace / relative_path).resolve()

        # Prevent access outside the NEXUS workspace.
        if not target.is_relative_to(self.workspace):
            raise PermissionError("Access outside the NEXUS workspace is prohibited.")

        return target

    def execute(self, action, approved=False):

        action_type = action.action_type.upper().strip()

        # 1. Check security policy.
        decision = self.security.check_action(action_type)

        if not decision.allowed:
            return {
                "success": False,
                "message": decision.reason
            }

        # 2. Require approval for sensitive operations.
        if decision.requires_approval and not approved:
            return {
                "success": False,
                "message": "Employee approval is required."
            }

        try:

            # 3. Supported safe operations.
            if action_type == "ANALYZE":
                return {
                    "success": True,
                    "message": "Instruction analysis step acknowledged."
                }

            elif action_type == "LIST_FILES":
                relative_path = action.parameters.get("path", ".")
                folder = self._safe_path(relative_path)

                if not folder.is_dir():
                    raise ValueError("The requested folder does not exist.")

                files = [
                    item.name for item in folder.iterdir()
                ]

                return {
                    "success": True,
                    "files": files
                }

            elif action_type == "READ_FILE":
                relative_path = action.parameters.get("path")

                if not relative_path:
                    raise ValueError("A file path is required.")

                file_path = self._safe_path(relative_path)

                if not file_path.is_file():
                    raise ValueError("The requested file does not exist.")

                if file_path.stat().st_size > 1_000_000:
                    raise ValueError("File exceeds the 1 MB reading limit.")

                content = file_path.read_text(
                    encoding="utf-8",
                    errors="replace"
                )

                return {
                    "success": True,
                    "content": content
                }

            else:
                return {
                    "success": False,
                    "message": f"Action not implemented: {action_type}"
                }

        except Exception as error:
            return {
                "success": False,
                "message": str(error)
            }
