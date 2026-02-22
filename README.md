#   INSYTE - AI POWERED CUSTOMER SENTIMENT INTELLIGENCE
INSYTE is a v1-B2B SaaS platform that helps businesses understand what customers actually feel about their product by analyzing large volumes of reviews and generating clear, actionable business insights.
Upload a CSV of reviews, INSYTE does the rest.
It analyses the reviews, extracts key business factors, generates summaries, identifes risk and gives dashboards on which businesses can rely on.<br>
Live on : https://insyte-ai.netlify.app<br>
⚠️IMP NOTE: Used GEMINI API(free tier), CORE tool may not be accessible.

# ⚡KEY FEATURES
- AI powered sentiment detection.(positive/negative/neutral)
- Batch processing for thousands of reviews.
- Confidence level calibration.
- Factor extraction like:
    - Delivery/Logistics
    - Customer Support
    - UX/Usability
    - Pricing/Value
    - Perfomance
- Business reliable insights:
    - Risk level
    - Sentiment distribution
    - Mixed feedback ratio
- Top PROS and CONS section.

# 💡HOW IT WORKS
1. User uploads CSV of reviews.
2. Backend sends it to AI (an API call is initiated to GEMINI API).
3. Each review returns :(JSON FILE)<br>
    {<br>
     &ensp;sentiment : " ... ",<br>
     &ensp;confidence : " ... ",<br>
     &ensp;summary : " ... "<br>
   }<br>
4. Factors are robustly mapped.(factor parameters are hard coded)
5.  Insights are aggregated and displayed with beautification.

# 🗂️PROJECT STRUCTURE
```
INSYTE
│
├── backend/
│   ├── main.py                        # FastAPI entry point
│   │
│   ├── models/
│   │   ├── sentiment_schema.py        # Single review schema
│   │   ├── batch_schema.py            # Batch review + insights schema
│   │
│   ├── services/
│   │   ├── sentiment_service.py       # Single review AI processing
│   │   ├── batch_sentiment_service.py # Batch AI processing
│   │   ├── factor_mapper.py           # Extracts business factors
│   │   ├── aggregation_service.py     # Builds insights dashboard
│   │
│   ├── utils/
│   │   ├── json_validator.py          # Ensures AI output safety
│   │   ├── confidence_calibrator.py   # Adjusts confidence scores
│   │
│   ├── core/
│   │   ├── config.py                  # System configuration
│
├── frontend/
|   ├── assets
|   ├── public/    
│        ├── index.html                # Landing page UI
|        ├── app.html                  # Main UI (with Tailwind Styling)
│        ├── style.css                 # Root Styles
│        ├── script.js                 # Frontend logic + API calls 
│
├── requirements.txt
```
# 💻TECH STACK
## BACKEND
- Python
- fastAPI
- Google Gemini API
- Robust Schema validation
## FRONTEND
- HTML
- Tailwind CSS
- JS

# ⚙️RUN IT LOCALLY
1. Clone repo
```bash
git clone https://github.com/shriikriishna06/insyte.git
cd insyte
```
2. Install backend deps
```bash
pip install -r requirements.txt
```
3. Creation of .env
```
GEMINI_API_KEY=your_key_here
```
4. Start backend service
```bash
python -m uvicorn backend.main:app --reload
```
5. Go live on<br>
Make sure to set the right path for the assets and js to get served. (using python(fastAPI) to serve the front end is recommended)
```
insyte/frontend/landingpage.html
```
6. Using py to serve the frontend<br>
Following steps are already performed but are commented in  the main.py file.(to use just uncomment...)<br>
- Place this API endpoint in the beginning of the main.py file.
```python
frontend_dir = Path(__file__).resolve().parents[1] / "frontend" / "public"

@app.get("/")
def root():
    return FileResponse(frontend_dir / "landingpage.html")
```
- Place this at the end of main.py file.
```python
app.mount(
    "/",
    StaticFiles(directory=str(frontend_dir)),
    name="static"
)
```

# 🛡️RELIABILITY
- Strict JSON validation
- AI hallucination protection
- Confidence calibration system
- Graceful fallback handling
- Safe batching to avoid failures

# 📄CSV FORMAT
No headers required. Cleaning, parsing ->Insyte handles it all.
Sample format:
```
Product quality is amazing but delivery was late
Customer support helped me quickly
App crashes often
```
# ✅️STATUS
This project is currently:
- Working end to end
- SaaS ready architecture
- Business reliable insights
## 🎯FUTURE PLAN
- Integration of USER accounts.(firebase, OAUTH etc)
- Saved history on the server side using persistent db.(currently using browser local storage still persistent after browser reopen)
- Visual Insights
- Insight export (PDF)
- Dockerization (devops)
- Integrating Redis and Cloudflare for rate limiting and security concerns(DDOS)

# 👤NOTE BY THE AUTHOR
Built with ⚡ and obsession....







