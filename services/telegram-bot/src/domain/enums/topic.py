from enum import StrEnum


class KafkaTopicEnum(StrEnum):
    USER_ACTION = "user.action"
    REVIEW_ACTION = "review.action"
