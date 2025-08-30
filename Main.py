from fastapi import FastAPI, Query
import yaml
from model import HandicappingModel
from fetchers import fetch_game_data

# Initialize FastAPI app
app = FastAPI()

# Load config by model choice
def load_config(choice: str):
    filename = f"config_{choice}.yaml"
    with open(filename, "r") as f:
        return yaml.safe_load(f)

# Prediction endpoint
@app.get("/predict")
def predict(model: str = Query("conservative", enum=["aggressive", "conservative", "both"])):
    game_data = fetch_game_data()

    if model == "both":
        results = {}
        for choice in ["aggressive", "conservative"]:
            config = load_config(choice)
            m = HandicappingModel(config, label=choice)
            results[choice] = m.calculate_edge(game_data)
        return results
    else:
        config = load_config(model)
        m = HandicappingModel(config, label=model)
        edge = m.calculate_edge(game_data)
        return {model: edge}

# Local testing (not used by Render)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

