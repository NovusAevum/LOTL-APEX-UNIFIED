# Node 20 Alpine for Next.js 15
FROM node:20-alpine as deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund

FROM node:20-alpine as builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine as runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
RUN addgroup -S nextjs && adduser -S nextjs -G nextjs
USER nextjs
# Read-only FS; Next standalone can run from .next/standalone if configured
EXPOSE 3000
CMD ["node", ".next/standalone/server.js"]
