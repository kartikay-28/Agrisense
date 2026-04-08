import type { Metadata } from "next";
import { Playfair_Display, DM_Sans } from "next/font/google";
import { Toaster } from "sonner";
import { AuthProvider } from "@/context/AuthContext";
import "./globals.css";
import NavigationBar from "@/components/NavigationBar";

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  weight: ["400", "600"],
  style: ["normal", "italic"],
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-dmsans",
  weight: ["300", "400", "500"],
});

export const metadata: Metadata = {
  title: "AgriSense",
  description: "Agricultural intelligence for farmers",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${playfair.variable} ${dmSans.variable} antialiased`}
      >
        <AuthProvider>
          <NavigationBar />
          <main className="max-w-[1100px] mx-auto px-5 md:px-[40px] pt-12 pb-24 min-h-screen">
            {children}
          </main>
          <Toaster position="top-right" />
        </AuthProvider>
      </body>
    </html>
  );
}
