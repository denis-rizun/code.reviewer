from src.core.constants import Constants
from src.core.exceptions import NotFoundException, DeserializationException
from src.core.logger import Logger
from src.domain.interfaces.broker.producer import IProducer
from src.domain.interfaces.reviewer.pipeline import IReviewerPipeline
from src.domain.interfaces.reviewer.service import IReviewerService

logger = Logger.setup(__name__)


class ReviewerPipeline(IReviewerPipeline):
    def __init__(self, reviewer: IReviewerService, producer: IProducer) -> None:
        self._reviewer = reviewer
        self._producer = producer

    async def run(self, key: str, value: dict[str, str]) -> None:
        user_id, link = self.fetch_from_message(key=key, value=value)

        overview = await self._reviewer.review(link=link)
        logger.info(f"[ReviewerPipeline]: Successful completed | User({user_id})")

        await self.send_result(key=key, overview=overview, link=link)

    async def send_result(self, key: str, overview: str, link: str) -> None:
        async with self._producer:
            await self._producer.send(
                topic=Constants.REVIEW_RESPONSE_TOPIC,
                key=key,
                value={"overview": overview, "task_id": key, "repository_link": link},
            )

    @classmethod
    def fetch_from_message(cls, key: str, value: dict[str, str]) -> tuple[int, str]:
        if ":" not in key:
            logger.error(f"Invalid key format: {key}")
            raise DeserializationException("Invalid key format")

        try:
            user_id = int(key.split(":")[0])
        except (IndexError, ValueError) as e:
            logger.error(f"[ReviewerPipeline]: Cannot parse user_id from key: {key}")
            raise DeserializationException("Cannot parse user_id from key") from e

        link = value.get("repository_link")
        if not link:
            logger.error(f"[ReviewerPipeline]: Link not found in message: {value}")
            raise NotFoundException("Link not found in message")

        return user_id, link
