# cfb_model.py
# College Football Spread Model (Power Ratings + Roster + Efficiency + Calibration)

# ------------------------
# INPUT SECTION
# ------------------------

# Example inputs (Florida vs USF, 2025)
teams = {
    "Florida": {
        "sp_rating": 19.2,            # SP+ preseason rating
        "returning_prod": 0.65,       # % returning production
        "portal_adj": 1.0,            # points adjustment for transfers (manual)
        "recruiting_adj": 0.5,        # points adjustment for roster talent
        "efficiency_off": 0.0,        # EPA/play adjustment (carryover or current season)
        "efficiency_def": 0.0,        # defensive EPA/play adjustment
    },
    "USF": {
        "sp_rating": 1.4,
        "returning_prod": 0.70,
        "portal_adj": 0.0,
        "recruiting_adj": -0.5,
        "efficiency_off": -1.0,       # downgrade vs SEC defense
        "efficiency_def": -1.5,       # downgrade vs SEC offense
    }
}

home_team = "Florida"
away_team = "USF"

home_field_adv = 2.5       # points
vegas_line = -17.5         # Florida -17.5 (market line)

# ------------------------
# CALCULATION SECTION
# ------------------------

def calculate_spread(home, away):
    # Base power rating differential
    base = home["sp_rating"] - away["sp_rating"]
    
    # Roster adjustments
    roster_adj = (
        home["portal_adj"] + home["recruiting_adj"]
        - away["portal_adj"] - away["recruiting_adj"]
    )
    
    # Efficiency adjustments
    efficiency_adj = (
        home["efficiency_off"] - away["efficiency_def"]
        + home["efficiency_def"] - away["efficiency_off"]
    )
    
    # Combine all adjustments
    spread = base + roster_adj + efficiency_adj
    return spread

# Model spread
model_spread = calculate_spread(teams[home_team], teams[away_team]) + home_field_adv

# Edge vs Vegas
edge = model_spread - abs(vegas_line)

# ------------------------
# OUTPUT SECTION
# ------------------------

print(f"{home_team} vs {away_team}")
print(f"Model Spread: {home_team} {model_spread:.1f}")
print(f"Vegas Line: {home_team} {vegas_line}")
print(f"Edge: {edge:.1f} points")

if abs(edge) < 3:
    print("Recommendation: PASS / Small lean")
elif abs(edge) < 7:
    print("Recommendation: MEDIUM play")
else:
    print("Recommendation: STRONG play")
