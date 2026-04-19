"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { signIn } from "next-auth/react";

export default function SignIn() {
  const { login, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, router]);

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Use NextAuth's CredentialsProvider to sign in (demo auth)
      const result = await signIn("credentials", {
        redirect: false,
        email: "farmer@agrisense.com",
        password: "demo",
      });

      if (result?.ok) {
        // Also set the local auth flag for consistency
        login();
      } else {
        console.error("SignIn failed:", result?.error);
      }
    } catch (error) {
      console.error("SignIn error:", error);
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      const result = await signIn("google", {
        redirect: false,
      });
      // In a real environment redirect triggers, so if not redirected immediately:
      if (result?.ok) {
         // Create mock google user profile
         login({ name: "Google User", location: "Punjab", crop: "Maize", season: "Rabi", acres: 10 });
      } else {
         // Mock it entirely for demo since clientID may be missing!
         login({ name: "Google Farmer", location: "Haryana", crop: "Wheat", season: "Rabi", acres: 12 });
      }
    } catch (err) {
      console.error(err);
      // Fallback trigger
      login({ name: "Google Farmer", location: "Haryana", crop: "Wheat", season: "Rabi", acres: 12 });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)] w-full">
      <div className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[16px] p-10 w-[90%] max-w-[400px] flex flex-col gap-6 shadow-sm">
        <div className="text-center flex flex-col gap-2">
          <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
            Welcome back
          </h1>
          <p className="font-body text-[13px] text-[#7A6A55]">
            Sign in to access your farm&apos;s intelligence.
          </p>
        </div>

        <form className="flex flex-col gap-4 w-full" onSubmit={handleSignIn}>
          <div className="flex flex-col gap-1">
            <label className="font-body font-medium text-[11px] text-[#7A6A55] uppercase tracking-[0.1em]">
              Email
            </label>
            <input
              type="email"
              placeholder="e.g. rajan@farm.com"
              className="h-[44px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-3 font-body text-[13px] focus:outline-none focus:border-[#7A3B2E] transition-colors placeholder-[#A89E89]"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="font-body font-medium text-[11px] text-[#7A6A55] uppercase tracking-[0.1em]">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="h-[44px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-3 font-body text-[13px] focus:outline-none focus:border-[#7A3B2E] transition-colors placeholder-[#A89E89]"
            />
          </div>

          <button
            type="submit"
            className="bg-[#7A3B2E] text-[#F5F0E8] w-full py-[12px] rounded-[24px] font-medium text-[14px] text-center mt-2 hover:bg-[#683025] transition-colors"
          >
            Sign In
          </button>
        </form>

        <div className="flex flex-col gap-4 mt-2">
          <div className="relative border-t-[0.5px] border-[#D9CEB8] w-full flex items-center justify-center">
            <span className="bg-[#FDFAF4] px-3 absolute text-[11px] text-[#7A6A55] uppercase tracking-[0.05em]">
              Or
            </span>
          </div>

          <button onClick={handleGoogleSignIn} type="button" className="border-[0.5px] border-[#D9CEB8] text-[#2C2416] w-full py-[12px] rounded-[24px] font-medium text-[13px] flex items-center justify-center gap-2 hover:bg-[#F5F1EA] transition-colors cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Continue with Google
          </button>
        </div>
      </div>
    </div>
  );
}
