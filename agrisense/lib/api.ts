/**
 * Central API Client for AgriSense Platform
 * Communicates with FastAPI backend running on localhost:8000
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Helper to handle fetch responses and throw structured errors
 */
async function fetchWithHandler(endpoint: string, options: RequestInit = {}) {
  try {
    const defaultHeaders: HeadersInit = {
      "Content-Type": "application/json",
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API request failed with status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error);
    throw error;
  }
}

/**
 * Fetch market data for a specific crop and optionally state.
 */
export async function getMarketData(crop: string, state?: string) {
  const params = new URLSearchParams({ crop });
  if (state) params.append("state", state);
  return fetchWithHandler(`/api/market-data?${params.toString()}`);
}

/**
 * Predict crop yield using the ML model.
 */
export async function predictYield(params: {
  crop: string;
  rainfall_mm: number;
  fertilizer_pct: number;
  season: string;
  field_acres?: number;
}) {
  return fetchWithHandler("/api/yield-predict", {
    method: "POST",
    body: JSON.stringify(params),
  });
}

/**
 * Fetch climate risk evaluation for a location based on a crop.
 */
export async function getClimateRisk(lat?: number, lon?: number, crop?: string) {
  const params = new URLSearchParams();
  if (lat !== undefined) params.append("lat", lat.toString());
  if (lon !== undefined) params.append("lon", lon.toString());
  if (crop) params.append("crop", crop);
  
  const queryString = params.toString();
  const endpoint = `/api/climate-risk${queryString ? `?${queryString}` : ""}`;
  
  return fetchWithHandler(endpoint);
}

/**
 * Request actionable insights from the LLM based on farm/market data.
 */
export async function getLLMInsight(data: object) {
  return fetchWithHandler("/api/llm-insight", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Send a chat message to the AI Advisor.
 */
export async function sendChatMessage(history: any[], message: string) {
  return fetchWithHandler("/api/chat", { 
    method: "POST",
    body: JSON.stringify({ history, message }),
  });
}
