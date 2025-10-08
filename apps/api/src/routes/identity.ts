import { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import { prisma } from '../lib/prisma'

export const identityRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.addHook('preHandler', async (request, reply) => {
    try {
      await request.jwtVerify()
    } catch (err) {
      reply.send(err)
    }
  })

  fastify.get('/profile', async (request) => {
    const userId = (request.user as any).userId
    return await prisma.identityProfile.findUnique({
      where: { userId }
    })
  })

  fastify.post('/learn', async (request) => {
    const userId = (request.user as any).userId
    const { interaction } = z.object({ interaction: z.record(z.any()) }).parse(request.body)
    
    // TODO: Implement learning algorithm
    const profile = await prisma.identityProfile.upsert({
      where: { userId },
      create: {
        userId,
        communicationStyle: {},
        responsePreferences: {},
        decisionPatterns: {},
        behaviorMetrics: {}
      },
      update: {
        learningProgress: { increment: 0.1 }
      }
    })
    
    return profile
  })
}
