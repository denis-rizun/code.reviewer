package messaging

import (
	"context"
	"gateway/internal/domain/dto"
)

type IConsumer interface {
	Consume(ctx context.Context, handler func(dto.Message)) error
	Close() error
}
