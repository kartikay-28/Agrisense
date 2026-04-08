"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      toast.error("Please sign in to continue", {
        style: { background: "#EDE3D3", color: "#7A3B2E", border: "0.5px solid #D9CEB8" },
        className: "font-body",
      });
      router.replace("/signin"); // Using replace to avoid back-button loops
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 w-full">
        <div className="bg-[#F5F1EA] px-[24px] py-[12px] rounded-[8px] animate-pulse shadow-sm">
          <p className="font-body italic text-[14px] text-[#7A6A55]">
            AgriSense is verifying...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return <>{children}</>;
}
