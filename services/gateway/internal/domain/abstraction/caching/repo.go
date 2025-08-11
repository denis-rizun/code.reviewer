package caching

import (
	"context"
	"time"
)

type IRepo interface {
	Get(ctx context.Context, key string) (string, error)
	Set(ctx context.Context, key string, value interface{}, duration time.Duration) error
	Delete(ctx context.Context, key string) error
}
