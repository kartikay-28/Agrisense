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
      // FIXED: Google OAuth client configuration
      // Ensure these environment variables are actually in your .env or .env.local file!
      clientId: process.env.GOOGLE_CLIENT_ID || process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "dummy-client-id",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "dummy-client-secret",
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
