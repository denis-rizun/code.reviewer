package consumer

import "github.com/segmentio/kafka-go"

type Factory struct {
	brokers []string
}

func NewFactory(brokers []string) *Factory {
	return &Factory{brokers: brokers}
}

func (f *Factory) Create(groupID string, topic string) *Consumer {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  f.brokers,
		GroupID:  groupID,
		Topic:    topic,
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})
	return NewConsumer(reader)
}
