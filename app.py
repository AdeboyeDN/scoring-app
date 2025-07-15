from fastapi import FastAPI, Request
from pydantic import BaseModel
import ray
from ray import serve
from scorer import Scorer

# Start Ray
ray.init(num_cpus=0.5)

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

# Wrap FastAPI app in a Ray Serve deployment
@serve.deployment(ray_actor_options={"num_cpus": 0.25})
@serve.ingress(app)
class ScoreService:
    pass  # Ray Serve just serves the FastAPI app

# Deploy
serve.run(ScoreService.bind(), name="score_app", route_prefix="/", blocking=True)
