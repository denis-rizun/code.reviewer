package application

import (
	"context"
	"encoding/json"
	"fmt"
	"gateway/internal/domain/abstraction/caching"
	"gateway/internal/domain/abstraction/messaging"
	"gateway/internal/domain/dto"
	"gateway/pkg/logger"
	"time"
)

type ReviewService struct {
	RedisRepo      caching.IRepo
	KafkaPublisher messaging.IPublisher
}

func NewReviewService(repo caching.IRepo, kafkaPublisher messaging.IPublisher) *ReviewService {
	return &ReviewService{RedisRepo: repo, KafkaPublisher: kafkaPublisher}
}

func (s *ReviewService) CheckOrEnqueue(
	ctx context.Context,
	dto dto.ReviewRequestDTO,
) (string, bool, error) {
	val, err := s.RedisRepo.Get(ctx, dto.TaskID)
	if err == nil && val != "" {
		return val, true, nil
	}

	if err := s.KafkaPublisher.Publish(ctx, dto.TaskID, dto); err != nil {
		return "", false, err
	}

	return "", false, nil
}

func (s *ReviewService) HandleMessaging(msg dto.Message) {
	var data map[string]interface{}
	if err := json.Unmarshal(msg.Value, &data); err != nil {
		logger.Error.Printf("failed to parse kafka message: %v", err)
		return
	}

	taskID, ok := data["task_id"].(string)
	if !ok {
		logger.Error.Printf("task_id not found in message: %v", data)
		return
	}

	key := fmt.Sprintf("task:%s", taskID)

	err := s.RedisRepo.Set(context.Background(), key, msg.Value, time.Hour)
	if err != nil {
		logger.Error.Printf("failed to save message to redis: %v", err)
		return
	}

	logger.Info.Printf("task_id=%s saved to redis", taskID)
}
