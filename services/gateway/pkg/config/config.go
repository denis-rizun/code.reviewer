package config

import (
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
	"log"
)

type Config struct {
	Port int `envconfig:"PORT"`

	RedisHost string `envconfig:"REDIS_HOST"`
	RedisPort int    `envconfig:"REDIS_PORT"`

	KafkaBrokers []string `envconfig:"KAFKA_BROKERS" split_words:"true"`
}

func LoadConfig() *Config {
	_ = godotenv.Load()

	var cfg Config
	if err := envconfig.Process("", &cfg); err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	return &cfg
}
