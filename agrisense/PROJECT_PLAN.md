# AgriSense: AI-Powered Agricultural Decision Support Platform
**Project Plan & MVP Definition**  
**Date:** April 8, 2026

## 1. Problem Statement
Farmers—particularly smallholders in regions like Himachal Pradesh—face unpredictable market fluctuations, volatile crop prices, and increasing climate risks such as erratic rainfall and temperature extremes. Relying on traditional guesswork often leads to significant crop and income losses. There is a critical need for an accessible platform that translates complex agricultural, weather, and market data into actionable, easy-to-understand insights.

## 2. Objective
To build a streamlined, user-friendly web dashboard that leverages historical and real-time data to predict crop demand, market prices, and climate risks. By combining Machine Learning models with an LLM-powered AI Advisor, AgriSense aims to deliver simple, natural-language recommendations that empower farmers to make profitable, data-backed decisions.

## 3. Target Users
*   Small and medium-scale farmers in India.
*   Agricultural cooperatives.
*   Government extension officers and farming consultants.

## 4. Data Sources (MVP)
*   **Production:** Historical crop yield data (Kaggle Indian agriculture datasets, data.gov.in).
*   **Climate:** Weather data and IMD rainfall/temperature records.
*   **Market:** AGMARKNET wholesale price datasets.
*   *Note for MVP:* Initial models will utilize publicly available CSV files and synthetic/mock data processed using Python, Pandas, and NumPy, with real API integration planned for post-MVP.

## 5. Technology Stack
*   **Backend & Data Processing:** Python, Pandas, NumPy, FastAPI.
*   **Machine Learning:** Prophet/LSTM (time-series forecasting), Random Forest/XGBoost (regression for demand/yield), Classification models (climate risk levels).
*   **AI Layer:** LLM integration (OpenAI, Grok, or local models) for natural language advice.
*   **Frontend:** Next.js, Tailwind CSS, Recharts.
*   **Deployment:** Vercel (Frontend) and Render (Backend).

## 6. MVP Scope
The MVP will focus on a clutter-free, highly focused user experience demonstrating core AI/ML capabilities:
*   **Authentication:** Public landing page and simple, secure sign-in.
*   **Protected Dashboard:** An organized summary view featuring key metrics—recommended crops, expected prices, and risk alerts.
*   **Core Modules:**
    *   *Market & Demand Insights:* Visualized demand trends and ML-backed trajectory predictions.
    *   *Price Predictions:* Forecasting graphs indicating the optimal time to sell.
    *   *Climate Risk:* 10-day hazard forecasts, clear risk badges, and actionable irrigation advice.
    *   *Yield Prediction:* Predicted harvest outcomes with interactive "what-if" scenario sliders.
*   **AI Advisor:** A conversational interface where users can ask localized questions and receive data-backed answers based on the ML outputs.
*   **UI/UX Design:** A clean, minimal interface utilizing a balanced green and terracotta color scheme (avoiding harsh bright blues), complete with a simple black/white (dark/light) mode toggle for optimal readability.

## 7. Success Metrics for MVP
*   **Usability:** Fully functional navigation, protected routes, and responsive mobile-first design.
*   **Technical Viability:** Successful execution of ML inferences (even on mock data) reflected in interactive charts and adjustable sliders.
*   **AI Performance:** The LLM Advisor consistently provides coherent, personalized, and data-backed advice.
*   **Clarity:** Users can interpret metrics efficiently without being overwhelmed by data clutter.

## 8. Future Enhancements (Post-MVP)
*   Integration of real-time weather and market APIs.
*   Personalized farm profiles with GPS location-based intelligence.
*   Advanced recommendation engine for seed and crop selection.
*   Dedicated native mobile application.
