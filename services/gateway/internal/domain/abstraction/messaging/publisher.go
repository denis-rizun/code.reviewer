package messaging

import (
	"context"
)

type IPublisher interface {
	Publish(ctx context.Context, key string, value any) error
}
