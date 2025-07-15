from fastapi import FastAPI, Request
from pydantic import BaseModel
import ray
from ray import serve
from scorer import Scorer

# Start Ray
ray.init()

# Start Ray Serve with public host
serve.start(detached=True, http_options={"host": "0.0.0.0", "port": 8000})

# Input schema
class ScoreRequest(BaseModel):
    features: dict

# FastAPI app
app = FastAPI()

@app.get("/")  # Optional health check
async def root():
    return {"status": "ok"}

# Ray Serve deployment wrapping FastAPI app
@serve.deployment(ray_actor_options={"num_cpus": 0})
@serve.ingress(app)
class ScoreService:
    def __init__(self):
        self.scorer = Scorer()

    @app.post("/score")
    async def score_endpoint(self, request: Request):
        body = await request.json()
        features = body["features"]
        score = self.scorer.score(features)
        return {"score": score}

# Deploy the app
serve.run(ScoreService.bind(), name="score_app", route_prefix="/", blocking=True)
