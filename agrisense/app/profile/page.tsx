"use client";

import { useState, useEffect } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/context/AuthContext";

const CROPS = ["Wheat", "Rice", "Maize", "Soybean", "Cotton", "Sugarcane", "Tomato", "Potato"];
const STATES = ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", "Rajasthan", "Madhya Pradesh"];

export default function Profile() {
  const { user, updateProfile } = useAuth();
  
  const [name, setName] = useState(user.name);
  const [location, setLocation] = useState(user.location);
  const [crop, setCrop] = useState(user.crop);
  const [acres, setAcres] = useState(user.acres.toString());
  const [season, setSeason] = useState(user.season);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setName(user.name);
    setLocation(user.location);
    setCrop(user.crop);
    setAcres(user.acres.toString());
    setSeason(user.season);
  }, [user]);

  const handleSave = () => {
    updateProfile({
      name,
      location,
      crop,
      acres: parseFloat(acres) || 0,
      season
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <ProtectedRoute>
      <div className="flex flex-col gap-10 max-w-[680px] w-full mx-auto pb-12">
        {/* Header */}
        <section className="flex flex-col gap-1">
          <span className="uppercase tracking-[0.14em] text-[#5C7A52] text-[10px] font-medium border-b-[0.5px] border-[#C9A97A] pb-1.5 mb-1.5 w-max">
            Farm profile
          </span>
          <h1 className="font-display font-semibold text-[28px] text-[#2C2416]">
            Your Profile
          </h1>
          <p className="font-body font-light text-[14px] text-[#7A6A55]">
            Keep your farm details up to date for accurate predictions and advice.
          </p>
        </section>

        {/* Avatar + Name Row */}
        <div className="flex items-center gap-5">
          <div className="w-[56px] h-[56px] rounded-full bg-[#DDE8D9] flex items-center justify-center text-[#3A5E32] font-display font-semibold text-[22px] select-none uppercase">
            {name.charAt(0)}
          </div>
          <div className="flex flex-col gap-0.5">
            <span className="font-display font-semibold text-[18px] text-[#2C2416]">{name}</span>
            <span className="font-body text-[12px] text-[#7A6A55]">{location} · {crop} farmer</span>
          </div>
        </div>

        {/* Form */}
        <div className="flex flex-col gap-6 bg-[#FDFAF4] border-[0.5px] border-[#D9CEB8] rounded-[12px] p-[28px]">
          <h2 className="font-display font-semibold text-[16px] text-[#2C2416]">Personal details</h2>

          <div className="flex flex-col gap-1.5">
            <label className="font-body text-[11px] uppercase tracking-[0.1em] text-[#7A6A55] font-medium">Full name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="h-[40px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-[14px] font-body text-[13px] text-[#2C2416] focus:outline-none focus:border-[#7A3B2E]"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="font-body text-[11px] uppercase tracking-[0.1em] text-[#7A6A55] font-medium">State / Location</label>
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="h-[40px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-[14px] font-body text-[13px] text-[#2C2416] focus:outline-none focus:border-[#7A3B2E] appearance-none"
              >
                {STATES.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-body text-[11px] uppercase tracking-[0.1em] text-[#7A6A55] font-medium">Primary crop</label>
              <select
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                className="h-[40px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-[14px] font-body text-[13px] text-[#2C2416] focus:outline-none focus:border-[#7A3B2E] appearance-none"
              >
                {CROPS.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-body text-[11px] uppercase tracking-[0.1em] text-[#7A6A55] font-medium">Total farm area (acres)</label>
              <input
                type="number"
                value={acres}
                onChange={(e) => setAcres(e.target.value)}
                min="0"
                step="0.1"
                className="h-[40px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-[14px] font-body text-[13px] text-[#2C2416] focus:outline-none focus:border-[#7A3B2E]"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-body text-[11px] uppercase tracking-[0.1em] text-[#7A6A55] font-medium">Current season</label>
              <select
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                className="h-[40px] bg-[#F5F1EA] border-[0.5px] border-[#D9CEB8] rounded-[8px] px-[14px] font-body text-[13px] text-[#2C2416] focus:outline-none focus:border-[#7A3B2E] appearance-none"
              >
                <option value="Rabi">Rabi</option>
                <option value="Kharif">Kharif</option>
                <option value="Zaid">Zaid</option>
              </select>
            </div>
          </div>
        </div>

        {/* Farm Summary Card */}
        <div className="bg-[#F5F1EA] rounded-[12px] p-[24px] flex flex-col gap-3">
          <h2 className="font-display font-semibold text-[16px] text-[#2C2416]">Farm summary</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Crop", value: crop },
              { label: "Area", value: `${acres} ac` },
              { label: "Season", value: season },
              { label: "Region", value: location },
            ].map((item) => (
              <div key={item.label} className="flex flex-col gap-1">
                <span className="font-body text-[10px] uppercase tracking-[0.1em] text-[#7A6A55] font-medium">{item.label}</span>
                <span className="font-display font-semibold text-[16px] text-[#2C2416]">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleSave}
            className="bg-[#7A3B2E] text-[#F5F0E8] rounded-[24px] px-[28px] py-[11px] font-medium text-[14px] hover:opacity-90 transition-opacity"
          >
            Save changes
          </button>
          {saved && (
            <span className="font-body text-[13px] text-[#5C7A52] font-medium">
              Profile saved
            </span>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
