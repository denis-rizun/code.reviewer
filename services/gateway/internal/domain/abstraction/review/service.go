package review

import (
	"context"
	"gateway/internal/domain/dto"
)

type IReviewService interface {
	CheckOrEnqueue(ctx context.Context, dto dto.ReviewRequestDTO) (string, bool, error)
	HandleMessaging(msg dto.Message)
}
