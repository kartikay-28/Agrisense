import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] max-w-[1100px] mx-auto text-center px-4 gap-16">
      {/* Hero Section */}
      <section className="flex flex-col items-center gap-6 mt-12">
        <h1 className="font-display font-semibold text-[36px] md:text-[48px] text-[#2C2416] leading-tight max-w-[800px]">
          Smarter farming starts with <br /> better decisions
        </h1>
        <p className="font-body text-[16px] md:text-[18px] text-[#7A6A55] max-w-[600px] leading-relaxed">
          Predict demand, prices, and climate risks using AI. AgriSense is your
          trusted intelligence platform designed specifically for the modern
          farmer.
        </p>
        <div className="flex gap-4 mt-4">
          <Link
            href="/signin"
            className="bg-[#7A3B2E] text-[#F5F0E8] rounded-[24px] px-[28px] py-[12px] font-medium text-[14px] hover:opacity-90 transition-opacity"
          >
            Get Started
          </Link>
          <Link
            href="/signin"
            className="border border-[#7A3B2E] text-[#7A3B2E] rounded-[24px] px-[28px] py-[12px] font-medium text-[14px] hover:bg-[#EDE3D3] transition-colors"
          >
            Sign In
          </Link>
        </div>
      </section>

      {/* Features - 3 Columns */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-8">
        {[
          {
            title: "Demand Prediction",
            desc: "Accurately forecast market demand for your crops and plan your selling window.",
          },
          {
            title: "Price Forecasting",
            desc: "Track commodity prices and get notified before significant drops or spikes.",
          },
          {
            title: "Climate Risk Alerts",
            desc: "Anticipate droughts, floods, and frost with localized risk indicators.",
          },
        ].map((feature, idx) => (
          <div
            key={idx}
            className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[12px] p-[24px] flex flex-col gap-3 text-left"
          >
            <h3 className="font-display font-semibold text-[18px] text-[#2C2416]">
              {feature.title}
            </h3>
            <p className="font-body font-light text-[14px] text-[#7A6A55] leading-relaxed">
              {feature.desc}
            </p>
          </div>
        ))}
      </section>

      {/* How It Works */}
      <section className="flex flex-col items-center gap-8 w-full mt-10">
        <h2 className="font-display italic text-[24px] text-[#5C7A52]">
          How it works
        </h2>
        <div className="flex flex-col md:flex-row gap-6 w-full justify-center">
          {[
            { step: "Step 1", text: "Input farm data" },
            { step: "Step 2", text: "AI analyzes trends" },
            { step: "Step 3", text: "Get simple insights" },
          ].map((item, idx) => (
            <div
              key={idx}
              className="flex-1 flex flex-col items-center gap-2 p-4 bg-[#F5F1EA] rounded-[10px]"
            >
              <span className="font-medium text-[11px] uppercase tracking-[0.1em] text-[#7A3B2E]">
                {item.step}
              </span>
              <p className="font-body text-[14px] text-[#2C2416] font-medium">
                {item.text}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Minimal Footer */}
      <footer className="mt-16 border-t-[0.5px] border-[#E8DFC9] pt-6 w-full text-center">
        <p className="font-body text-[12px] text-[#7A6A55]">
          Powered by AgriSense
        </p>
      </footer>
    </div>
  );
}
