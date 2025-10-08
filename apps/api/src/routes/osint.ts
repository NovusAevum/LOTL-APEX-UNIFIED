import { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import { prisma } from '../lib/prisma'

const createInvestigationSchema = z.object({
  title: z.string(),
  description: z.string().optional(),
  type: z.enum(['DOMAIN_RECON', 'SOCIAL_MEDIA', 'THREAT_INTEL', 'VULNERABILITY', 'COMPLIANCE']),
  targets: z.array(z.string())
})

export const osintRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.addHook('preHandler', async (request, reply) => {
    try {
      await request.jwtVerify()
    } catch (err) {
      reply.send(err)
    }
  })

  fastify.get('/investigations', async (request) => {
    const userId = (request.user as any).userId
    return await prisma.investigation.findMany({
      where: { userId },
      include: { osintData: true }
    })
  })

  fastify.post('/investigations', async (request) => {
    const userId = (request.user as any).userId
    const data = createInvestigationSchema.parse(request.body)
    
    return await prisma.investigation.create({
      data: { 
        ...data, 
        userId,
        findings: {}
      }
    })
  })

  fastify.post('/scan/domain', async (request) => {
    const { domain } = z.object({ domain: z.string() }).parse(request.body)
    
    // TODO: Implement actual domain scanning
    return {
      domain,
      status: 'scanned',
      results: {
        whois: {},
        dns: {},
        subdomains: [],
        ports: []
      }
    }
  })
}
