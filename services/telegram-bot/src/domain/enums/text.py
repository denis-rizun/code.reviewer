from enum import StrEnum

from src.core.config import config


class TextEnum(StrEnum):
    INFO = (
        "<b>🤖 code.reviewer</b>\n"
        "AI-driven auditor for your public GitHub repositories.\n"
        "Just drop a link — we'll handle the rest."
    )
    SUPPORT = (
        "📞 <b>Need help?</b>\n"
        "If you have any questions or issues,\n"
        "please contact our support team:\n"
        "<b>@dddd1w</b>"
    )
    REVIEW = (
        "<b>📦 Repository Review</b>\n"
        "Send me a public GitHub repository link.\n"
        "Within 20-60 seconds, I'll provide a detailed audit covering:\n\n"
        "• Documentation\n"
        "• Code quality\n"
        "• Project structure\n"
        "• Tech stack\n"
        "• And more..."
    )
    DONATE = (
        "💡 Like the project?\n"
        "Support me on GitHub ⭐\n"
        f"<a href='{config.GITHUB_LINK}'>Click me</a>."
    )
