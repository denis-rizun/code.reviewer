from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from src.application.ai.deepseek import DeepseekAIModel
from src.application.file_handler.chunker import ChunkerService
from src.application.cloner import GitHubCloner
from src.application.file_handler.processer import FileProcesser
from src.application.file_handler.import_extractor import ImportExtractor
from src.application.message_handler import MessageHandler
from src.application.reviewer.pipeline import ReviewerPipeline
from src.application.reviewer.service import ReviewerService
from src.application.serializer.jsons import JSONSerializer
from src.application.serializer.string import StringSerializer
from src.core.config import config
from src.infrastructure.kafka.factories import KafkaConsumerFactory, KafkaProducerFactory
from src.infrastructure.kafka.services import KafkaConsumer, KafkaProducer


class Container(DeclarativeContainer):
    json_serializer = Singleton(JSONSerializer)
    string_serializer = Singleton(StringSerializer)

    kafka_producer_factory = Factory(
        KafkaProducerFactory,
        bootstrap_servers=config.kafka_bootstrap_server,
        key_serializer=string_serializer,
        value_serializer=json_serializer,
    )
    kafka_producer = Factory(KafkaProducer, factory=kafka_producer_factory)
    kafka_consumer_factory = Factory(
        KafkaConsumerFactory,
        bootstrap_servers=config.kafka_bootstrap_server,
        key_serializer=string_serializer,
        value_serializer=json_serializer,
    )
    kafka_consumer = Factory(KafkaConsumer, factory=kafka_consumer_factory)
    message_handler = Factory(MessageHandler)

    deepseek_ai_model = Factory(DeepseekAIModel)

    github_cloner = Factory(GitHubCloner)
    file_processer = Factory(FileProcesser)
    chunker = Factory(ChunkerService)
    import_extractor = Factory(ImportExtractor)

    reviewer_service = Factory(
        ReviewerService,
        cloner=github_cloner,
        processer=file_processer,
        ai_model=deepseek_ai_model,
        chunker=chunker,
        import_extractor=import_extractor,
    )
    reviewer_pipeline = Factory(
        ReviewerPipeline,
        reviewer=reviewer_service,
        producer=kafka_producer,
    )



container = Container()
