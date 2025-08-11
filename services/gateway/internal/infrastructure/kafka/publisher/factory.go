package publisher

import "github.com/segmentio/kafka-go"

type Factory struct {
	brokers []string
}

func NewFactory(brokers []string) *Factory {
	return &Factory{brokers: brokers}
}

func (f *Factory) Create(topic string) *Publisher {
	writer := &kafka.Writer{
		Addr:     kafka.TCP(f.brokers...),
		Topic:    topic,
		Balancer: &kafka.LeastBytes{},
	}
	return NewPublisher(writer, topic)
}
