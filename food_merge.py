import random

# Ngoc Nguyen
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
    Determines if a merge is valid and calculates updated points and coins.
    Merging does not deduct coins.
    
    Args:
        usr_input (str): The name of the ingredient the player wants to merge.
        coins (int): The current amount of coins the player has.
        usr_points (int): The current amount of points the player has.
        
    Returns:
        updated_points (int): The player's updated points after a merge.
        coins (int): The amount of coins left, remains unchanged during a merge.
            and only changes after purchasing new ingredient.
        result (str): The name of the higher-tier product created.
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
# Ngoc Nguyen

# Siddhant Chintaluri
def purchase_ingredient(ingredient_name, cost, balance, deck):
    """
    Users begin with a set amount of 500 coins, which will be spent on 
    ingredients to merge together. No more coins will be given throughout the 
    game, the goal being to achieve the final item with as few coins spent 
    (as efficient as possible)

    Args:
        ingredient_name (str): name of the specific ingredient you want to buy
        
        cost (int): integer price of the ingredient to be deducted from the 
                    balance
        balance (int): Player’s current coin amount
        deck (list): collection of ingredients available to the player based on 
                     tier level
        max_inventory_size (int): maximum allowed inventory size

    Returns: 
        balance (int): updated balance after the purchase
        ingredients (list): updated deck containing the new ingredient

    Side Effects:
        Confirmation message if the purchase is successful
        Prints “warning” message if balance is low or inventory is near full

    Raises:
        ValueError: if cost exceeds the balance, prompting a “Game Over” state

        This function ONLY handles purchasing (coin deduction + adding an 
        ingredient to the deck).
        It does NOT handle removing ingredients, merging items, or modifying the
        deck after a merge.
    """
    max_inventory_size = 10
    # Validate input
    if cost <= 0:
        raise ValueError("Invalid cost")

    if not isinstance(ingredient_name, str):
        raise ValueError("Invalid ingredient name")

    # Check affordability
    if cost > balance:
        raise ValueError("Game Over")

    # Check inventory space
    if len(deck) >= max_inventory_size:
        print("Inventory full. Cannot purchase.")
        return balance, deck

    # Check duplicates
    count = 0
    for item in deck:
        if item == ingredient_name:
            count += 1

    if count >= 3:
        print(f"You already have many {ingredient_name} items.")

    # Deduct cost
    balance -= cost

    # Add ingredient
    deck.append(ingredient_name)

    # Warnings system
    if balance <= 50:
        print("Warning: Low balance!")

    if balance <= 100:
        print("Careful: You are entering low funds range.")

    print(f"Purchased {ingredient_name} successfully.")

    return balance, deck
# Siddhant Chintaluri

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