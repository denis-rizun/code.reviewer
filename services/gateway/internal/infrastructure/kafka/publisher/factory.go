package publisher

import (
	"github.com/segmentio/kafka-go"
	"strings"
)

type Factory struct {
	brokers string
}

func NewFactory(brokers string) *Factory {
	return &Factory{brokers: brokers}
}

func (f *Factory) Create(topic string) *Publisher {
	brokerList := strings.Split(f.brokers, ",")

	writer := &kafka.Writer{
		Addr:     kafka.TCP(brokerList...),
		Topic:    topic,
		Balancer: &kafka.LeastBytes{},
	}
	return NewPublisher(writer, topic)
}
