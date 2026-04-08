import ProtectedRoute from "@/components/ProtectedRoute";

export default function Profile() {
  return (
    <ProtectedRoute>
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 w-full">
        <div className="bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] px-8 py-10 rounded-[12px] shadow-sm max-w-[500px] text-center flex flex-col gap-3">
          <h1 className="font-display font-semibold text-[24px] text-[#2C2416]">
            Your Profile
          </h1>
          <p className="font-body text-[14px] text-[#7A6A55] leading-relaxed">
            Your farm profile and notification settings have been securely configured. More granular preferences will be available in the upcoming release.
          </p>
        </div>
      </div>
    </ProtectedRoute>
  );
}
