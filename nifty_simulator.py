import uvicorn
from fastapi import FastAPI
import random

app = FastAPI()
s_val = 25000
val = random.randrange(s_val, (int(s_val*1.001)))

@app.get("/")
async def root():
    global s_val
    global val
    val = random.randrange(val, int(val*1.001))
    return f"Nifty price : {str(val)}"

if __name__ == "__main__":
    uvicorn.run(app)
