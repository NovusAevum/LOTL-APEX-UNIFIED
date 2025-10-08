import { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import { prisma } from '../lib/prisma'

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6)
})

const registerSchema = z.object({
  email: z.string().email(),
  username: z.string().min(3),
  password: z.string().min(6)
})

export const authRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.post('/login', async (request, reply) => {
    const { email, password } = loginSchema.parse(request.body)
    
    // TODO: Implement password hashing and verification
    const user = await prisma.user.findUnique({ where: { email } })
    
    if (!user) {
      return reply.code(401).send({ error: 'Invalid credentials' })
    }
    
    const token = fastify.jwt.sign({ userId: user.id })
    return { token, user: { id: user.id, email: user.email, username: user.username } }
  })

  fastify.post('/register', async (request, reply) => {
    const { email, username, password } = registerSchema.parse(request.body)
    
    // TODO: Implement password hashing
    const user = await prisma.user.create({
      data: { email, username, password }
    })
    
    const token = fastify.jwt.sign({ userId: user.id })
    return { token, user: { id: user.id, email: user.email, username: user.username } }
  })
}
