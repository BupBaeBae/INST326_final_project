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
## Ngoc Nguyen

## John Nguyen ##
class Player:
    """ 
    representation of a Player
    
    Attributes:
        deck (list of str): player's current collection of ingredients that they have
        balance (int): player's current amount of coins
        points (int): player's current amount of points
        level (str): player's current level
        
    """
    def __init__(self, name, deck = None, balance = 500, points = 0, level = "Novice Chef"):
        """initializes a Player's attributes - John Nguyen"""
        self.name = name
        self.deck = deck if deck is not None else []
        self.balance = balance
        self.points = points
        self.level = level
        
    def __str__(self):
        """informal representation of Player - John Nguyen"""
        return (
                f"{self.name}, "
                f"{self.deck}, "
                f"{self.balance}, "
                f"{self.points}, "
                f"{self.level} "
                )
        
    def __repr__(self):
        """string representation of Player - John Nguyen"""
        return (
                f"Chef {self.name} Attributes:\n"
                f"Deck: {self.deck}\n" 
                f"Balance: {self.balance}\n" 
                f"Points: {self.points}\n" 
                f"Level: {self.level}"
                )
## John Nguyen ##    

# Ngoc Nguyen    
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
    completed_recipe_list = []
    
    if usr_input == "feast":
        
        completed_recipe_list.append("feast")
        
        # Logic for the final goal (3-item merge)
        return usr_points + 100, coins, "dessert feast"

    if usr_input in RECIPES:
        result, tier, pt_val, cost = RECIPES[usr_input]
        updated_points = usr_points + pt_val
        
        completed_recipe_list.append(result)
        
        # Return coins unchanged to ensure merging is free
        return updated_points, coins, result
    
    return usr_points, coins, None

class GameManager:
    """
    Manages the game flow, the player, and tracks overall game progression.
    """
    def __init__(self, player):
        """
        Initializes the manager with a player and the recipe data.

        Args:
            player (Player): Player class object.
        """
        self.player = player
        self.is_running = True
        self.completed_recipes = []
        # level_id used for validate_purchase logic
        self.level_id_map = {"Novice Chef": 1, "Advanced Chef": 2, "Expert Chef": 3}

    def get_level_id(self):
        """
        Gets the chef's level.

        Returns:
            str: returns chef's level, as a string, that matches with the level 
                ID number.
        """
        return self.level_id_map.get(self.player.level, 1)  
# Ngoc Nguyen

