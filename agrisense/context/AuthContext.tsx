"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  isLoading: true,
  login: () => {},
  logout: () => {},
});

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check localStorage on mount
    const authStatus = localStorage.getItem("agrisense_auth");
    if (authStatus === "true") {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const login = () => {
    localStorage.setItem("agrisense_auth", "true");
    setIsAuthenticated(true);
    toast.success("Successfully signed in", {
      style: { background: "#F5F1EA", color: "#2C2416", border: "0.5px solid #D9CEB8" },
      className: "font-body",
    });
    router.push("/dashboard");
  };

  const logout = () => {
    localStorage.removeItem("agrisense_auth");
    setIsAuthenticated(false);
    toast("You have been signed out", {
      style: { background: "#F5F1EA", color: "#7A6A55", border: "0.5px solid #D9CEB8" },
      className: "font-body",
    });
    router.push("/");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
