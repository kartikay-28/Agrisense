import React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorMessageProps {
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export default function ErrorMessage({
  message = "Data temporarily unavailable. We're having trouble retrieving the latest information for your farm.",
  onRetry,
  className = "",
}: ErrorMessageProps) {
  return (
    <div
      className={`bg-[#FDFAF4] border-l-[3px] border-[#7A3B2E] p-5 rounded-r-[8px] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-sm ${className}`}
    >
      <div className="flex items-center gap-3 text-[#7A3B2E]">
        <AlertCircle size={20} className="flex-shrink-0" />
        <p className="font-body text-[14px] font-medium leading-relaxed">
          {message}
        </p>
      </div>

      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 border-[0.5px] border-[#D9CEB8] text-[#5C7A52] hover:bg-[#F5F1EA] px-[16px] py-[8px] rounded-[24px] font-medium text-[13px] bg-white transition-colors flex-shrink-0"
        >
          <RefreshCw size={14} />
          Try Again
        </button>
      )}
    </div>
  );
}