from typing import Self, Any, ClassVar

from httpx import AsyncClient, Response, Timeout
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from src.core.constants import Constants
from src.core.exceptions import BadResponseException, NotInitializedException
from src.core.logger import Logger
from src.domain.interfaces.ai.model import IAIModel
from src.domain.type import ExcType, ExcVal, ExcTB

logger = Logger.setup(__name__)


class DeepseekAIModel(IAIModel):
    MAX_TOKENS = 4000
    MODEL = "deepseek-chat"
    _BASE_URL: ClassVar[str] = "https://api.deepseek.com/chat/completions"
    _MAX_RETRIES: ClassVar[int] = 2
    _DELAY: ClassVar[int] = 30

    def __init__(self) -> None:
        self._client = None

    async def __aenter__(self) -> Self:
        self._client = AsyncClient()
        return self

    async def __aexit__(self, exc_type: ExcType, exc_val: ExcVal, exc_tb: ExcTB) -> None:
        if self._client:
            await self._client.aclose()

    @retry(
        stop=stop_after_attempt(_MAX_RETRIES),
        wait=wait_fixed(_DELAY),
        retry=retry_if_exception_type(BadResponseException)
    )
    async def ask(self, prompt: str) -> str:
        if not self._client:
            raise NotInitializedException("HTTPX-Client is not initialized")

        response = await self._get_response(prompt=prompt)
        if response.status_code != 200:
            raise BadResponseException(
                message=f"Invalid response from AI Model: {response.text}"
            )

        return self._serialize(response=response)

    async def _get_response(self, prompt: str) -> Response:
        return await self._client.post(
            url=self._BASE_URL,
            json=self._build_payload(prompt=prompt),
            headers=Constants.get_deepseek_headers(),
            timeout=Timeout(connect=10, read=120, write=120, pool=10)
        )

    @classmethod
    def _build_payload(cls, prompt: str) -> dict[str, Any]:
        return {
            "model": cls.MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }

    @classmethod
    def _serialize(cls, response: Response) -> str:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Unexpected OpenAI response format: {e}")
            raise ValueError("Malformed response from OpenAI API") from e
