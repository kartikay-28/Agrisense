"use client";

import { useState } from "react";
import Link from "next/link";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function YieldPage() {
  const [rainfall, setRainfall] = useState(120);
  const [fertilizer, setFertilizer] = useState(80);
  const [irrigation, setIrrigation] = useState(2); // 1 = Low, 2 = Med, 3 = High

  const baseYield = 4.8;
  const rainFactor = (rainfall - 100) * 0.005;
  const fertFactor = (fertilizer - 50) * 0.01;
  const irrFactor = (irrigation - 1) * 0.15;

  const predictedYield = (baseYield + rainFactor + fertFactor + irrFactor).toFixed(1);

  return (
    <ProtectedRoute>
    <div className="flex flex-col gap-12 max-w-[1100px] w-full mx-auto pb-10">
      {/* Header */}
      <section className="flex flex-col items-start gap-1 w-full relative">
        <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5 flex justify-between w-max gap-4 items-center">
          Yield prediction
        </span>
        <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
          How much will you harvest?
        </h1>
        <p className="font-body font-light text-[14px] text-[#7A6A55]">
          ML-powered estimate based on your field data, weather, and market inputs
        </p>
      </section>

      {/* Field Selector */}
      <section className="flex flex-col gap-2 w-full md:w-1/3">
        <label className="font-body font-medium text-[11px] uppercase tracking-[0.1em] text-[#7A6A55]">
          Select field
        </label>
        <select className="h-[40px] bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-[14px] font-body text-[13px] text-[#2C2416] focus:outline-none focus:border-[#7A3B2E] appearance-none">
          <option>North Field — 4.2 acres · Wheat</option>
          <option>South Field — 2.8 acres · Rice</option>
          <option>East Sector — 3.1 acres · Maize</option>
        </select>
      </section>

      {/* Comparison Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">
        {/* Prediction */}
        <div className="bg-[#FDFAF4] rounded-[12px] border-[0.5px] border-[#D9CEB8] p-[32px] flex flex-col gap-2 items-center text-center shadow-sm relative">
          <span className="font-body text-[14px] font-medium text-[#2C2416]">
            Predicted yield
          </span>
          <h2 className="font-display font-semibold text-[48px] text-[#5C7A52] my-2">
            {predictedYield} <span className="font-body text-[20px] font-light text-[#7A6A55]">tons/acre</span>
          </h2>
          <span className="bg-[#DDE8D9] text-[#3A5E32] rounded-[20px] px-[12px] py-[4px] uppercase text-[10px] tracking-[0.1em] font-bold">
            High confidence (82%)
          </span>
        </div>

        {/* Historical Average */}
        <div className="bg-[#F5F1EA] rounded-[12px] p-[32px] flex flex-col gap-2 items-center text-center">
          <span className="font-body text-[14px] font-medium text-[#7A6A55]">
            Historical average
          </span>
          <h2 className="font-display font-semibold text-[48px] text-[#7A6A55] my-2">
            4.2 <span className="font-body text-[20px] font-light text-[#A89E89]">tons/acre</span>
          </h2>
          <span className="text-[#A89E89] text-[12px] font-light">
            Based on your last 4 seasons
          </span>
        </div>
      </section>

      {/* Confidence Breakdown Indicators */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
        {[
          { label: "Weather factor", score: "8.5 / 10", c: "text-[#5C7A52]" },
          { label: "Soil factor", score: "7.0 / 10", c: "text-[#B07A3A]" },
          { label: "Market factor", score: "9.2 / 10", c: "text-[#5C7A52]" },
        ].map((f, i) => (
          <div key={i} className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] p-[16px] rounded-[10px] flex justify-between items-center">
            <span className="font-body text-[13px] text-[#7A6A55] font-medium">
              {f.label}
            </span>
            <span className={`font-display font-semibold text-[18px] ${f.c}`}>
              {f.score}
            </span>
          </div>
        ))}
      </section>

      {/* Interactive Sliders */}
      <section className="flex flex-col gap-6 bg-[#F5F1EA] p-[24px] rounded-[12px]">
        <h3 className="font-display font-semibold text-[18px] text-[#2C2416] mb-2">
          Adjust assumptions
        </h3>

        {/* Slider 1 */}
        <div className="flex flex-col gap-3">
          <div className="flex justify-between w-full">
            <label className="font-body text-[13px] text-[#7A6A55]">Expected rainfall (mm)</label>
            <span className="font-medium text-[13px] text-[#2C2416]">{rainfall} mm</span>
          </div>
          <input
            type="range"
            min="0"
            max="200"
            value={rainfall}
            onChange={(e) => setRainfall(Number(e.target.value))}
            className="w-full accent-[#7A3B2E]"
          />
        </div>

        {/* Slider 2 */}
        <div className="flex flex-col gap-3">
          <div className="flex justify-between w-full">
            <label className="font-body text-[13px] text-[#7A6A55]">Fertilizer application (%)</label>
            <span className="font-medium text-[13px] text-[#2C2416]">{fertilizer}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value={fertilizer}
            onChange={(e) => setFertilizer(Number(e.target.value))}
            className="w-full accent-[#5C7A52]"
          />
        </div>

        {/* Slider 3 */}
        <div className="flex flex-col gap-3">
          <div className="flex justify-between w-full">
            <label className="font-body text-[13px] text-[#7A6A55]">Irrigation frequency</label>
            <span className="font-medium text-[13px] text-[#2C2416]">
              {irrigation === 1 ? "Low" : irrigation === 2 ? "Medium" : "High"}
            </span>
          </div>
          <input
            type="range"
            min="1"
            max="3"
            step="1"
            value={irrigation}
            onChange={(e) => setIrrigation(Number(e.target.value))}
            className="w-full accent-[#C9A97A]"
          />
        </div>
      </section>

      {/* AI Insight Block */}
      <section className="bg-[#F5F1EA] p-[24px] rounded-[10px]">
        <h2 className="font-display italic text-[16px] text-[#5C7A52] mb-3">
          Why your yield is projected this way
        </h2>
        <div className="font-body font-light text-[13px] text-[#2C2416] leading-[1.8] flex flex-col gap-4">
          <p>
            Your current planting density naturally supports an above-average yield. This is bolstered entirely by robust sunlight patterns early in the season, meaning stalks are taller and more established than the local block average.
          </p>
          <p>
            The model sees the heaviest deviation coming from your upcoming fertilizer application rate. Adjusting the amount up toward 80% ensures the rapid growth phase continues unimpeded, pushing your final tons-per-acre firmly above historical trends.
          </p>
        </div>
      </section>

      {/* Action Row */}
      <section className="flex flex-col md:flex-row gap-4 pt-4 items-center">
        <button className="bg-[#7A3B2E] text-[#F5F0E8] rounded-[24px] px-[28px] py-[12px] font-medium text-[14px] hover:opacity-90 transition-opacity w-full md:w-auto">
          Download yield report (PDF)
        </button>
        <Link
          href="/advisor"
          className="border border-[#5C7A52] text-[#5C7A52] rounded-[24px] px-[28px] py-[12px] font-medium text-[14px] hover:bg-[#DDE8D9] transition-colors w-full md:w-auto text-center"
        >
          Ask the AI Advisor about this
        </Link>
      </section>
    </div>
    </ProtectedRoute>
  );
}
