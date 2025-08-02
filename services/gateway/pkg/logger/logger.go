package logger

import (
	"log"
	"os"
)

var (
	Info  *log.Logger
	Error *log.Logger
)

const (
	Red   = "\033[31m"
	Green = "\033[32m"
	Reset = "\033[0m"
)

func init() {
	Info = log.New(os.Stdout, Green+"INFO: "+Reset, log.Ldate|log.Ltime|log.Lmsgprefix)
	Error = log.New(os.Stderr, Red+"ERROR: "+Reset, log.Ldate|log.Ltime|log.Lmsgprefix)
}
