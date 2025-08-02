package logger

import (
	"gateway/internal/domain"
	"log"
	"os"
)

var (
	Info  *log.Logger
	Error *log.Logger
)

func init() {
	Info = log.New(
		os.Stdout,
		domain.GreenColor+"INFO: "+domain.ResetColor, log.Ldate|log.Ltime|log.Lmsgprefix,
	)
	Error = log.New(
		os.Stderr,
		domain.RedColor+"ERROR: "+domain.ResetColor, log.Ldate|log.Ltime|log.Lmsgprefix,
	)
}
