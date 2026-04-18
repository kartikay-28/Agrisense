import React from "react";
import { FolderOpen } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
  className?: string;
}

export default function EmptyState({
  title = "No Data Found",
  description = "There is currently no information available for this selection.",
  actionText,
  onAction,
  className = "",
}: EmptyStateProps) {
  return (
    <div
      className={`bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[16px] p-8 flex flex-col items-center flex-1 justify-center text-center gap-4 ${className}`}
    >
      <div className="w-[48px] h-[48px] bg-[#EDE3D3] rounded-full flex justify-center items-center">
        <FolderOpen size={24} className="text-[#C9A97A]" />
      </div>

      <div className="max-w-[300px]">
        <h3 className="font-display font-medium text-[#2C2416] text-[16px] mb-2">
          {title}
        </h3>
        <p className="font-body text-[#7A6A55] text-[13px] leading-relaxed">
          {description}
        </p>
      </div>

      {actionText && onAction && (
        <button
          onClick={onAction}
          className="mt-2 text-[#5C7A52] hover:text-[#3A5E32] font-semibold text-[13px] uppercase tracking-wide border-b-[0.5px] border-transparent hover:border-[#5C7A52] transition-colors pb-0.5"
        >
          {actionText}
        </button>
      )}
    </div>
  );
}