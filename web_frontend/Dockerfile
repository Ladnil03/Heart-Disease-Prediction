FROM node:20-alpine as builder

WORKDIR /app

# Install a simple HTTP server
RUN npm install -g serve

COPY . .

# Stage 2: Runtime stage
FROM node:20-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["serve", "-s", ".", "-l", "3000"]
