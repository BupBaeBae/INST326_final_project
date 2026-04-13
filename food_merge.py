import random

# Format: "ingredient": ("result", tier, point_value, purchase_cost)
RECIPES = {
    "apple": ("juice", 1, 1, 10),
    "strawberry": ("jam", 1, 1, 10),
    "banana": ("puree", 1, 1, 15),
    "blueberry": ("syrup", 1, 1, 15),
    "juice": ("smoothie", 2, 2, 0),
    "jam": ("tart", 2, 2, 0),
    "puree": ("pudding", 2, 2, 0),
    "syrup": ("candy", 2, 2, 0),
    "smoothie": ("fruit bowl", 3, 3, 0),
    "tart": ("pie", 3, 3, 0),
    "pudding": ("cake", 3, 3, 0),
    "candy": ("sundae", 3, 3, 0),
    "cake": ("dessert feast", 4, 10, 0),
    "pie": ("dessert feast", 4, 10, 0),
    "sundae": ("dessert feast", 4, 10, 0)
}

def calculate_merge(usr_input, coins, usr_points):
    """
    Determines if a merge is valid and calculates updated points.
    Merging does not deduct coins.
    """
    if usr_input == "feast":
        # Logic for the final goal (3-item merge)
        return usr_points + 100, coins, "dessert feast"

    if usr_input in RECIPES:
        result, tier, pt_val, cost = RECIPES[usr_input]
        updated_points = usr_points + pt_val
        # Return coins unchanged to ensure merging is free
        return updated_points, coins, result
    
    return usr_points, coins, None

def main():
    user_deck = []
    user_coins = 500
    user_points = 0
    level_label = "Novice Chef"
    level_id = 0

    print("Welcome to the Dessert Feast Efficiency Challenge!")
    print("Goal: Use your 500 coins to create as many Dessert Feasts as possible.")
    
    # Final summary of game result
    print("\n--- FINAL RESULTS ---")
    print(f"Total Points: {user_points}")
    print(f"Feasts Created: {user_deck.count('dessert feast')}")
    print(f"Coins Remaining: {user_coins}")

if __name__ == "__main__":
    main()