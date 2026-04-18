"use client";

import { useState, useRef, useEffect } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { sendChatMessage } from "@/lib/api";
import { Send, Bot, User, Sparkles, AlertCircle } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function AIAdvisor() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello Rajan. I'm your AgriSense AI Advisor. How can I assist you with your farm operations today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const suggestedPrompts = [
    "Should I sell my stored wheat this week?",
    "What crop is best for Rabi season in Punjab?",
    "How does the current dry spell affect soil moisture?",
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (message: string) => {
    if (!message.trim()) return;

    // Append user message immediately
    const newMessages: Message[] = [...messages, { role: "user", content: message }];
    setMessages(newMessages);
    setInput("");
    setIsTyping(true);
    setError(null);

    try {
      // Pass the current message history to context to backend
      const response = await sendChatMessage(newMessages, message);
      // Wait for the backend LLM engine response
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response?.reply || response?.response || "I am currently analyzing those parameters. Please try again in an hour." },
      ]);
    } catch (err) {
      console.error(err);
      setError("AI Engine is temporarily unavailable.");
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex flex-col h-[calc(100vh-140px)] max-w-[800px] w-full mx-auto relative">
        <section className="flex flex-col gap-1 border-b-[0.5px] border-[#D9CEB8] pb-4 flex-shrink-0">
          <h1 className="font-display font-semibold text-[24px] text-[#2C2416] flex items-center gap-2">
            <Sparkles size={20} className="text-[#5C7A52]" /> Ask the AI Advisor
          </h1>
          <p className="font-body text-[#7A6A55] text-[13px]">
            Powered by contextual farm insights and real-time market data.
          </p>
        </section>

        {/* Chat History Area */}
        <div className="flex-1 overflow-y-auto py-6 flex flex-col gap-6 scrollbar-hide">
          
          {error && (
            <div className="bg-[#FDFAF4] border-[0.5px] border-[#7A3B2E] rounded-lg p-3 text-[#7A3B2E] text-[12px] flex items-center justify-center gap-2">
              <AlertCircle size={14}/> {error}
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex gap-3 w-full ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {/* Bot Avatar (Left) */}
              {msg.role === "assistant" && (
                <div className="w-[36px] h-[36px] bg-[#5C7A52] rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot size={18} className="text-white" />
                </div>
              )}

              {/* Chat Bubble */}
              <div
                className={`max-w-[75%] p-4 rounded-[16px] font-body text-[14px] leading-relaxed shadow-sm block break-words ${
                  msg.role === "user"
                    ? "bg-[#2C2416] text-white rounded-tr-[4px]"
                    : "bg-[#F5F1EA] border border-[#D9CEB8] text-[#2C2416] rounded-tl-[4px]"
                }`}
              >
                {msg.content}
              </div>

              {/* User Avatar (Right) */}
              {msg.role === "user" && (
                <div className="w-[36px] h-[36px] bg-[#C9A97A] rounded-full flex items-center justify-center flex-shrink-0">
                  <User size={18} className="text-[#2C2416]" />
                </div>
              )}
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex gap-3 w-full justify-start items-center">
              <div className="w-[36px] h-[36px] bg-[#5C7A52] rounded-full flex items-center justify-center flex-shrink-0">
                <Bot size={18} className="text-white" />
              </div>
              <div className="bg-[#F5F1EA] border border-[#D9CEB8] rounded-[16px] rounded-tl-[4px] p-4 flex gap-1 h-[42px] items-center justify-center shadow-sm">
                <div className="w-1.5 h-1.5 bg-[#A8C4A1] rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-1.5 h-1.5 bg-[#A8C4A1] rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-1.5 h-1.5 bg-[#A8C4A1] rounded-full animate-bounce"></div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} className="h-[2px]" />
        </div>

        {/* Input Area (Pinned to bottom of container) */}
        <div className="flex flex-col gap-3 bg-white/90 backdrop-blur pt-2 flex-shrink-0 border-t-[0.5px] border-transparent">
          {/* Suggested Prompts */}
          <div className="flex flex-wrap gap-2 justify-center lg:justify-start overflow-x-auto pb-2 scrollbar-hide">
            {suggestedPrompts.map((prompt) => (
              <button
                key={prompt}
                onClick={() => handleSend(prompt)}
                disabled={isTyping}
                className="whitespace-nowrap px-4 py-[6px] rounded-[24px] border border-[#D9CEB8] bg-[#F5F1EA] text-[#7A6A55] text-[12px] font-medium hover:bg-[#DDE8D9] hover:text-[#5C7A52] hover:border-[#5C7A52] transition-colors disabled:opacity-50"
              >
                {prompt}
              </button>
            ))}
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend(input);
            }}
            className="flex gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isTyping}
              placeholder="Ask about market timing, climate risks, or yield confidence..."
              className="flex-1 bg-[#F5F1EA] border border-[#D9CEB8] rounded-[24px] px-6 py-4 outline-none focus:ring-1 focus:ring-[#5C7A52] text-[#2C2416] text-[14px] disabled:opacity-50 transition-all font-body"
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="bg-[#5C7A52] text-white w-[54px] h-[54px] rounded-full flex items-center justify-center hover:bg-[#3A5E32] disabled:opacity-50 disabled:bg-[#A8C4A1] transition-colors flex-shrink-0"
            >
              <Send size={18} className="translate-x-[1px]" />
            </button>
          </form>
          <div className="text-center mt-2 pb-2">
             <span className="text-[10px] text-[#A69B8D] uppercase tracking-widest font-medium">AgriSense ML responses may produce inaccurate information</span>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
