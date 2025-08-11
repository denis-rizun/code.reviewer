package main

import (
	"gateway/internal/infrastructure"
	"gateway/pkg/logger"
)

func main() {
	bootstrap := infrastructure.NewBootstrap()

	router, err := bootstrap.Configure()
	if err != nil {
		logger.Error.Fatalf("failed to configure application: %v", err)
	}

	if err := router.Run(); err != nil {
		logger.Error.Fatalf("failed to run server: %v", err)
	}
	logger.Info.Println("server running")
}