## John Nguyen ##
def merge(current_deck, ingredient_to_merge, new_product, is_feast=False):
    """
    Updates deck after successful merge event by removing used ingredients
    and adding the newly merged product in their place
    - John Nguyen
    
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

    
#Lilia Burkes
def update_store_items(completed_recipe_list, current_lvl,
                           ingredients, new_ingredients):
    """Levels up the player when they reach a level benchmark, unlocks new 
        ingredients. If a level’s benchmark item/recipe is present in 
        completed_recipe_list, the player moves on to the next level.  

    Args:
        completed_recipe_list (list): list of all successful merges by the player
	    current_lvl (str): “novice chef”, “advanced chef” “expert chef”
	    ingredients (list): current ingredients available to the player
	
    Side effects:
	    current_lvl (str) is set to a new level value
	    ingredients (list) is amended with more ingredients depending on new level (from data file)
    
    """

    benchmark = {
        'Advanced Chef': 'juice',
        'Expert Chef': 'pudding'
    }

    for level, recipe in benchmark.items():
        if recipe in completed_recipe_list:
            current_lvl = level
            if new_ingredients is not None and new_ingredients not in ingredients:
                ingredients.append(new_ingredients)

    return current_lvl, ingredients

#Siddhant Chintaluri         
def validate_purchase(ingredient_name, cost, balance, deck, level_id, 
                      max_inventory_size=10):
    """
    Validates whether a purchase is legal given the player's current state.
    Checks affordability, inventory space, level gate, and input correctness.
    
    Args:
        ingredient_name (str): name of the ingredient the player wants to buy
        cost (int): price of the ingredient
        balance (int): player's current coin amount
        deck (list): current inventory of ingredients
        level_id (int): player's current level, used to gate higher-tier 
                        purchases
        max_inventory_size (int): maximum allowed inventory size, defaults to 10

    Returns:
        bool: True if the purchase is valid, False otherwise

    Raises:
        ValueError: if cost is zero or negative
        ValueError: if ingredient_name is not a string

    """
    if cost <= 0:
        raise ValueError("Invalid cost")

    if not isinstance(ingredient_name, str):
        raise ValueError("Invalid ingredient name")

    if ingredient_name in RECIPES:
        _, tier, _, _ = RECIPES[ingredient_name]
        if tier > level_id:
            print(f"You must reach level {tier} to purchase {ingredient_name}.")
            return False

    if cost > balance:
        raise ValueError("Game Over")

    if len(deck) >= max_inventory_size:
        print("Inventory full. Cannot purchase.")
        return False

    return True


def purchase_ingredient(ingredient_name, cost, balance, deck, level_id, 
                        max_inventory_size=10):
    """
    Purchases an ingredient if valid, deducting coins and adding it to the deck.
    Calls validate_purchase first before making any changes to game state.

    Args:
        ingredient_name (str): name of the specific ingredient you want to buy
        cost (int): integer price of the ingredient to be deducted from the 
                    balance
        balance (int): player's current coin amount
        deck (list): collection of ingredients available to the player
        level_id (int): the player's current level, used to gate higher-tier 
                        purchases
        max_inventory_size (int): maximum allowed inventory size, defaults to 10

    Returns:
        balance (int): updated balance after the purchase
        deck (list): updated deck containing the new ingredient

    Side Effects:
        Prints confirmation message if the purchase is successful.
        Prints warning message if balance is low.

    Raises:
        ValueError: if cost is zero or negative
        ValueError: if ingredient_name is not a string
        ValueError: if cost exceeds balance, triggering a "Game Over" state

    Techniques demonstrated: f-strings containing expressions
    """
    if not validate_purchase(ingredient_name, cost, balance, deck, level_id, 
                             max_inventory_size):
        return balance, deck

    count = 0
    for item in deck:
        if item == ingredient_name:
            count += 1

    if count >= 3:
        print(
            f"You already have 3 {ingredient_name} items. Consider merging them."
            )

    balance -= cost
    deck.append(ingredient_name)

    if balance <= 50:
        print("Warning: Low balance!")
    elif balance <= 100:
        print("Careful: You are entering low funds range.")

    print(f"Purchased {ingredient_name} successfully. "
          f"Remaining balance: {balance} coins.")

    return balance, deck
# Siddhant Chintaluri


# Ngoc Nguyen   
def main():
    name = input("Enter your Chef Name: ")
    p = Player(name)
    game = GameManager(p)
    
    available_to_buy = ["apple", "strawberry"]
    
    print(f"\nWelcome {p.name} to the Dessert Feast Efficiency Challenge!")
    print("Goal: Use your 500 coins to create as many Dessert Feasts as possible.")
    
    try:
        while game.is_running:
            print(f"\nStatus: {p}")
            action = input("\nAction: [B]uy, [M]erge, [Q]uit: ").strip().upper()
            
            if action == "B":
                print(f"Marketplace (Available: {available_to_buy})")
                item = input("What would you like to buy? ").strip().lower()
                
                if item in available_to_buy:
                    cost = RECIPES[item][3]
                    p.balance, p.deck = purchase_ingredient(
                        item, cost, p.balance, p.deck, game.get_level_id()
                    )
                else:
                    print("That item is not available for purchase.")
            elif action == "M":
                target = input("Which item to merge? (Type 'feast' for final goal): ").lower()
                
                if target == "feast":
                    if all(x in p.deck for x in ["cake", "pie", "sundae"]):
                        p.points, p.balance, result = calculate_merge("feast", p.balance, p.points)
                        p.deck = merge(p.deck, None, result, is_feast=True)
                        game.completed_recipes.append(result)
                        print("SUCCESS! You created a Dessert Feast!")
                    else:
                        print("Incomplete ingredients! You need a Cake, Pie, and Sundae.")
                        
                elif p.deck.count(target) >= 2:
                    p.points, p.balance, result = calculate_merge(target, p.balance, p.points)
                    p.deck = merge(p.deck, target, result)
                    game.completed_recipes.append(result)
                    print(f"Merge successful! You now have {result}.")
                    
                    unlock_ingredients = {"juice": "banana", "pudding": "blueberry"}
                    new_item = unlock_ingredients.get(result)
                    p.level, available_to_buy = update_store_items(
                        game.completed_recipes, p.level, available_to_buy, new_item
                    )
                else:
                    print(f"Not enough {target} items to merge.")

            elif action == "Q":
                game.is_running = False
            
            elif action != "":
                    print(f"Invalid action: '{action}'. Please use B, M, or Q.")
        
    except ValueError as e:
        print(f"\nGAME OVER: {e}")  
           
    print("\n" + "="*30)
    print("FINAL RESULTS")
    print(f"Chef: {p.name}")
    print(f"Total Points: {p.points}")
    print(f"Feasts Created: {p.deck.count('dessert feast')}")
    print(f"Coins Remaining: {p.balance}")
    print("="*30)

if __name__ == "__main__":
    main()
# Ngoc Nguyen