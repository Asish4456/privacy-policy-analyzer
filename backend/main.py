from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_policy(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    print("FILE:", file)
    print("TEXT:", text)

    if file is not None:
        content = await file.read()
        return {
            "risk_level": "Medium",
            "risk_score": 6,
            "insights": [[0, "PDF successfully received"]]
        }

    if text is not None:
        return {
            "risk_level": "Low",
            "risk_score": 3,
            "insights": [[0, "Text successfully received"]]
        }

    return {"error": "No input received"}
