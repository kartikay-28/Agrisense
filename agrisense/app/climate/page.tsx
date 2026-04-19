"use client";

import Link from "next/link";
import { ArrowUp, ArrowDown } from "lucide-react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/context/AuthContext";

export default function Climate() {
  const { user } = useAuth();
  
  const days = [
    { name: "Mon", temp: "22-29°", rain: "Low rain", risk: "Low", rLabel: "bg-[#DDE8D9] text-[#3A5E32]" },
    { name: "Tue", temp: "23-31°", rain: "Dry", risk: "Moderate", rLabel: "bg-[#F0E4CC] text-[#B07A3A]" },
    { name: "Wed", temp: "25-33°", rain: "Dry", risk: "High", rLabel: "bg-[#EDE3D3] text-[#7A3B2E]" },
    { name: "Thu", temp: "26-34°", rain: "Dry", risk: "High", rLabel: "bg-[#EDE3D3] text-[#7A3B2E]" },
    { name: "Fri", temp: "24-32°", rain: "Moderate", risk: "Moderate", rLabel: "bg-[#F0E4CC] text-[#B07A3A]" },
    { name: "Sat", temp: "22-28°", rain: "Heavy", risk: "Moderate", rLabel: "bg-[#F0E4CC] text-[#B07A3A]" },
    { name: "Sun", temp: "21-27°", rain: "Low rain", risk: "Low", rLabel: "bg-[#DDE8D9] text-[#3A5E32]" },
    { name: "Mon", temp: "20-25°", rain: "Dry", risk: "Low", rLabel: "bg-[#DDE8D9] text-[#3A5E32]" },
    { name: "Tue", temp: "21-27°", rain: "Low rain", risk: "Low", rLabel: "bg-[#DDE8D9] text-[#3A5E32]" },
    { name: "Wed", temp: "23-29°", rain: "Dry", risk: "Moderate", rLabel: "bg-[#F0E4CC] text-[#B07A3A]" },
  ];

  return (
    <ProtectedRoute>
    <div className="flex flex-col gap-12 max-w-[1100px] w-full mx-auto pb-10">
      {/* Header */}
      <section className="flex flex-col items-start gap-1 w-full relative">
        <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5 flex justify-between w-max gap-4 items-center">
          Climate & weather risk
        </span>
        <div className="flex w-full items-center justify-between">
          <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
            Weather forecast & field risk
          </h1>
          <span className="bg-[#F0E4CC] text-[#B07A3A] px-[12px] py-[4px] rounded-[20px] font-medium uppercase text-[11px] tracking-[0.08em] shadow-sm">
            Moderate Risk
          </span>
        </div>
        <p className="font-body font-light text-[14px] text-[#7A6A55]">
          Understand upcoming climate risks
        </p>
      </section>

      {/* 10-day forecast */}
      <section className="flex gap-3 overflow-x-auto pb-2 scrollbar-none w-full snap-x snap-mandatory">
        {days.map((d, i) => (
          <div
            key={i}
            className={`min-w-[100px] flex-1 bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[10px] p-[12px_8px] flex flex-col items-center gap-3 text-center snap-center ${
              i === 0 ? "border-[#7A3B2E] border-[1.5px]" : ""
            }`}
          >
            <span className="font-body text-[11px] uppercase text-[#7A6A55] tracking-[0.1em] font-medium">
              {d.name}
            </span>
            <span className="font-body text-[13px] text-[#2C2416] font-medium">
              {d.temp}
            </span>
            <div className="flex flex-col items-center gap-1.5">
              <span className="font-body text-[10px] text-[#5C7A52]">
                {d.rain}
              </span>
              <span
                className={`px-2 py-0.5 text-[9px] uppercase tracking-[0.08em] font-medium rounded-[4px] ${d.rLabel}`}
              >
                {d.risk}
              </span>
            </div>
          </div>
        ))}
      </section>

      {/* Risk Summary Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { title: "Drought risk", label: "High Risk", rLabel: "bg-[#EDE3D3] text-[#7A3B2E]", text: "Soil moisture dropping rapidly. High probability of drought stress." },
          { title: "Flood risk", label: "Low Risk", rLabel: "bg-[#DDE8D9] text-[#3A5E32]", text: "No heavy precipitation expected. Flooding probability negligible." },
          { title: "Frost risk", label: "Low Risk", rLabel: "bg-[#DDE8D9] text-[#3A5E32]", text: "Temperatures remain safely above 20°C minimum thresholds." },
        ].map((risk, i) => (
          <div key={i} className="bg-[#F5F1EA] rounded-[12px] p-[20px_24px] flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <h3 className="font-display font-semibold text-[15px] text-[#2C2416]">
                {risk.title}
              </h3>
              <span className={`px-3 py-1 text-[10px] uppercase font-bold rounded-[20px] ${risk.rLabel}`}>
                {risk.label}
              </span>
            </div>
            <p className="font-body text-[13px] text-[#7A6A55] font-light leading-relaxed">
              {risk.text}
            </p>
          </div>
        ))}
      </section>

      {/* Irrigation Recommendation */}
      <section className="bg-[#DDE8D9] border-l-[3px] border-[#5C7A52] p-[16px_20px] w-full">
        <h3 className="font-body font-medium text-[14px] text-[#3A5E32] mb-1">
          Irrigation recommendation
        </h3>
        <p className="font-body text-[14px] text-[#4A2418] leading-[1.6]">
          Based on the dry forecast, irrigate your {user.crop.toLowerCase()} field on Tuesday and Friday this week. Estimated water needed: 18mm per session.
        </p>
      </section>

      {/* AI Insight Block */}
      <section className="bg-[#F5F1EA] p-[24px] rounded-[10px]">
        <h2 className="font-display italic text-[16px] text-[#5C7A52] mb-3">
          How this weather affects your crops
        </h2>
        <div className="font-body font-light text-[13px] text-[#2C2416] leading-[1.8] flex flex-col gap-4">
          <p>
            The upcoming heat wave on Wednesday and Thursday (reaching 34°) coincides with the early growing phase of your {user.crop.toLowerCase()}. This heat stress can limit early root development unless soil moisture is actively maintained.
          </p>
          <p>
            With the moderate rain expected on Friday, we recommend holding off on heavy secondary fertilization until after the showers pass, ensuring nutrients aren&apos;t washed away prematurely.
          </p>
        </div>
      </section>

      {/* Historical Context */}
      <section className="border-t-[0.5px] border-[#E8DFC9] pt-6 flex justify-center text-center">
        <p className="font-body italic font-light text-[13px] text-[#7A6A55] max-w-[600px]">
          Rainfall this month is 34% below the 10-year average for {user.location}. Similar patterns in 2019 and 2021 led to 8–12% yield reduction without immediate irrigation.
        </p>
      </section>
    </div>
    </ProtectedRoute>
  );
}
