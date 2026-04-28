"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { signOut } from "next-auth/react";

export interface UserProfile {
  name: string;
  crop: string;
  season: string;
  acres: number;
  location: string;
}

const defaultProfile: UserProfile = {
  name: "Rajan",
  crop: "Wheat",
  season: "Rabi",
  acres: 5,
  location: "Punjab",
};

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: UserProfile;
  login: (profile?: Partial<UserProfile>) => void;
  logout: () => void;
  updateProfile: (profile: Partial<UserProfile>) => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  isLoading: true,
  user: defaultProfile,
  login: () => {},
  logout: () => {},
  updateProfile: () => {},
});

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<UserProfile>(defaultProfile);
  const router = useRouter();

  useEffect(() => {
    // Auth should only live for the active browser session.
    const authStatus = sessionStorage.getItem("agrisense_auth");
    if (authStatus === "true") {
      setIsAuthenticated(true);
      const savedProfile = localStorage.getItem("agrisense_profile");
      if (savedProfile) {
        setUser(JSON.parse(savedProfile));
      }
    }
    // Clear any legacy persistent auth flag from older builds.
    localStorage.removeItem("agrisense_auth");
    setIsLoading(false);
  }, []);

  const login = (profile?: Partial<UserProfile>) => {
    sessionStorage.setItem("agrisense_auth", "true");
    
    // Check if we already have a saved profile, if not use default + any passed fields
    let profileToSave = user;
    const savedStr = localStorage.getItem("agrisense_profile");
    if (savedStr) {
      profileToSave = { ...JSON.parse(savedStr), ...profile };
    } else {
      profileToSave = { ...defaultProfile, ...profile };
    }
    
    localStorage.setItem("agrisense_profile", JSON.stringify(profileToSave));
    setUser(profileToSave);
    setIsAuthenticated(true);
    
    toast.success(`Welcome back, ${profileToSave.name}`, {
      style: { background: "#F5F1EA", color: "#2C2416", border: "0.5px solid #D9CEB8" },
      className: "font-body",
    });
    router.push("/dashboard");
  };

  const logout = () => {
    sessionStorage.removeItem("agrisense_auth");
    localStorage.removeItem("agrisense_auth");
    // We intentionally keep profile data in local storage so it's remembered next time,
    // or we could remove it. Let's keep it.
    setIsAuthenticated(false);
    void signOut({ redirect: false });
    toast("You have been signed out", {
      style: { background: "#F5F1EA", color: "#7A6A55", border: "0.5px solid #D9CEB8" },
      className: "font-body",
    });
    router.push("/");
  };

  const updateProfile = (profileUpdates: Partial<UserProfile>) => {
    const updated = { ...user, ...profileUpdates };
    setUser(updated);
    localStorage.setItem("agrisense_profile", JSON.stringify(updated));
    toast.success("Profile updated successfully", {
      style: { background: "#F5F1EA", color: "#2C2416", border: "0.5px solid #D9CEB8" },
      className: "font-body",
    });
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, user, login, logout, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
}
