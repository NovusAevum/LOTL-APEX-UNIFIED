FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat python3 py3-pip
WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable pnpm && pnpm install --frozen-lockfile

# Copy source
COPY . .

# Build
RUN pnpm build

CMD ["pnpm", "start"]
