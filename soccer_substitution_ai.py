# soccer_substitution_ai.py
# AI-Based Soccer Substitution Decision Assistant for HW 5 of CMSC 471

class Player:
    def __init__(self, name, position, fatigue, performance, yellow_card=False, injury_risk=0):
        self.name = name
        self.position = position
        self.fatigue = fatigue            # 0-100, A higher numnber means that they are more tired
        self.performance = performance    # 0-10, A higher number means they have better performance
        self.yellow_card = yellow_card    # True or False to tell if they have recieved a card or not
        self.injury_risk = injury_risk    # 0-100, A higher number means they have more injury risk


class Substitute:
    def __init__(self, name, position, attacking_rating, defensive_rating):
        self.name = name
        self.position = position
        self.attacking_rating = attacking_rating    # 0-10
        self.defensive_rating = defensive_rating    # 0-10


def calculate_substitution_score(player, substitute, minute, score_difference):
    score = 0
    reasons = []

    # Fatigue factor. This will allow the coaches to have a sense of what level of fatigue their players have.
    if player.fatigue >= 75:
        score += 30
        reasons.append(f"{player.name} has very high fatigue.")
    elif player.fatigue >= 60:
        score += 20
        reasons.append(f"{player.name} is becoming tired.")

    # Performance factor. This will allow the coaches to decide on a substitution based on the players performance in game. 
    if player.performance <= 5:
        score += 25
        reasons.append(f"{player.name} has a low performance rating.")
    elif player.performance <= 6.5:
        score += 10
        reasons.append(f"{player.name}'s performance is only average.")

    # Yellow card risk
    if player.yellow_card:
        score += 15
        reasons.append(f"{player.name} is on a yellow card, which increases risk or another foul leading to a red.")

    # Injury risk
    if player.injury_risk >= 70:
        score += 35
        reasons.append(f"{player.name} has a high injury risk.")
    elif player.injury_risk >= 40:
        score += 15
        reasons.append(f"{player.name} has some injury risk.")

    # Match minute factor
    if minute >= 70:
        score += 15
        reasons.append("The match is in the later stages.")
    elif minute >= 55:
        score += 10
        reasons.append("This is a reasonable time to consider a substitution.")

    # Tactical factor based on scoreline to tell coaches what the best decision is to make in the current stage of the game. 
    if score_difference < 0:
        score += substitute.attacking_rating * 2
        reasons.append("The team is losing, so attacking impact is more valuable.")
    elif score_difference > 0:
        score += substitute.defensive_rating * 2
        reasons.append("The team is winning, so defensive stability is more valuable.")
    else:
        score += substitute.attacking_rating + substitute.defensive_rating
        reasons.append("The match is tied, so a balanced impact is useful.")

    # Constraint: position compatibility. Some players might be comfortable playing in multiple positions but others may not. 
    if player.position != substitute.position:
        score -= 20
        reasons.append("The substitute plays a different position, so there is a tactical penalty.")

    return score, reasons


def recommend_substitution(players, substitutes, minute, score_difference, substitutions_remaining):
    if substitutions_remaining <= 0:
        return None, "No substitutions remaining."

    best_score = float("-inf")
    best_player_out = None
    best_player_in = None
    best_reasons = []

    for player in players:
        for substitute in substitutes:
            score, reasons = calculate_substitution_score(
                player,
                substitute,
                minute,
                score_difference
            )

            if score > best_score:
                best_score = score
                best_player_out = player
                best_player_in = substitute
                best_reasons = reasons

    return {
        "player_out": best_player_out,
        "player_in": best_player_in,
        "utility_score": best_score,
        "reasons": best_reasons
    }, None


def main():
    print("AI-Based Soccer Substitution Decision Assistant")
    print("------------------------------------------------")

    # Example players currently on the field
    players = [
        Player("Starting Winger", "Winger", fatigue=82, performance=5.5, yellow_card=False, injury_risk=30),
        Player("Central Midfielder", "Midfielder", fatigue=68, performance=6.0, yellow_card=True, injury_risk=20),
        Player("Left Back", "Defender", fatigue=55, performance=7.0, yellow_card=True, injury_risk=15),
        Player("Striker", "Forward", fatigue=60, performance=4.8, yellow_card=False, injury_risk=10)
    ]

    # Example substitutes available on the bench
    substitutes = [
        Substitute("Fresh Winger", "Winger", attacking_rating=8, defensive_rating=4),
        Substitute("Defensive Midfielder", "Midfielder", attacking_rating=4, defensive_rating=8),
        Substitute("Backup Defender", "Defender", attacking_rating=3, defensive_rating=7),
        Substitute("Backup Striker", "Forward", attacking_rating=8, defensive_rating=3)
    ]

    try:
        minute = int(input("Enter current match minute: "))
        score_difference = int(input("Enter score difference. Winning by 1 = 1, tied = 0, losing by 1 = -1: "))
        substitutions_remaining = int(input("Enter substitutions remaining: "))
    except ValueError:
        print("Invalid input. Please enter whole numbers.")
        return

    recommendation, error = recommend_substitution(
        players,
        substitutes,
        minute,
        score_difference,
        substitutions_remaining
    )

    if error:
        print(error)
        return

    print("\nRecommended Substitution")
    print("------------------------")
    print(f"Player OUT: {recommendation['player_out'].name} ({recommendation['player_out'].position})")
    print(f"Player IN: {recommendation['player_in'].name} ({recommendation['player_in'].position})")
    print(f"Utility Score: {recommendation['utility_score']}")

    print("\nReasons")
    print("-------")
    for reason in recommendation["reasons"]:
        print(f"- {reason}")

    print("\nFinal Explanation")
    print("-----------------")
    print(
        f"The AI recommends substituting {recommendation['player_out'].name} "
        f"for {recommendation['player_in'].name} because this option has the "
        f"highest utility score based on the current match situation."
    )


if __name__ == "__main__":
    main()