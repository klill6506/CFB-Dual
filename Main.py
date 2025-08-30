import argparse
import yaml
from model import HandicappingModel
from fetchers import fetch_game_data

def load_config(choice):
    filename = f"config_{choice}.yaml"
    with open(filename, "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["aggressive", "conservative", "both"], default="conservative")
    args = parser.parse_args()

    game_data = fetch_game_data()

    if args.model == "both":
        for choice in ["aggressive", "conservative"]:
            config = load_config(choice)
            model = HandicappingModel(config, label=choice)
            edge = model.calculate_edge(game_data)
            print(f"{choice.upper()} Model Edge: {edge:.2f}")
    else:
        config = load_config(args.model)
        model = HandicappingModel(config, label=args.model)
        edge = model.calculate_edge(game_data)
        print(f"{args.model.upper()} Model Edge: {edge:.2f}")
