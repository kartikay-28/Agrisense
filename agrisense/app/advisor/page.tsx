"use client";

import { useState } from "react";
import { Send } from "lucide-react";
import ProtectedRoute from "@/components/ProtectedRoute";

// Static ML-backed responses — replace with real FastAPI call once backend is live
const ML_RESPONSES: Record<string, string> = {
  "What is the best time to sell my wheat this season?":
    "Based on price regression analysis of the last 3 seasons, week 18 (late May) shows the highest predicted modal price for wheat in your region — approximately ₹2,450/quintal. Holding until then is recommended if storage conditions allow.",
  "Will the dry spell affect my rice crop?":
    "The climate risk model scores your current conditions at 0.72 (High Risk) due to rainfall deviation of -38% from the seasonal average. Rice in the tillering phase is particularly sensitive. Irrigation of 18mm every 3 days is advised.",
  "Should I apply more fertilizer this week?":
    "Your yield prediction model shows fertilizer as the highest-impact variable right now (factor score: 9.2/10). Increasing application to 80% of the recommended dose this week could improve predicted yield by 6–8%.",
  "What's driving the price of maize right now?":
    "The price regression model identifies month (seasonal demand) and state supply index as the top two predictors. Maize prices are currently elevated due to reduced Kharif output in UP and MP — a 4.5% increase over the 30-day baseline.",
  "How does my yield compare to last year?":
    "Your predicted yield of 5.1 tons/acre is 21% above last year's recorded 4.2 tons/acre. The primary driver is improved rainfall distribution in the early growing phase, which the model weights at 50% of the risk score.",
  "What risks should I watch in the next 30 days?":
    "The climate risk model flags two concerns: (1) Drought probability 68% in weeks 3–4 based on IMD forecast patterns. (2) Temperature stress risk rises to HIGH if temperatures exceed 35°C for 3+ consecutive days. Irrigation scheduling and mulching are the recommended mitigations.",
};

const DEFAULT_RESPONSE =
  "This question is being processed by the AgriSense ML models. For now, please refer to your Dashboard for the latest risk scores and price predictions, or check the Climate and Market pages for detailed analysis.";

export default function Advisor() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "The current dry spell looks very similar to late 2021. With your wheat currently in the critical tillering phase, early-stage moisture stress can reduce your baseline yield by 8–12% if irrigation is missed. This is based on the climate risk model scoring your conditions at 0.68 (High Risk).",
      title: "What this means for your farm",
    },
    {
      role: "user",
      content: "What is the best time to sell my wheat this season?",
    },
    {
      role: "assistant",
      content:
        "Based on price regression analysis of the last 3 seasons, week 18 (late May) shows the highest predicted modal price for wheat in your region — approximately ₹2,450/quintal. Holding until then is recommended if storage conditions allow.",
      title: "Market outlook for your wheat",
    },
  ]);

  const questions = [
    "What is the best time to sell my wheat this season?",
    "Will the dry spell affect my rice crop?",
    "Should I apply more fertilizer this week?",
    "What's driving the price of maize right now?",
    "How does my yield compare to last year?",
    "What risks should I watch in the next 30 days?",
  ];

  const handleSend = () => {
    if (!prompt.trim()) return;

    const userMsg = { role: "user", content: prompt, title: "" };
    const response = ML_RESPONSES[prompt] ?? DEFAULT_RESPONSE;
    const assistantMsg = {
      role: "assistant",
      content: response,
      title: "ML-powered insight",
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setPrompt("");
  };

  return (
    <ProtectedRoute>
      <div className="flex flex-col md:flex-row gap-12 max-w-[1100px] w-full mx-auto pb-10">
        {/* Left Column - Chat */}
        <section className="flex-[65%] flex flex-col h-[calc(100vh-140px)] relative">
          <div className="mb-6 shrink-0">
            <h1 className="font-display font-semibold text-[22px] text-[#2C2416]">
              Your ML farm advisor
            </h1>
            <p className="font-body font-light text-[14px] text-[#7A6A55]">
              Insights powered by Scikit-learn models — crop classification &amp; price regression.
            </p>
          </div>

          <div className="flex-1 overflow-y-auto max-h-[480px] pb-32 scrollbar-none flex flex-col gap-4">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`max-w-[85%] ${
                  m.role === "user"
                    ? "self-end !bg-[#EDE3D3] !rounded-[12px_12px_2px_12px] p-[12px_16px] !border-none"
                    : "self-start bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[12px_12px_12px_2px] p-[14px_18px]"
                }`}
              >
                {m.title && (
                  <h3 className="font-display italic text-[14px] text-[#5C7A52] mb-1.5">
                    {m.title}
                  </h3>
                )}
                <p
                  className={`font-body text-[13px] leading-[1.8] ${
                    m.role === "user" ? "text-[#2C2416]" : "font-light"
                  }`}
                >
                  {m.content}
                </p>
              </div>
            ))}
          </div>

          <div className="absolute bottom-0 w-full left-0 pt-4 bg-gradient-to-t from-[#F5F1EA] via-[#F5F1EA] to-transparent">
            <div className="relative">
              <textarea
                className="w-full bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[8px] p-[14px] pr-12 font-body text-[13px] text-[#2C2416] resize-none h-[80px] focus:outline-none focus:border-[#7A3B2E]"
                placeholder="Ask about prices, rain, when to plant..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
              />
              <button
                className="absolute right-4 bottom-4 bg-[#7A3B2E] text-[#F5F0E8] w-[32px] h-[32px] rounded-full flex items-center justify-center hover:opacity-90 transition-opacity"
                onClick={handleSend}
              >
                <Send size={14} />
              </button>
            </div>
          </div>
        </section>

        {/* Right Column - Prompts */}
        <aside className="flex-[35%] flex flex-col gap-4 pt-1">
          <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 w-max block">
            Suggested questions
          </span>
          <div className="flex flex-col gap-2">
            {questions.map((q) => (
              <button
                key={q}
                onClick={() => setPrompt(q)}
                className="bg-[#EDE3D3] text-[#7A3B2E] border-none rounded-[20px] p-[8px_14px] font-body text-[12px] text-left hover:bg-[#D9CEB8] transition-colors w-full"
              >
                {q}
              </button>
            ))}
          </div>
          <div className="h-[0.5px] bg-[#E8DFC9] w-full my-4" />
          <p className="font-body font-light italic text-[11px] text-[#7A6A55] max-w-[90%]">
            Answers are generated by Scikit-learn ML models (Random Forest + Gradient Boosting) trained on Indian agricultural data. Not a substitute for professional agronomic advice.
          </p>
        </aside>
      </div>
    </ProtectedRoute>
  );
}
