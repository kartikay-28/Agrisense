import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import GoogleProvider from 'next-auth/providers/google'

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Demo Login',
      credentials: {},
      async authorize() {
        return { id: '1', name: 'Demo Farmer', email: 'farmer@agrisense.com' }
      },
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || 'dummy-client-id',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || 'dummy-client-secret',
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET || 'fallback-secret-for-dev',
  pages: { signIn: '/', error: '/' },
  callbacks: {
    async redirect({ url, baseUrl }) {
      return baseUrl;
    },
  },
})

export { handler as GET, handler as POST }
