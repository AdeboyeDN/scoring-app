from fastapi import FastAPI, Request
from pydantic import BaseModel
import ray
from ray import serve
from scorer import Scorer

# Start Ray without fractional CPUs
ray.init()

# Input schema
class ScoreRequest(BaseModel):
    features: dict

# FastAPI app
app = FastAPI()

@app.post("/score")
async def score_endpoint(request: Request):
    body = await request.json()
    features = body["features"]
    score = Scorer().score(features)
    return {"score": score}

# Ray Serve deployment wrapping FastAPI app
@serve.deployment(ray_actor_options={"num_cpus": 0.25})
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

# Run Serve application
serve.run(ScoreService.bind(), name="score_app", route_prefix="/", blocking=True)
