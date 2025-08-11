package consumer

import (
	"context"
	"gateway/internal/domain/dto"
	"github.com/segmentio/kafka-go"
)

type Consumer struct {
	reader *kafka.Reader
}

func NewConsumer(reader *kafka.Reader) *Consumer {
	return &Consumer{reader: reader}
}

func (k *Consumer) Consume(ctx context.Context, handler func(msg dto.Message)) error {
	for {
		msg, err := k.reader.ReadMessage(ctx)
		if err != nil {
			return err
		}
		
		handler(dto.Message{
			Key:   msg.Key,
			Value: msg.Value,
			Topic: msg.Topic,
		})
	}
}

func (k *Consumer) Close() error {
	return k.reader.Close()
}
