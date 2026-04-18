import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/",
  },
});

export const config = {
  matcher: ['/dashboard', '/market', '/climate', '/yield', '/advisor', '/profile', '/mandi']
};