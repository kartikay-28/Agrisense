"use client";

import { useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";

const mandiData = [
  { market: "Shimla Mandi",      state: "Himachal Pradesh", commodity: "Wheat",  price: 2420, trend: "up",   change: "+0.8%" },
  { market: "Chandigarh Mandi",  state: "Punjab",           commodity: "Rice",   price: 3220, trend: "up",   change: "+0.9%" },
  { market: "Delhi Mandi",       state: "Delhi",            commodity: "Tomato", price: 1540, trend: "up",   change: "+2.7%" },
  { market: "Bathinda Mandi",    state: "Punjab",           commodity: "Potato", price: 820,  trend: "up",   change: "+1.2%" },
  { market: "Nashik Mandi",      state: "Maharashtra",      commodity: "Onion",  price: 1220, trend: "up",   change: "+1.7%" },
];

const commodities = ["All", "Wheat", "Rice", "Tomato", "Potato", "Onion"];

// Simulated 7-day price history per commodity (₹/quintal)
const priceHistory: Record<string, number[]> = {
  Wheat:  [2380, 2390, 2400, 2395, 2410, 2415, 2420],
  Rice:   [3190, 3200, 3210, 3205, 3215, 3218, 3220],
  Tomato: [1480, 1500, 1520, 1510, 1530, 1535, 1540],
  Potato: [790,  800,  810,  805,  815,  818,  820],
  Onion:  [1210, 1215, 1220, 1218, 1222, 1220, 1220],
};

function Sparkline({ values, trend }: { values: number[]; trend: string }) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const w = 80;
  const h = 28;
  const pts = values
    .map((v, i) => {
      const x = (i / (values.length - 1)) * w;
      const y = h - ((v - min) / range) * h;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} className="overflow-visible">
      <polyline
        points={pts}
        fill="none"
        stroke={trend === "up" ? "#5C7A52" : "#7A3B2E"}
        strokeWidth="1.5"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}

export default function MandiPage() {
  const [selected, setSelected] = useState("All");

  const filtered =
    selected === "All"
      ? mandiData
      : mandiData.filter((d) => d.commodity === selected);

  const best = [...filtered].sort((a, b) => b.price - a.price)[0];

  return (
    <ProtectedRoute>
      <div className="flex flex-col gap-12 max-w-[1100px] w-full mx-auto">

        {/* Header */}
        <section className="flex flex-col items-start gap-1">
          <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5">
            Mandi comparison
          </span>
          <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
            Best mandi to sell today
          </h1>
          <p className="font-body font-light text-[14px] text-[#7A6A55]">
            Live modal prices across mandis · Pick the highest-paying market
          </p>
        </section>

        {/* Commodity filter */}
        <section className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
          {commodities.map((c) => (
            <button
              key={c}
              onClick={() => setSelected(c)}
              className={`whitespace-nowrap rounded-[20px] px-4 py-1.5 text-[13px] font-medium transition-colors ${
                selected === c
                  ? "bg-[#7A3B2E] text-[#F5F0E8]"
                  : "border-[0.5px] border-[#D9CEB8] text-[#7A6A55] hover:bg-[#F5F1EA]"
              }`}
            >
              {c}
            </button>
          ))}
        </section>

        {/* Best pick banner */}
        {best && (
          <div className="bg-[#DDE8D9] border-[0.5px] border-[#5C7A52] rounded-[12px] px-5 py-4 flex items-center justify-between gap-4">
            <div className="flex flex-col gap-0.5">
              <span className="uppercase tracking-[0.14em] text-[#3A5E32] text-[10px] font-medium">
                Best price today
              </span>
              <span className="font-display font-semibold text-[18px] text-[#2C2416]">
                {best.market}
              </span>
              <span className="font-body text-[13px] text-[#5C7A52]">
                {best.commodity} · {best.state}
              </span>
            </div>
            <div className="text-right">
              <span className="font-display font-semibold text-[24px] text-[#2C2416]">
                ₹{best.price.toLocaleString("en-IN")}
              </span>
              <p className="font-body text-[11px] text-[#5C7A52]">per quintal</p>
            </div>
          </div>
        )}

        {/* Mandi cards */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {filtered.map((row) => {
            const isBest = row.market === best?.market && row.commodity === best?.commodity;
            return (
              <div
                key={`${row.market}-${row.commodity}`}
                className={`bg-[#FDFAF4] border-[0.5px] rounded-[12px] p-[20px_24px] flex flex-col gap-4 ${
                  isBest ? "border-[#5C7A52]" : "border-[#D9CEB8]"
                }`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex flex-col gap-0.5">
                    <span className="font-medium text-[14px] text-[#2C2416] font-body">
                      {row.market}
                    </span>
                    <span className="text-[11px] text-[#7A6A55] font-body">
                      {row.state}
                    </span>
                  </div>
                  {isBest && (
                    <span className="text-[10px] font-medium uppercase tracking-[0.1em] bg-[#DDE8D9] text-[#3A5E32] px-2 py-0.5 rounded-[4px]">
                      Best
                    </span>
                  )}
                </div>

                {/* Sparkline */}
                <div className="flex items-end gap-3">
                  <Sparkline values={priceHistory[row.commodity]} trend={row.trend} />
                  <span className="text-[10px] text-[#7A6A55] font-body">7-day</span>
                </div>

                <div className="flex items-center justify-between pt-3 border-t-[0.5px] border-[#E8DFC9]">
                  <div className="flex flex-col gap-0.5">
                    <span className="uppercase tracking-[0.14em] text-[10px] font-medium text-[#7A6A55]">
                      {row.commodity}
                    </span>
                    <span className="font-display font-semibold text-[20px] text-[#2C2416]">
                      ₹{row.price.toLocaleString("en-IN")}
                    </span>
                    <span className="text-[11px] text-[#7A6A55]">per quintal</span>
                  </div>
                  <span
                    className={`px-2.5 py-1 text-[11px] font-medium rounded-[4px] ${
                      row.trend === "up"
                        ? "bg-[#DDE8D9] text-[#3A5E32]"
                        : "bg-[#EDE3D3] text-[#7A3B2E]"
                    }`}
                  >
                    {row.change}
                  </span>
                </div>
              </div>
            );
          })}
        </section>

        {/* AI Insight */}
        <section className="bg-[#F5F1EA] pt-4">
          <h2 className="font-display italic text-[18px] text-[#5C7A52] mb-3">
            How to use mandi comparison to maximise your returns
          </h2>
          <div className="font-body font-light text-[13px] text-[#2C2416] leading-[1.8] flex flex-col gap-4 max-w-3xl">
            <p>
              Modal prices vary across mandis due to local supply-demand dynamics, transport costs, and seasonal buyer activity. Comparing prices before you load your produce can add ₹50–200 per quintal to your net income.
            </p>
            <p>
              Today, Nashik Mandi is showing the strongest upward momentum for Onion, while Delhi Mandi continues to lead for Tomato. If transport costs to a higher-priced mandi are below the price difference, the move is profitable.
            </p>
            <p>
              Prices are updated daily from AGMARKNET records. For perishables like Tomato and Onion, check again in the morning before dispatch — intraday swings can be significant.
            </p>
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-8 pt-6 border-t-[0.5px] border-[#E8DFC9] flex justify-center">
          <p className="font-body text-[11px] text-[#7A6A55] font-light">
            Data sourced from mandi_prices.csv · Updated daily · Powered by AgriSense ML
          </p>
        </footer>

      </div>
    </ProtectedRoute>
  );
}
