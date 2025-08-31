from typing import ClassVar


class Constants:
    PROJECT_NAME: ClassVar[str] = "code.reviewer"
    GITHUB_LINK: ClassVar[str] = "https://github.com/denis-rizun/code.reviewer"
    GATEWAY_URL: ClassVar[str] = "http://api:8080"

    INFO_TEXT: ClassVar[str] = (
        "<b>🤖 code.reviewer</b>\n"
        "AI-driven auditor for your public GitHub repositories.\n"
        "Just drop a link — we'll handle the rest."
    )
    SUPPORT_TEXT: ClassVar[str] = (
        "📞 <b>Need help?</b>\n"
        "If you have any questions or issues,\n"
        "please contact our support team:\n"
        "<b>@dddd1w</b>"
    )
    REVIEW_REQUEST_TEXT: ClassVar[str] = (
        "<b>📦 Repository Audit</b>\n"
        "Send me a public GitHub repository link.\n"
        "Within 1-3 minutes, I'll provide a detailed audit covering:\n\n"
        "• Documentation\n"
        "• Code quality\n"
        "• Project structure\n"
        "• Architecture\n"
        "• And more..."
    )
    REVIEW_INCORRECT_LINK_TEXT: ClassVar[str] = (
        "❌ <i>Please send a valid GitHub repository link.</i>"
    )
    REVIEW_STARTING_TEXT: ClassVar[str] = "<b>Starting repository audit...</b>"
    REVIEW_WAITING_1_TEXT: ClassVar[str] = "🔄 <b>Fetching metadata of repository...</b>"
    REVIEW_WAITING_2_TEXT: ClassVar[str] = "🔄 <b>Loading repository...</b>"
    REVIEW_WAITING_3_TEXT: ClassVar[str] = "🔄 <b>Analyzing repository...</b>"
    REVIEW_RESULT_TEXT: ClassVar[str] = "✅ <b>Repository audit completed!</b>"
    DONATE_TEXT: ClassVar[str] = (
        "💡 Like the project?\n"
        "Support me on GitHub ⭐\n"
        f"<a href='{GITHUB_LINK}'>Click me</a>."
    )
