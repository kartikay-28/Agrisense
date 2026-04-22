"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

export type LanguageCode = "en" | "hi" | "mr" | "ta";

type TranslationKey =
  | "nav.home"
  | "nav.signIn"
  | "nav.dashboard"
  | "nav.market"
  | "nav.mandi"
  | "nav.climate"
  | "nav.yield"
  | "nav.advisor"
  | "nav.profile"
  | "nav.logOut"
  | "nav.signOut"
  | "nav.signOutConfirm"
  | "nav.cancel"
  | "nav.confirm"
  | "nav.language"
  | "landing.heroTitle"
  | "landing.heroSubtitle"
  | "landing.getStarted"
  | "landing.featureDemandTitle"
  | "landing.featureDemandDesc"
  | "landing.featurePriceTitle"
  | "landing.featurePriceDesc"
  | "landing.featureClimateTitle"
  | "landing.featureClimateDesc"
  | "landing.howItWorks"
  | "landing.step1"
  | "landing.step1Text"
  | "landing.step2"
  | "landing.step2Text"
  | "landing.step3"
  | "landing.step3Text"
  | "landing.footer"
  | "signin.welcome"
  | "signin.subtitle"
  | "signin.email"
  | "signin.password"
  | "signin.submit"
  | "signin.or"
  | "signin.google";

type TranslationMap = Record<TranslationKey, string>;

