
from dataclasses import dataclass


@dataclass
class SecurityDecision:
    allowed: bool
    requires_approval: bool
    reason: str


class NexusSecurity:

    # Actions that always require employee approval
    SENSITIVE_ACTIONS = {
        "DELETE_FILE",
        "SEND_EMAIL",
        "SEND_MESSAGE",
        "UPLOAD_FILE",
        "DOWNLOAD_FILE",
        "MODIFY_FILE",
        "RUN_COMMAND",
        "FINANCIAL_TRANSACTION",
        "SUBMIT_FORM",
        "DESKTOP_CONTROL"
    }

    # Actions that are not permitted
    BLOCKED_ACTIONS = {
        "STEAL_DATA",
        "ACCESS_PASSWORDS",
        "DISABLE_SECURITY",
        "UNAUTHORIZED_ACCESS"
    }

    def check_action(self, action_type):

        action_type = action_type.upper().strip()

        if action_type in self.BLOCKED_ACTIONS:
            return SecurityDecision(
                allowed=False,
                requires_approval=False,
                reason="This action is prohibited by NEXUS security."
            )

        if action_type in self.SENSITIVE_ACTIONS:
            return SecurityDecision(
                allowed=True,
                requires_approval=True,
                reason="Employee approval is required."
            )

        return SecurityDecision(
            allowed=True,
            requires_approval=False,
            reason="No additional approval required."
        )

