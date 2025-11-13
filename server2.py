from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sarvamai import SarvamAI

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SarvamAI client
client = SarvamAI(api_subscription_key="YOUR_VALID_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    # ✅ Build dynamic prompt based on user input
    refined_prompt = (
        f"List only the top 4 books for learning {user_message}. "
        f"Give only book names and authors, in a simple numbered list. No explanations."
    )

    print("📩 Received from frontend:", user_message)
    print("🧠 Sending prompt:", refined_prompt)

    response = client.chat.completions(
        messages=[{"role": "user", "content": refined_prompt}],
        temperature=0.3,
        top_p=1,
        max_tokens=200,
    )

    ai_reply = response.choices[0].message.content
    return {"reply": ai_reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
