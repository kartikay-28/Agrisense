"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowUp, ArrowDown, Activity, RefreshCw } from "lucide-react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { getMarketData, getClimateRisk, getLLMInsight } from "@/lib/api";

export default function Dashboard() {
  const [marketData, setMarketData] = useState<any>(null);
  const [climateRisk, setClimateRisk] = useState<any>(null);
  const [aiInsight, setAiInsight] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Run API calls in parallel (defaulting to Wheat for now)
      const [marketRes, climateRes] = await Promise.all([
        getMarketData("Wheat"),
        getClimateRisk(), // defaults to current location if params not passed
      ]);

      // Handle typical FastAPI responses or mock fallbacks
      const topMarketData =
        marketRes?.data && Array.isArray(marketRes.data)
          ? marketRes.data[0]
          : marketRes;
      setMarketData(topMarketData);
      setClimateRisk(climateRes);

      // Fetch insight sequentially based on the retrieved data
      const insightRes = await getLLMInsight({
        market: topMarketData,
        climate: climateRes,
      });

      // Usually `{ insight: "..." }` or `{ response: "..." }`
      setAiInsight(
        insightRes?.insight ||
          insightRes?.response ||
          "Insights are currently unavailable based on the latest data."
      );
    } catch (err: any) {
      console.error(err);
      setError("Failed to fetch dashboard data. Please check if your backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const latestDataAge = "Just now";

  // Reusable loading skeleton
  const Skeleton = ({ className = "" }: { className?: string }) => (
    <div className={`animate-pulse bg-[#D9CEB8]/40 rounded-[10px] ${className}`}></div>
  );

  return (
    <ProtectedRoute>
      <div className="flex flex-col gap-12 max-w-[1100px] w-full mx-auto">
        
        {/* Header Area */}
        <section className="flex flex-row justify-between items-end gap-4">
          <div className="flex flex-col items-start gap-1">
            <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5">
              Your farm · {new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
            </span>
            <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
              Good morning, Rajan.
            </h1>
            <p className="font-body font-light text-[14px] text-[#7A6A55]">
              Wheat season · Week 14 of 26
            </p>
          </div>
          
          <button
            onClick={fetchDashboardData}
            disabled={loading}
            className="flex items-center justify-center gap-2 border-[0.5px] border-[#D9CEB8] text-[#5C7A52] hover:bg-[#F5F1EA] px-[16px] py-[8px] rounded-[24px] font-medium text-[12px] bg-white transition-colors disabled:opacity-50"
          >
            <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
            Refresh
          </button>
        </section>

        {error && (
          <div className="bg-[#FDFAF4] border-l-[3px] border-[#7A3B2E] p-[14px_18px] text-[#7A3B2E] font-medium text-[13px]">
            {error}
          </div>
        )}

        {/* Season Progress */}
        <section className="w-full relative">
          <span className="uppercase tracking-[0.14em] text-[#7A6A55] text-[10px] font-medium block mb-2">
            Season progress — Week 14 of 26
          </span>
          <div className="w-full h-[8px] bg-[#D9CEB8] rounded-[4px] relative mb-4">
            <div
              className="absolute left-0 top-0 h-full bg-[#5C7A52] rounded-[4px]"
              style={{ width: "53.8%" }}
            ></div>
          </div>
          <div className="flex justify-between w-full text-[11px] font-medium px-1">
            <span className="text-[#7A6A55] w-[40%] text-left">Planting</span>
            <span className="text-[#2C2416] w-[40%] text-left">Growing</span>
            <span className="text-[#7A6A55] w-[20%] text-right">Harvest</span>
          </div>
        </section>

        {/* Metric Tiles Row */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-[12px]">
          {/* Tile 1: Current Price */}
          <div className="bg-[#F5F1EA] rounded-[10px] p-[20px] flex flex-col">
            <span className="text-[#7A6A55] font-medium text-[11px] uppercase tracking-[0.06em] mb-2">
              Wheat Price (Per Quintal)
            </span>
            {loading ? (
              <Skeleton className="h-[38px] w-24 my-1" />
            ) : (
              <>
                <span className="font-display font-semibold text-[32px] text-[#5C7A52]">
                  ₹{marketData?.price ?? marketData?.current_price ?? marketData?.price_inr ?? "2,275"}
                </span>
                <div className="flex items-center text-[#5C7A52] font-medium text-[11px] mt-1 gap-1">
                  <span>Current Market Data</span>
                </div>
              </>
            )}
          </div>

          {/* Tile 2: 7-Day Change */}
          <div className="bg-[#F5F1EA] rounded-[10px] p-[20px] flex flex-col">
            <span className="text-[#7A6A55] font-medium text-[11px] uppercase tracking-[0.06em] mb-2">
              7-Day Price Change
            </span>
            {loading ? (
              <Skeleton className="h-[38px] w-24 my-1" />
            ) : (
              <>
                <span className="font-display font-semibold text-[32px] text-[#2C2416]">
                  {marketData?.price_change_7d ?? "+12.4%"}
                </span>
                <div className="flex items-center text-[#7A6A55] font-medium text-[11px] mt-1 gap-1">
                  {marketData?.price_change_7d?.startsWith("-") ? (
                    <ArrowDown size={12} className="text-[#7A3B2E]" />
                  ) : (
                    <ArrowUp size={12} className="text-[#5C7A52]" />
                  )}
                  <span>Compared to last week</span>
                </div>
              </>
            )}
          </div>

          {/* Tile 3: Volatility */}
          <div className="bg-[#F5F1EA] rounded-[10px] p-[20px] flex flex-col">
            <span className="text-[#7A6A55] font-medium text-[11px] uppercase tracking-[0.06em] mb-2">
              Market Volatility
            </span>
            {loading ? (
              <Skeleton className="h-[38px] w-24 my-1" />
            ) : (
              <>
                <span className="font-display font-semibold text-[32px] text-[#2C2416]">
                  {marketData?.volatility ?? "Moderate"}
                </span>
                <div className="flex items-center text-[#7A6A55] font-medium text-[11px] mt-1 gap-1">
                  <Activity size={12} />
                  <span>Based on recent index</span>
                </div>
              </>
            )}
          </div>
        </section>

        {/* Risk Alert Banner */}
        {loading ? (
          <Skeleton className="h-[80px] w-full" />
        ) : climateRisk ? (
          <section
            className={`border-l-[3px] p-[14px_18px] flex flex-col gap-2 ${
              climateRisk?.level === "High" || climateRisk?.risk_level === "High"
                ? "bg-[#EDE3D3] border-[#7A3B2E]"
                : climateRisk?.level === "Medium" || climateRisk?.risk_level === "Medium"
                ? "bg-[#FDF4E3] border-[#C9A97A]"
                : "bg-[#DDE8D9] border-[#5C7A52]"
            }`}
          >
            <h3
              className={`font-medium text-[12px] uppercase tracking-[0.1em] font-body ${
                climateRisk?.level === "High" || climateRisk?.risk_level === "High"
                  ? "text-[#7A3B2E]"
                  : "text-[#2C2416]"
              }`}
            >
              Climate Risk Detected: {climateRisk?.level || climateRisk?.risk_level || "Moderate"}
            </h3>
            <p className="font-body text-[13px] text-[#4A2418] leading-[1.6]">
              {climateRisk?.message ||
                climateRisk?.recommendation ||
                "Dry spell likely in the next 10 days. Soil moisture is dropping below optimal for wheat in your region. Consider irrigation adjustment by Thursday."}
            </p>
            <Link
              href="/climate"
              className="font-medium text-[12px] text-inherit hover:underline transition-all mt-1 w-max"
            >
              See full climate report →
            </Link>
          </section>
        ) : null}

        {/* AI Insight Section */}
        <section className="flex flex-col gap-0 border-t-[0.5px] border-transparent mt-2">
          <div className="bg-[#F5F1EA] p-[24px] rounded-[10px] flex flex-col h-full border border-[#E8DFC9]">
            <h3 className="font-display italic text-[16px] text-[#5C7A52] mb-3">
              What the market is telling you
            </h3>
            <div className="font-body font-light text-[13px] text-[#2C2416] leading-[1.8] flex flex-col gap-4">
              {loading ? (
                <>
                  <Skeleton className="h-4 w-[100%]" />
                  <Skeleton className="h-4 w-[90%]" />
                  <Skeleton className="h-4 w-[95%]" />
                  <Skeleton className="h-4 w-[75%]" />
                </>
              ) : (
                <p>
                  {aiInsight ||
                    "Wheat prices have surged in your region due to regional shortages and recent transport delays in the northern states. The market is pricing in a premium for immediate delivery. Since your harvest is still 12 weeks away, you won't capture this peak immediately. However, forward contracts for next quarter are also rising. We recommend holding your current stored maize slightly longer as those prices are being pulled up alongside wheat."}
                </p>
              )}
            </div>
            <div className="mt-8">
              <Link
                href="/advisor"
                className="inline-flex items-center justify-center border border-[#5C7A52] text-[#5C7A52] hover:bg-[#DDE8D9] rounded-[24px] px-[20px] py-[9px] font-medium text-[13px] transition-colors"
              >
                Ask the AI Advisor →
              </Link>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-8 pt-6 border-t-[0.5px] border-[#E8DFC9] flex justify-center">
          <p className="font-body text-[11px] text-[#7A6A55] font-light">
            Data updated {latestDataAge} · Powered by AgriSense ML
          </p>
        </footer>
      </div>
    </ProtectedRoute>
  );
}
import Link from "next/link";
import { ArrowUp, ArrowDown } from "lucide-react";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function Dashboard() {
  const latestDataAge = "15 minutes ago";

  return (
    <ProtectedRoute>
      <div className="flex flex-col gap-12 max-w-[1100px] w-full mx-auto">
      {/* Header Area */}
      <section className="flex flex-col items-start gap-1">
        <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5">
          Your farm · {new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
        </span>
        <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
          Good morning, Rajan.
        </h1>
        <p className="font-body font-light text-[14px] text-[#7A6A55]">
          Wheat season · Week 14 of 26 · Moderate risk overall
        </p>
      </section>

      {/* Season Progress */}
      <section className="w-full relative">
        <span className="uppercase tracking-[0.14em] text-[#7A6A55] text-[10px] font-medium block mb-2">
          Season progress — Week 14 of 26
        </span>
        <div className="w-full h-[8px] bg-[#D9CEB8] rounded-[4px] relative mb-4">
          <div
            className="absolute left-0 top-0 h-full bg-[#5C7A52] rounded-[4px]"
            style={{ width: "53.8%" }}
          ></div>
        </div>
        <div className="flex justify-between w-full text-[11px] font-medium px-1">
          <span className="text-[#7A6A55] w-[40%] text-left">Planting</span>
          <span className="text-[#2C2416] w-[40%] text-left">Growing</span>
          <span className="text-[#7A6A55] w-[20%] text-right">Harvest</span>
        </div>
      </section>

      {/* Metric Tiles Row */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-[12px]">
        {/* Tile 1 */}
        <div className="bg-[#F5F1EA] rounded-[10px] p-[20px] flex flex-col">
          <span className="text-[#7A6A55] font-medium text-[11px] uppercase tracking-[0.06em] mb-2">
            Wheat price · 7 days
          </span>
          <span className="font-display font-semibold text-[32px] text-[#5C7A52]">
            ₹2,275
          </span>
          <div className="flex items-center text-[#5C7A52] font-medium text-[11px] mt-1 gap-1">
            <ArrowUp size={12} strokeWidth={3} />
            <span>+12.4%</span>
          </div>
        </div>

        {/* Tile 2 */}
        <div className="bg-[#F5F1EA] rounded-[10px] p-[20px] flex flex-col">
          <span className="text-[#7A6A55] font-medium text-[11px] uppercase tracking-[0.06em] mb-2">
            Rain forecast · Next 10 days
          </span>
          <span className="font-display font-semibold text-[32px] text-[#7A3B2E]">
            Low
          </span>
          <div className="flex items-center text-[#7A3B2E] font-medium text-[11px] mt-1 gap-1">
            <ArrowDown size={12} strokeWidth={3} />
            <span>-80% vs avg</span>
          </div>
        </div>

        {/* Tile 3 */}
        <div className="bg-[#F5F1EA] rounded-[10px] p-[20px] flex flex-col">
          <span className="text-[#7A6A55] font-medium text-[11px] uppercase tracking-[0.06em] mb-2">
            Yield confidence
          </span>
          <span className="font-display font-semibold text-[32px] text-[#2C2416]">
            78%
          </span>
          <div className="flex items-center text-[#7A6A55] font-medium text-[11px] mt-1 gap-1">
            <span>Stable from yesterday</span>
          </div>
        </div>
      </section>

      {/* Risk Alert Banner */}
      <section className="bg-[#EDE3D3] border-l-[3px] border-[#7A3B2E] p-[14px_18px] flex flex-col gap-2">
        <h3 className="font-medium text-[12px] uppercase tracking-[0.1em] text-[#7A3B2E] font-body">
          Risk detected
        </h3>
        <p className="font-body text-[13px] text-[#4A2418] leading-[1.6]">
          Dry spell likely in the next 10 days. Soil moisture is dropping below optimal for wheat in your region. Consider irrigation adjustment by Thursday.
        </p>
        <Link
          href="/climate"
          className="font-medium text-[12px] text-[#7A3B2E] hover:underline transition-all mt-1 w-max"
        >
          See full climate report →
        </Link>
      </section>

      {/* Two-column layout */}
      <section className="grid grid-cols-1 md:grid-cols-5 gap-6">
        {/* Left: Market Snapshot */}
        <div className="md:col-span-3 flex flex-col gap-4">
          <h2 className="font-display font-semibold text-[18px] text-[#2C2416]">
            Market snapshot
          </h2>
          <div className="flex flex-col gap-3">
            {[
              { name: "Wheat", price: "₹2,275", change: "+12.4%", trend: "up" },
              { name: "Rice", price: "₹3,150", change: "-2.1%", trend: "down" },
              { name: "Maize", price: "₹2,050", change: "+4.5%", trend: "up" },
            ].map((crop) => (
              <Link key={crop.name} href="/market" className="block group">
                <div className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[12px] p-[20px_24px] flex items-center justify-between transition-colors group-hover:bg-[#F5F1EA]">
                  <div className="flex flex-col gap-3">
                    <span className="font-medium text-[14px] text-[#2C2416] font-body">
                      {crop.name}
                    </span>
                    <div className="flex flex-col gap-1">
                      <span className="uppercase tracking-[0.14em] font-medium text-[10px] text-[#7A6A55]">
                        7-day change
                      </span>
                      <span
                        className={`inline-block px-2.5 py-1 text-[11px] font-medium rounded-[4px] w-max ${
                          crop.trend === "up"
                            ? "bg-[#DDE8D9] text-[#3A5E32]"
                            : "bg-[#EDE3D3] text-[#7A3B2E]"
                        }`}
                      >
                        {crop.change}
                      </span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-3">
                    <span className="font-medium text-[14px] text-[#2C2416] font-body">
                      {crop.price}
                    </span>
                    <div className="flex items-end h-[24px] gap-[2px]">
                      {/* Mini sparkline visualization */}
                      {[40, 60, 45, 70, 50, 80, crop.trend === "up" ? 100 : 30].map(
                        (val, i) => (
                          <div
                            key={i}
                            className={`w-[4px] rounded-t-[1px] ${
                              crop.trend === "up"
                                ? "bg-[#5C7A52]"
                                : "bg-[#7A3B2E]"
                            }`}
                            style={{ height: `${val}%` }}
                          />
                        )
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Right: AI Insight */}
        <div className="md:col-span-2 flex flex-col gap-0 border-t-[0.5px] border-transparent">
          <h2 className="font-display font-semibold text-[18px] text-[#2C2416] mb-4 invisible md:visible">
            Insight
          </h2>
          <div className="bg-[#F5F1EA] py-[10px] flex flex-col h-full">
            <h3 className="font-display italic text-[16px] text-[#5C7A52] mb-3">
              What the market is telling you
            </h3>
            <div className="font-body font-light text-[13px] text-[#2C2416] leading-[1.8] flex flex-col gap-4">
              <p>
                Wheat prices have surged in your region due to regional shortages and recent transport delays in the northern states. The market is pricing in a premium for immediate delivery.
              </p>
              <p>
                Since your harvest is still 12 weeks away, you won&apos;t capture this peak immediately. However, forward contracts for next quarter are also rising. We recommend holding your current stored maize slightly longer as those prices are being pulled up alongside wheat.
              </p>
            </div>
            <div className="mt-8">
              <Link
                href="/advisor"
                className="inline-flex items-center justify-center border border-[#5C7A52] text-[#5C7A52] hover:bg-[#DDE8D9] rounded-[24px] px-[20px] py-[9px] font-medium text-[13px] transition-colors"
              >
                Ask the AI Advisor →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-8 pt-6 border-t-[0.5px] border-[#E8DFC9] flex justify-center">
        <p className="font-body text-[11px] text-[#7A6A55] font-light">
          Data updated {latestDataAge} · Powered by AgriSense ML
        </p>
      </footer>
    </div>
    </ProtectedRoute>
  );
}
