package router

import (
	"encoding/json"
	"fmt"
	"gateway/internal/application"
	"gateway/internal/domain/dto"
	"gateway/pkg/logger"
	"github.com/gin-gonic/gin"
	"net/http"
)

type ReviewHandler struct {
	reviewService *application.ReviewService
}

func NewReviewHandler(reviewService *application.ReviewService) *ReviewHandler {
	return &ReviewHandler{reviewService: reviewService}
}

func (h *ReviewHandler) Register(r *gin.RouterGroup) {
	r.POST("/review", h.CheckIn)
}

func (h *ReviewHandler) CheckIn(c *gin.Context) {
	var req dto.ReviewRequestDTO
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid request"})
		return
	}

	result, found, err := h.reviewService.CheckOrEnqueue(c.Request.Context(), req)
	if err != nil {
		fmt.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "internal error"})
		return
	}

	if found {
		var resultData map[string]interface{}
		if err := json.Unmarshal([]byte(result), &resultData); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to parse result"})
			return
		}

		resultData["status"] = "ready"
		c.JSON(http.StatusOK, resultData)

		key := fmt.Sprintf("task:%s", req.TaskID)
		if err := h.reviewService.RedisRepo.Delete(c.Request.Context(), key); err != nil {
			logger.Error.Printf("failed to delete Key %s: %v\n", key, err)
		}
		return
	}

	c.JSON(http.StatusAccepted, gin.H{"status": "processing"})
}
