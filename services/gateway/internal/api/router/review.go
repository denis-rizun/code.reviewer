package router

import (
	"fmt"
	"gateway/internal/application"
	"gateway/internal/domain/dto"
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
		c.JSON(http.StatusOK, gin.H{"status": "ready", "data": result})
		return
	}

	c.JSON(http.StatusAccepted, gin.H{"status": "processing"})
}
