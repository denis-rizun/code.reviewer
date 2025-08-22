import shutil
from asyncio import gather

from src.core.constants import Constants
from src.core.logger import Logger
from src.domain.entities.file import FileRepositoryMetaContent
from src.domain.interfaces.ai.model import IAIModel
from src.domain.interfaces.chunker import IChunkerService
from src.domain.interfaces.import_extractor import IImportExtractor
from src.domain.interfaces.repository.cloner import IRepositoryCloner
from src.domain.interfaces.repository.processer import IFileProcesser
from src.domain.interfaces.reviewer.service import IReviewerService

logger = Logger.setup(__name__)


class ReviewerService(IReviewerService):
    def __init__(
            self,
            cloner: IRepositoryCloner,
            processer: IFileProcesser,
            ai_model: IAIModel,
            chunker: IChunkerService,
            import_extractor: IImportExtractor,
    ) -> None:
        self._cloner = cloner
        self._processer = processer
        self._ai_model = ai_model
        self._chunker = chunker
        self._extractor = import_extractor

    async def review(self, link: str) -> str:
        repository, local_path = await self._prepare_repo(link=link)

        try:
            prompts = self._prepare_prompts(repo_data=repository)
            overview = await self._run_ai_analysis(prompts=prompts)
        finally:
            shutil.rmtree(local_path)

        return overview

    async def _prepare_repo(self, link: str) -> tuple[FileRepositoryMetaContent, str]:
        repo = self._cloner.clone(link=link)
        content = await self._processer.get_files_content(root_path=repo.local_path)
        readme = self._processer.get_readme(content=content)
        actions = self._processer.get_actions(content=content)
        files_count = self._processer.get_files_count(content=content)
        imports = self._extractor.extract(files=content)

        return (
            FileRepositoryMetaContent(
                description=(
                    f"{repo.name} - {repo.description} "
                    f"- {repo.language} - {repo.licence.name} - {files_count} files"
                ),
                readme=readme,
                actions=actions,
                content=content,
                imports=imports,
            ),
            repo.local_path
        )


    def _prepare_prompts(self, repo_data: FileRepositoryMetaContent) -> list[str]:
        constants = (
            Constants.get_prompt_metadata(),
            Constants.get_prompt_readme_and_actions(),
            Constants.get_prompt_code(),
            Constants.get_prompt_imports_analysis(),
            Constants.get_prompt_overview(),
        )

        max_tokens = self._ai_model.MAX_TOKENS - Constants.AVG_TOKEN_PER_PROMPT
        chunks_code = self._chunker.chunk(repo_data.content, max_tokens)
        chunks_imports = self._chunker.chunk(repo_data.imports, max_tokens)

        prompts = [
            constants[0].format(metadata=repo_data.description),
            constants[1].format(readme=repo_data.readme, actions=repo_data.actions),
        ]
        prompts.extend(constants[2].format(code=chunk) for chunk in chunks_code)
        prompts.extend(constants[3].format(imports=chunk) for chunk in chunks_imports)
        return prompts

    async def _run_ai_analysis(self, prompts: list[str]) -> str:
        async with self._ai_model as ai:
            responses = await gather(*(ai.ask(prompt) for prompt in prompts))
            overview_prompt = self._generate_overview(responses=responses)
            return await ai.ask(overview_prompt)

    @classmethod
    def _generate_overview(cls, responses: list[str]) -> str:
        return Constants.get_prompt_overview().format(
            metadata=responses[0],
            readme_actions=responses[1],
            code="\n".join(responses[2]),
            imports="\n".join(responses[3]),
        )
