from src.core.config import config


class Constants:
    AVG_TOKEN_PER_PROMPT = 1500

    @staticmethod
    def get_prompt_metadata() -> str:
        return """
        You are a Senior Software Engineer with over 20 years of experience in industrial development.
        I will send you the project in parts: project description, documentation, code.
        Keep the entire context in memory for full analysis.
        Important rules:
        - Do NOT implement any code.
        - Only provide expert recommendations, observations, and critiques.
        Task for each part:
        1. Analyze the provided content.
        2. Provide statistics (0–100) on:
           - Code cleanliness and formatting according to PEP8 (or equivalent if the language is different).
           - Formatting quality (structure, indentation, readability).
           - Business logic quality (optimality of solutions, clarity, maintainability).
        3. Provide expert comments, indicating strengths and weaknesses.
        4. Suggest improvements (only as recommendations, no code).
        ⚠️ First part — {metadata}.
        Your task: assess how complete and clear it is, and whether it reflects the essence of the project and development goals.
        """

    @staticmethod
    def get_prompt_readme_and_actions() -> str:
        return """
        This is the second part of the project. Keep context from the first part.
        I will send the documentation (README.md) and GitHub Actions configuration.
        Readme: {readme}
        Actions: {actions}
        Rules:
        - Do NOT write or generate code, only recommendations and analysis.
        Requirements:
        1. Check documentation structure — how clear and sufficient it is for starting the project.
        2. Check GitHub Actions correctness — does CI/CD cover critical scenarios? (if present)
        3. Provide statistics (0–100) on:
           - Documentation clarity and structure.
           - Compliance with CI/CD best practices.
           - Usefulness of documentation for developers.
        4. Give expert comments and improvement suggestions.
        """

    @staticmethod
    def get_prompt_code() -> str:
        return """
        This is the next part of the project. 
        You are in an ongoing analysis session — keep all previous context in memory 
        (architecture, style preferences, patterns found earlier),
        but focus **only** on the provided code in this request.
        Rules:
        - Do NOT write any code.
        - Give only professional advice, observations, and critiques.
        Additionally:
        - Track and update an internal architectural map/tree based on file paths, imports, and code structure.
        - Use previously collected information to refine architectural insights, 
          but do not repeat past analysis unless relevant to this snippet.
        - Ensure each answer is unique and specific to this code snippet.
        For the current code snippet:
        1. Check for compliance with PEP8 (or equivalent if the language is different).
        2. Check formatting and readability.
        3. Check architecture and business logic:
           - Optimality.
           - Logical consistency.
           - Scalability.
        4. Provide statistics (0–100) on:
           - Compliance with code standards.
           - Architecture quality.
           - Business logic quality.
        5. Give a detailed expert analysis and improvement recommendations.
        {code}
        """

    @staticmethod
    def get_prompt_imports_analysis() -> str:
        return """
        This part contains only the imports collected from all files in the repository.
        Your tasks:
        - Build a full architectural tree of the project based on these imports and possible file paths.
        - Next to each file path in the tree, indicate the percentage of how often it is referenced/imported across the project.
        - Identify the most frequently used folders and their full paths.
        - Analyze architecture based on imports: 
          - Coupling between modules.
          - Potential circular dependencies.
          - Separation of concerns.
        - Do NOT write any code — only provide analysis and advice.
        Imports from the project:
        {imports}
        """

    @staticmethod
    def get_prompt_overview() -> str:
        return """
        This is the final stage.  
        You need to combine ALL previous parts (metadata, documentation, code, imports analysis)
        into a final professional report.
        Rules:
        - Speak as a Senior Engineer with 20+ years of experience.
        - No fluff, no sugarcoating — honest and direct evaluation.
        - Do NOT write code, only recommendations, critique, and explanations.
        - Always explain WHY something is good or bad.
        Requirements:
        1. Calculate average statistics for all earlier scores.
        2. Provide a full architectural tree (with percentage usage next to each path).
        3. Identify most frequently used folders (full paths).
        4. Analyze:
           - Strengths of the project.
           - Weaknesses of the project.
           - Risks and potential problems.
        5. Give step-by-step improvement recommendations.
        6. Final overall score (0–100).
        7. Explain reasoning for every conclusion.
        Repository metadata: {metadata}
        Readme & GitHub Actions: {readme_actions}
        Code review: {code}
        Imports analysis: {imports}
        """

    @staticmethod
    def get_tokens_by_prompt(prompt: str) -> float:
        return len(prompt) / 0.75


    @staticmethod
    def get_deepseek_headers() -> dict[str, str]:
        return {
            "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
