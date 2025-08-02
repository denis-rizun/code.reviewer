package publisher

import (
	"context"
	"encoding/json"
	"gateway/pkg/logger"
	"github.com/segmentio/kafka-go"
)

type Publisher struct {
	writer *kafka.Writer
	topic  string
}

func NewPublisher(writer *kafka.Writer, topic string) *Publisher {
	return &Publisher{writer: writer, topic: topic}
}

func (k *Publisher) Publish(ctx context.Context, key string, value any) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return k.publishRaw(ctx, key, data)
}

func (k *Publisher) publishRaw(ctx context.Context, key string, value []byte) error {
	msg := kafka.Message{
		Key:   []byte(key),
		Value: value,
	}
	err := k.writer.WriteMessages(ctx, msg)
	logger.Info.Print("published message to kafka")
	return err
}
