package infrastructure

import (
	"context"
	"gateway/internal/api/middleware"
	"gateway/internal/api/router"
	service "gateway/internal/application"
	"gateway/internal/domain"
	"gateway/internal/infrastructure/kafka/consumer"
	"gateway/internal/infrastructure/kafka/publisher"
	"gateway/internal/infrastructure/redis"
	"gateway/pkg/config"
	"github.com/gin-gonic/gin"
	redisGo "github.com/redis/go-redis/v9"
	"strconv"
)

type Bootstrap struct {
	cfg              *config.Config
	router           *gin.Engine
	api              *gin.RouterGroup
	publisherFactory *publisher.Factory
	consumerFactory  *consumer.Factory
}

func NewBootstrap() *Bootstrap {
	return &Bootstrap{}
}

func (b *Bootstrap) Configure() (*gin.Engine, error) {
	b.cfg = config.LoadConfig()
	gin.SetMode(gin.ReleaseMode)
	b.router = gin.New()
	b.api = b.router.Group("/api/v1")

	b.setupMiddleware()
	b.setupKafka()
	b.setupHandlers()
	return b.router, nil
}

func (b *Bootstrap) setupMiddleware() {
	b.router.Use(middleware.Logger())
	b.router.Use(gin.Recovery())
}

func (b *Bootstrap) setupKafka() {
	b.publisherFactory = publisher.NewFactory(b.cfg.KafkaBrokers)
	b.consumerFactory = consumer.NewFactory(b.cfg.KafkaBrokers)
}

func (b *Bootstrap) setupHandlers() {
	healthHandler := router.NewHealthHandler()
	healthHandler.Register(b.api)

	redisRepo := b.setupRedis()

	reviewPublisher := b.publisherFactory.Create(domain.ReviewRequestTopic)
	reviewService := service.NewReviewService(redisRepo, reviewPublisher)

	reviewHandler := router.NewReviewHandler(reviewService)
	reviewHandler.Register(b.api)

	reviewConsumer := b.consumerFactory.Create(domain.ReviewGroup, domain.ReviewResponseTopic)
	go func() {
		ctx := context.Background()
		_ = reviewConsumer.Consume(ctx, reviewService.HandleMessaging)
	}()
}

func (b *Bootstrap) setupRedis() *redis.Repository {
	rdb := redisGo.NewClient(&redisGo.Options{
		Addr: b.cfg.RedisHost + ":" + strconv.Itoa(b.cfg.RedisPort),
	})
	return redis.NewRepository(rdb)
}
