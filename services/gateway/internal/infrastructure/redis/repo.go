package redis

import (
	"context"
	"github.com/redis/go-redis/v9"
	"time"
)

type Repository struct {
	client *redis.Client
}

func NewRepository(client *redis.Client) *Repository {
	return &Repository{client: client}
}

func (r *Repository) Get(ctx context.Context, key string) (string, error) {
	return r.client.Get(ctx, key).Result()
}

func (r *Repository) Set(
	ctx context.Context,
	key string,
	value interface{},
	duration time.Duration,
) error {
	return r.client.Set(ctx, key, value, duration).Err()
}

func (r *Repository) Delete(ctx context.Context, key string) error {
	return r.client.Del(ctx, key).Err()
}
