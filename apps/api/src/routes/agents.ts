import { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import { prisma } from '../lib/prisma'

const createAgentSchema = z.object({
  name: z.string(),
  type: z.enum(['LOTL', 'OSINT', 'SECURITY', 'DATA', 'TASK', 'QUICK']),
  description: z.string().optional(),
  config: z.record(z.any())
})

export const agentRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.addHook('preHandler', async (request, reply) => {
    try {
      await request.jwtVerify()
    } catch (err) {
      reply.send(err)
    }
  })

  fastify.get('/', async (request) => {
    const userId = (request.user as any).userId
    return await prisma.agent.findMany({
      where: { userId },
      include: { tasks: true }
    })
  })

  fastify.post('/', async (request) => {
    const userId = (request.user as any).userId
    const data = createAgentSchema.parse(request.body)
    
    return await prisma.agent.create({
      data: { ...data, userId }
    })
  })

  fastify.patch('/:id/status', async (request) => {
    const { id } = request.params as { id: string }
    const { status } = z.object({ status: z.enum(['ACTIVE', 'INACTIVE', 'ERROR', 'MAINTENANCE']) }).parse(request.body)
    
    return await prisma.agent.update({
      where: { id },
      data: { status }
    })
  })
}
