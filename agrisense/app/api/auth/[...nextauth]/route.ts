import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Demo Login',
      credentials: {},
      async authorize() {
        return { id: '1', name: 'Demo Farmer', email: 'farmer@agrisense.com' }
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  pages: { signIn: '/', error: '/' },
})

export { handler as GET, handler as POST }
