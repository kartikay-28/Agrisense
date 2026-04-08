import ProtectedRoute from "@/components/ProtectedRoute";

export default function Market() {
  const latestDataAge = "15 minutes ago";
  const tabs = ["All crops", "Wheat", "Rice", "Maize", "Sugarcane"];

  return (
    <ProtectedRoute>
    <div className="flex flex-col gap-12 max-w-[1100px] w-full mx-auto">
      {/* Header Area */}
      <section className="flex flex-col items-start gap-1">
        <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5">
          Market intelligence
        </span>
        <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
          Crop prices & demand
        </h1>
        <p className="font-body font-light text-[14px] text-[#7A6A55]">
          Updated daily from commodity exchanges · Interpreted for your crops
        </p>
      </section>

      {/* Tabs */}
      <section className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {tabs.map((tab, idx) => (
          <button
            key={tab}
            className={`whitespace-nowrap rounded-[20px] px-4 py-1.5 text-[13px] font-medium transition-colors ${
              idx === 0
                ? "bg-[#7A3B2E] text-[#F5F0E8]"
                : "border-[0.5px] border-[#D9CEB8] text-[#7A6A55] hover:bg-[#F5F1EA]"
            }`}
          >
            {tab}
          </button>
        ))}
      </section>

      {/* Crop Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {[
          {
            name: "Wheat",
            price: "₹2,275",
            change: "+8.4%",
            trend: "up",
            demand: "High demand",
            window: "Best to sell: Next 2 weeks",
          },
          {
            name: "Rice",
            price: "₹3,150",
            change: "-3.1%",
            trend: "down",
            demand: "Moderate demand",
            window: "Hold — prices rising",
          },
          {
            name: "Maize",
            price: "₹2,050",
            change: "+4.5%",
            trend: "up",
            demand: "High demand",
            window: "Sell now — peak expected",
          },
        ].map((crop) => (
          <div
            key={crop.name}
            className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[12px] p-[20px_24px] flex flex-col gap-4"
          >
            <div className="flex justify-between items-center">
              <span className="font-medium text-[14px] text-[#2C2416] font-body">
                {crop.name}
              </span>
              <span className="font-medium text-[14px] text-[#2C2416] font-body">
                {crop.price}
              </span>
            </div>

            <div className="flex h-[32px] items-end gap-1 mb-2">
              {/* Simulate 30-day sparkline */}
              {Array.from({ length: 15 }).map((_, i) => (
                <div
                  key={i}
                  className={`flex-1 rounded-t-[1px] ${
                    crop.trend === "up" ? "bg-[#5C7A52]" : "bg-[#7A3B2E]"
                  }`}
                  style={{
                    height: `${Math.random() * 60 + 20}%`,
                    opacity: 0.8,
                  }}
                />
              ))}
            </div>

            <div className="flex flex-col gap-2">
              <span className="text-[12px] font-medium text-[#7A6A55]">
                {crop.demand}
              </span>
              <span className="text-[12px] font-medium text-[#7A3B2E]">
                {crop.window}
              </span>
            </div>
            <div className="mt-2 flex items-center justify-between pt-3 border-t-[0.5px] border-[#E8DFC9]">
              <span className="uppercase tracking-[0.14em] text-[10px] font-medium text-[#7A6A55]">
                30-day change
              </span>
              <span
                className={`px-2.5 py-1 text-[11px] font-medium rounded-[4px] ${
                  crop.trend === "up"
                    ? "bg-[#DDE8D9] text-[#3A5E32]"
                    : "bg-[#EDE3D3] text-[#7A3B2E]"
                }`}
              >
                {crop.change}
              </span>
            </div>
          </div>
        ))}
      </section>

      {/* AI Insight */}
      <section className="bg-[#F5F1EA] pt-4">
        <h2 className="font-display italic text-[18px] text-[#5C7A52] mb-3">
          What this season&apos;s prices mean for your income
        </h2>
        <div className="font-body font-light text-[13px] text-[#2C2416] leading-[1.8] flex flex-col gap-4 max-w-3xl">
          <p>
            The overall market conditions are showing strong inflationary pressure on staple grains, driven by lower-than-expected yields in central regions. This means baseline prices will likely remain elevated for at least another quarter.
          </p>
          <p>
            For your specific crop mix, your wheat is positioned perfectly to capture these premium rates. Since your harvest timing aligns with the projected peak of demand in week 18, you are likely to secure higher-than-average margins without forward contracting.
          </p>
          <p>
            The main risk factor to watch right now is sudden policy shifts regarding grain export tariffs. If restrictions are lifted, domestic prices could stabilize quickly. We will alert you if any policy discussions escalate.
          </p>
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
