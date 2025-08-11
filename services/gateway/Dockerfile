FROM golang:1.24.4 as builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o main ./cmd/main.go

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /app/main .

EXPOSE 8080

ENTRYPOINT ["./main"]