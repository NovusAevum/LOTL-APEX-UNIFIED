import Fastify from 'fastify'
import cors from '@fastify/cors'
import helmet from '@fastify/helmet'
import jwt from '@fastify/jwt'
import rateLimit from '@fastify/rate-limit'
import swagger from '@fastify/swagger'
import swaggerUi from '@fastify/swagger-ui'
import websocket from '@fastify/websocket'

import { authRoutes } from './routes/auth'
import { agentRoutes } from './routes/agents'
import { osintRoutes } from './routes/osint'
import { identityRoutes } from './routes/identity'
import { prisma } from './lib/prisma'
import { redis } from './lib/redis'

const fastify = Fastify({
  logger: {
    level: process.env.NODE_ENV === 'production' ? 'info' : 'debug'
  }
})

// Register plugins
async function registerPlugins() {
  await fastify.register(cors, {
    origin: process.env.NODE_ENV === 'production' 
      ? ['https://your-domain.com'] 
      : true
  })

  await fastify.register(helmet)
  
  await fastify.register(jwt, {
    secret: process.env.JWT_SECRET || 'default-secret'
  })

  await fastify.register(rateLimit, {
    max: 100,
    timeWindow: '1 minute'
  })

  await fastify.register(websocket)

  // Swagger documentation
  await fastify.register(swagger, {
    swagger: {
      info: {
        title: 'LOTL Apex API',
        description: 'Sovereign AI System API',
        version: '1.0.0'
      },
      host: 'localhost:3001',
      schemes: ['http', 'https'],
      consumes: ['application/json'],
      produces: ['application/json']
    }
  })

  await fastify.register(swaggerUi, {
    routePrefix: '/docs',
    uiConfig: {
      docExpansion: 'full',
      deepLinking: false
    }
  })
}

// Register routes
async function registerRoutes() {
  await fastify.register(authRoutes, { prefix: '/api/auth' })
  await fastify.register(agentRoutes, { prefix: '/api/agents' })
  await fastify.register(osintRoutes, { prefix: '/api/osint' })
  await fastify.register(identityRoutes, { prefix: '/api/identity' })

  // Health check
  fastify.get('/health', async () => {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      services: {
        database: await checkDatabase(),
        redis: await checkRedis(),
        weaviate: await checkWeaviate()
      }
    }
  })

  // WebSocket for real-time updates
  fastify.register(async function (fastify) {
    fastify.get('/ws', { websocket: true }, (connection) => {
      connection.socket.on('message', (message) => {
        connection.socket.send(`Echo: ${message}`)
      })
    })
  })
}

// Health checks
async function checkDatabase() {
  try {
    await prisma.$queryRaw`SELECT 1`
    return { status: 'healthy' }
  } catch (error) {
    return { status: 'unhealthy', error: error.message }
  }
}

async function checkRedis() {
  try {
    await redis.ping()
    return { status: 'healthy' }
  } catch (error) {
    return { status: 'unhealthy', error: error.message }
  }
}

async function checkWeaviate() {
  try {
    // Add Weaviate health check
    return { status: 'healthy' }
  } catch (error) {
    return { status: 'unhealthy', error: error.message }
  }
}

// Graceful shutdown
async function gracefulShutdown() {
  await prisma.$disconnect()
  await redis.disconnect()
  process.exit(0)
}

process.on('SIGTERM', gracefulShutdown)
process.on('SIGINT', gracefulShutdown)

// Start server
async function start() {
  try {
    await registerPlugins()
    await registerRoutes()
    
    const port = parseInt(process.env.PORT || '3001')
    const host = process.env.HOST || '0.0.0.0'
    
    await fastify.listen({ port, host })
    
    console.log(`🚀 LOTL Apex API server running on http://${host}:${port}`)
    console.log(`📚 API Documentation: http://${host}:${port}/docs`)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}

start()
