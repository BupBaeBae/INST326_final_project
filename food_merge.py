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

## John Nguyen ##
def update_deck(current_deck, ingredient_to_merge, new_product, is_feast=False):
    """
    Updates deck after successful merge event by removing used ingredients
    and adding the newly merged product in their place
    
    Args:
        current_deck (list of str):
            Current deck before any changes
        ingredient_to_merge (str):
            Old ingredient used in a merge event
            that will be removed from the deck.
            Uses two of this ingredient for a merge.
        new_product (str):
            new ingredient added to the deck from a merge event
        is_feast (bool):
            checks if final goal was reached or not
        
    Returns:
        current_deck (list of str): 
            updated deck with new higher tier products 
            added in place of the merged ingredients
        
    Side effects:
        Modifies current_deck by removing used ingredients and appending the new
        product. Deck size will decrease as two or more ingredients are replaced
        by one merged item
    """
    # dessert_feasts needs these 3 items merged to be created
    dessert_feast = ["cake", "pie", "sundae"]
    
    # remove items from the feast
    if is_feast:
        for item in dessert_feast:
            current_deck.remove(item)
    # remove items in a regular merge
    else:
        for i in range(2):
            current_deck.remove(ingredient_to_merge)
        
    # add newly merged item to the deck
    current_deck.append(new_product)
    
    return current_deck
    ## John Nguyen ##
    
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