const translations: Record<LanguageCode, TranslationMap> = {
  en: {
    "nav.home": "Home",
    "nav.signIn": "Sign In",
    "nav.dashboard": "Dashboard",
    "nav.market": "Market",
    "nav.mandi": "Mandi",
    "nav.climate": "Climate",
    "nav.yield": "Yield",
    "nav.advisor": "Advisor",
    "nav.profile": "Profile",
    "nav.logOut": "Log Out",
    "nav.signOut": "Sign out",
    "nav.signOutConfirm": "Are you sure you want to sign out of AgriSense?",
    "nav.cancel": "Cancel",
    "nav.confirm": "Confirm",
    "nav.language": "Language",
    "landing.heroTitle": "Smarter farming starts with better decisions",
    "landing.heroSubtitle": "Predict demand, prices, and climate risks using AI. AgriSense is your trusted intelligence platform designed specifically for the modern farmer.",
    "landing.getStarted": "Get Started",
    "landing.featureDemandTitle": "Demand Prediction",
    "landing.featureDemandDesc": "Accurately forecast market demand for your crops and plan your selling window.",
    "landing.featurePriceTitle": "Price Forecasting",
    "landing.featurePriceDesc": "Track commodity prices and get notified before significant drops or spikes.",
    "landing.featureClimateTitle": "Climate Risk Alerts",
    "landing.featureClimateDesc": "Anticipate droughts, floods, and frost with localized risk indicators.",
    "landing.howItWorks": "How it works",
    "landing.step1": "Step 1",
    "landing.step1Text": "Input farm data",
    "landing.step2": "Step 2",
    "landing.step2Text": "AI analyzes trends",
    "landing.step3": "Step 3",
    "landing.step3Text": "Get simple insights",
    "landing.footer": "Powered by AgriSense",
    "signin.welcome": "Welcome back",
    "signin.subtitle": "Sign in to access your farm's intelligence.",
    "signin.email": "Email",
    "signin.password": "Password",
    "signin.submit": "Sign In",
    "signin.or": "Or",
    "signin.google": "Continue with Google",
  },
  hi: {
    "nav.home": "होम",
    "nav.signIn": "साइन इन",
    "nav.dashboard": "डैशबोर्ड",
    "nav.market": "मार्केट",
    "nav.mandi": "मंडी",
    "nav.climate": "जलवायु",
    "nav.yield": "उपज",
    "nav.advisor": "सलाहकार",
    "nav.profile": "प्रोफाइल",
    "nav.logOut": "लॉग आउट",
    "nav.signOut": "साइन आउट",
    "nav.signOutConfirm": "क्या आप वाकई AgriSense से साइन आउट करना चाहते हैं?",
    "nav.cancel": "रद्द करें",
    "nav.confirm": "पुष्टि करें",
    "nav.language": "भाषा",
    "landing.heroTitle": "बेहतर फैसलों से शुरू होती है स्मार्ट खेती",
    "landing.heroSubtitle": "AI की मदद से मांग, कीमत और जलवायु जोखिम का अनुमान लगाएं। AgriSense आधुनिक किसान के लिए बनाया गया भरोसेमंद प्लेटफॉर्म है।",
    "landing.getStarted": "शुरू करें",
    "landing.featureDemandTitle": "मांग का अनुमान",
    "landing.featureDemandDesc": "अपनी फसल की बाजार मांग का सही अनुमान लगाएं और सही समय पर बिक्री की योजना बनाएं।",
    "landing.featurePriceTitle": "कीमत पूर्वानुमान",
    "landing.featurePriceDesc": "कमोडिटी कीमतों पर नजर रखें और बड़े उतार-चढ़ाव से पहले अलर्ट पाएं।",
    "landing.featureClimateTitle": "जलवायु जोखिम अलर्ट",
    "landing.featureClimateDesc": "स्थानीय जोखिम संकेतकों के साथ सूखा, बाढ़ और पाला पहले से जानें।",
    "landing.howItWorks": "यह कैसे काम करता है",
    "landing.step1": "चरण 1",
    "landing.step1Text": "खेत का डेटा दर्ज करें",
    "landing.step2": "चरण 2",
    "landing.step2Text": "AI रुझानों का विश्लेषण करता है",
    "landing.step3": "चरण 3",
    "landing.step3Text": "सरल सुझाव प्राप्त करें",
    "landing.footer": "AgriSense द्वारा संचालित",
    "signin.welcome": "वापसी पर स्वागत है",
    "signin.subtitle": "अपने खेत की जानकारी पाने के लिए साइन इन करें।",
    "signin.email": "ईमेल",
    "signin.password": "पासवर्ड",
    "signin.submit": "साइन इन",
    "signin.or": "या",
    "signin.google": "Google से जारी रखें",
  },
  mr: {
    "nav.home": "मुख्यपृष्ठ",
    "nav.signIn": "साइन इन",
    "nav.dashboard": "डॅशबोर्ड",
    "nav.market": "बाजार",
    "nav.mandi": "मंडी",
    "nav.climate": "हवामान",
    "nav.yield": "उत्पन्न",
    "nav.advisor": "सल्लागार",
    "nav.profile": "प्रोफाइल",
    "nav.logOut": "लॉग आउट",
    "nav.signOut": "साइन आउट",
    "nav.signOutConfirm": "तुम्हाला AgriSense मधून साइन आउट करायचे आहे का?",
    "nav.cancel": "रद्द करा",
    "nav.confirm": "पुष्टी करा",
    "nav.language": "भाषा",
    "landing.heroTitle": "चांगले निर्णय म्हणजे स्मार्ट शेतीची सुरुवात",
    "landing.heroSubtitle": "AI वापरून मागणी, किंमत आणि हवामान जोखीम यांचे भाकीत करा. AgriSense हा आधुनिक शेतकऱ्यासाठी तयार केलेला विश्वासार्ह प्लॅटफॉर्म आहे.",
    "landing.getStarted": "सुरुवात करा",
    "landing.featureDemandTitle": "मागणीचा अंदाज",
    "landing.featureDemandDesc": "तुमच्या पिकांची बाजारातील मागणी अचूक ओळखा आणि विक्रीची योग्य वेळ ठरवा.",
    "landing.featurePriceTitle": "किंमत अंदाज",
    "landing.featurePriceDesc": "बाजारभावावर लक्ष ठेवा आणि मोठ्या चढउतारांपूर्वी सूचना मिळवा.",
    "landing.featureClimateTitle": "हवामान जोखीम सूचना",
    "landing.featureClimateDesc": "स्थानिक निर्देशकांद्वारे दुष्काळ, पूर आणि थंडीचा अंदाज आधी घ्या.",
    "landing.howItWorks": "हे कसे काम करते",
    "landing.step1": "टप्पा 1",
    "landing.step1Text": "शेताची माहिती भरा",
    "landing.step2": "टप्पा 2",
    "landing.step2Text": "AI ट्रेंडचे विश्लेषण करते",
    "landing.step3": "टप्पा 3",
    "landing.step3Text": "सोपे सल्ले मिळवा",
    "landing.footer": "AgriSense द्वारे समर्थित",
    "signin.welcome": "पुन्हा स्वागत आहे",
    "signin.subtitle": "तुमच्या शेताची माहिती पाहण्यासाठी साइन इन करा.",
    "signin.email": "ईमेल",
    "signin.password": "पासवर्ड",
    "signin.submit": "साइन इन",
    "signin.or": "किंवा",
    "signin.google": "Google सह सुरू ठेवा",
  },
  ta: {
    "nav.home": "முகப்பு",
    "nav.signIn": "உள்நுழை",
    "nav.dashboard": "டாஷ்போர்டு",
    "nav.market": "சந்தை",
    "nav.mandi": "மண்டி",
    "nav.climate": "காலநிலை",
    "nav.yield": "விளைச்சல்",
    "nav.advisor": "ஆலோசகர்",
    "nav.profile": "சுயவிவரம்",
    "nav.logOut": "வெளியேறு",
    "nav.signOut": "வெளியேறுதல்",
    "nav.signOutConfirm": "AgriSense இலிருந்து வெளியேற விரும்புகிறீர்களா?",
    "nav.cancel": "ரத்து",
    "nav.confirm": "உறுதி",
    "nav.language": "மொழி",
    "landing.heroTitle": "சிறந்த முடிவுகள் தான் புத்திசாலி வேளாண்மையின் தொடக்கம்",
    "landing.heroSubtitle": "AI மூலம் தேவை, விலை, மற்றும் காலநிலை ஆபத்துகளை கணிக்கவும். AgriSense நவீன விவசாயிக்காக உருவாக்கப்பட்ட நம்பகமான தளம்.",
    "landing.getStarted": "தொடங்குங்கள்",
    "landing.featureDemandTitle": "தேவை கணிப்பு",
    "landing.featureDemandDesc": "உங்கள் பயிர்களுக்கு சந்தை தேவை என்ன என்பதை துல்லியமாக கணித்து விற்பனை நேரத்தை திட்டமிடுங்கள்.",
    "landing.featurePriceTitle": "விலை கணிப்பு",
    "landing.featurePriceDesc": "சந்தை விலைகளை கண்காணித்து பெரிய ஏற்ற இறக்கங்களுக்கு முன் அறிவிப்புகளை பெறுங்கள்.",
    "landing.featureClimateTitle": "காலநிலை ஆபத்து எச்சரிக்கை",
    "landing.featureClimateDesc": "உள்ளூர் ஆபத்து குறிப்புகளுடன் வறட்சி, வெள்ளம், பனிப்பொழிவு போன்றவற்றை முன்கூட்டியே அறியுங்கள்.",
    "landing.howItWorks": "இது எப்படி செயல்படுகிறது",
    "landing.step1": "படி 1",
    "landing.step1Text": "பண்ணை தகவலை உள்ளிடுங்கள்",
    "landing.step2": "படி 2",
    "landing.step2Text": "AI போக்குகளை ஆய்வு செய்கிறது",
    "landing.step3": "படி 3",
    "landing.step3Text": "எளிய அறிவுரைகள் பெறுங்கள்",
    "landing.footer": "AgriSense மூலம் இயக்கப்படுகிறது",
    "signin.welcome": "மீண்டும் வரவேற்கிறோம்",
    "signin.subtitle": "உங்கள் பண்ணை நுண்ணறிவை அணுக உள்நுழையவும்.",
    "signin.email": "மின்னஞ்சல்",
    "signin.password": "கடவுச்சொல்",
    "signin.submit": "உள்நுழை",
    "signin.or": "அல்லது",
    "signin.google": "Google மூலம் தொடரவும்",
  },
};

const languageOptions: { code: LanguageCode; label: string }[] = [
  { code: "en", label: "English" },
  { code: "hi", label: "Hindi" },
  { code: "mr", label: "Marathi" },
  { code: "ta", label: "Tamil" },
];

type LanguageContextType = {
  language: LanguageCode;
  setLanguage: (language: LanguageCode) => void;
  t: (key: TranslationKey) => string;
  options: { code: LanguageCode; label: string }[];
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<LanguageCode>("en");

  useEffect(() => {
    const storedLanguage = localStorage.getItem("agrisense_language") as LanguageCode | null;
    if (storedLanguage && translations[storedLanguage]) {
      setLanguage(storedLanguage);
    }
  }, []);

  const updateLanguage = (newLanguage: LanguageCode) => {
    setLanguage(newLanguage);
    localStorage.setItem("agrisense_language", newLanguage);
  };

  const t = useMemo(
    () => (key: TranslationKey) => translations[language][key] || translations.en[key],
    [language]
  );

  const value: LanguageContextType = {
    language,
    setLanguage: updateLanguage,
    t,
    options: languageOptions,
  };

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within LanguageProvider");
  }
  return context;
}
