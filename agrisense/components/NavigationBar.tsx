"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";

export default function NavigationBar() {
  const pathname = usePathname();
  const { isAuthenticated, logout, isLoading } = useAuth();
  const { language, setLanguage, t, options } = useLanguage();
  const [showLogout, setShowLogout] = useState(false);

  const links = [
    { label: t("nav.dashboard"), href: "/dashboard" },
    { label: t("nav.market"), href: "/market" },
    { label: t("nav.mandi"), href: "/mandi" },
    { label: t("nav.climate"), href: "/climate" },
    { label: t("nav.yield"), href: "/yield" },
    { label: t("nav.advisor"), href: "/advisor" },
    { label: t("nav.profile"), href: "/profile" },
  ];

  return (
    <>
      <nav className="h-[64px] bg-[#FDFAF4] border-b-[0.5px] border-[#D9CEB8] flex items-center justify-between px-5 md:px-[40px] sticky top-0 bg-opacity-95 backdrop-blur z-50">
        <Link href="/" className="font-display font-semibold text-[18px] flex">
          <span className="text-[#2C2416]">Agri</span>
          <span className="text-[#7A3B2E]">Sense</span>
        </Link>
        <div className="flex items-center gap-6">
          <label className="flex items-center gap-2 font-body text-[12px] text-[#7A6A55]">
            <span className="hidden md:inline">{t("nav.language")}</span>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as typeof language)}
              className="border border-[#D9CEB8] rounded-[20px] px-2.5 py-1 text-[12px] bg-[#FDFAF4] text-[#2C2416] focus:outline-none"
              aria-label={t("nav.language")}
            >
              {options.map((option) => (
                <option key={option.code} value={option.code}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          {!isLoading && !isAuthenticated && (
            <>
              <Link href="/" className="font-body text-[13px] text-[#7A6A55] hover:text-[#7A3B2E]">{t("nav.home")}</Link>
              <Link href="/signin" className="font-body text-[13px] text-[#7A6A55] hover:text-[#7A3B2E] border border-[#D9CEB8] px-[16px] py-[6px] rounded-[24px]">{t("nav.signIn")}</Link>
            </>
          )}
          {!isLoading && isAuthenticated && links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`font-body text-[13px] transition-colors ${
                  isActive
                    ? "text-[#7A3B2E] border-b-[1.5px] border-[#7A3B2E] pb-1"
                    : "text-[#7A6A55] hover:text-[#7A3B2E]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
          
          {!isLoading && isAuthenticated && (
            <button
              onClick={() => setShowLogout(true)}
              className="font-body text-[12px] font-medium text-[#7A3B2E] border-[0.5px] border-[#D9CEB8] px-4 py-1.5 rounded-[20px] hover:bg-[#EDE3D3] transition-colors ml-2"
            >
              {t("nav.logOut")}
            </button>
          )}
        </div>
      </nav>

      {showLogout && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-[#2C2416]/20 backdrop-blur-sm">
          <div className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[12px] p-6 max-w-[320px] w-[90%] flex flex-col gap-4 shadow-sm">
            <h3 className="font-display font-semibold text-[18px] text-[#2C2416]">{t("nav.signOut")}</h3>
            <p className="font-body text-[14px] text-[#7A6A55] leading-relaxed">
              {t("nav.signOutConfirm")}
            </p>
            <div className="flex gap-3 justify-end mt-2">
              <button
                onClick={() => setShowLogout(false)}
                className="px-4 py-2 rounded-[20px] font-body text-[13px] font-medium text-[#7A6A55] hover:bg-[#F5F1EA] transition-colors"
              >
                {t("nav.cancel")}
              </button>
              <button
                onClick={() => {
                  setShowLogout(false);
                  logout();
                }}
                className="px-4 py-2 rounded-[20px] font-body text-[13px] font-medium bg-[#7A3B2E] text-[#F5F0E8] hover:bg-[#683025] transition-colors"
              >
                {t("nav.confirm")}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
