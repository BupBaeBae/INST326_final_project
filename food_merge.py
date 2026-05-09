import random

# Ngoc Nguyen
# Format: "ingredient": ("result", tier, point_value, purchase_cost)
RECIPES = {
    "apple": ("juice", 1, 1, 10),
    "strawberry": ("jam", 1, 1, 10),
    "banana": ("puree", 1, 1, 15),
    "blueberry": ("syrup", 1, 1, 15),
    "juice": ("smoothie", 2, 2, 30),
    "jam": ("tart", 2, 2, 30),
    "puree": ("pudding", 2, 2, 50),
    "syrup": ("candy", 2, 2, 50),
    "smoothie": ("fruit bowl", 3, 3, 0),
    "tart": ("pie", 3, 3, 0),
    "pudding": ("cake", 3, 3, 0),
    "candy": ("sundae", 3, 3, 0),
    "fruit bowl": (None, 4, None, 0), 
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
        
    Side Effects:
        sets attributes of a Player
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
                f"{self.name} \n"
                f"{self.deck} \n"
                f"{self.balance} coins, "
                f"{self.points} points, "
                f"{self.level} "
                )
        
    def __repr__(self):
        """string representation of Player - John Nguyen"""
        return (
                f"Chef {self.name} stats:\n"
                f"Deck: {self.deck}\n" 
                f"Coins remaining: {self.balance}\n" 
                f"Total Points: {self.points}\n" 
                f"Level: {self.level}"
                )
## John Nguyen ##    

# Ngoc Nguyen
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
#Ngoc Nguyen

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
            checks if merging for feast
        
    Returns:
        current_deck (list of str): 
            updated deck with new higher tier products 
            added in place of the merged ingredients
        
    Side effects:
        Modifies current_deck by removing used ingredients and appending the new
        product. Deck size will decrease as two or more ingredients are replaced
        by one merged item
    """
    # dessert_feast needs specific items to be merged in order to be created
    dessert_feast = [item for item in RECIPES if RECIPES[item][0] == "dessert feast"]    
    
    # remove items from the feast from current deck
    if is_feast:
        for item in dessert_feast:
            current_deck.remove(item)
    # remove items in a regular merge from current deck
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
        
            ingredients.append(new_ingredients) if new_ingredients is not None \
                and new_ingredients not in ingredients else None


    # for level, recipe in benchmark.items():
    #     if recipe in completed_recipe_list:
    #         current_lvl = level
    #         if new_ingredients is not None and new_ingredients not in ingredients:
    #             ingredients.append(new_ingredients)

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

## John Nguyen ##
def shop_prices(available_items):
    """ shows list of available ingredients and their prices
    
    Returns:
        shop (list): list of available ingredients and their prices
    
    """
    shop = [f"{item} ({RECIPES[item][3]})" for item in available_items]
        
    return shop
## John Nguyen ##
        
### Lilia Burkes ####
def give_hint():
    """ Retrieves a list of hints from a bank stored in a txt file.
    
    Returns:
        hints (list): a list of hints taken from hints.txt
        
    Side Effects:
        opens and reads from hints.txt
    
    """
    
    hints = []
    
    with open("hints.txt", mode = "r", encoding="utf-8") as hint_pipeline:
        
        for hint in hint_pipeline:
            
            hints.append(hint)    
                      
        return hints

### Lilia Burkes ####
def sell_value(product, level_id):
    """ Determines the sell price for an item depending on the item's 
        tier and the player's level
    
    Args:
        level_id (int): the player's current level, used to gate higher-tier 
                        purchases
        product (str): the item the player is attempting to sell   
        
    Returns:
        sell_price (int): the calculated total value of an item     
       
    """
        
    if RECIPES[product][0] and RECIPES[product][1] < 3:
                     sell_price = level_id * (round(RECIPES[product][3] * .3))
                    
    elif RECIPES[product][0] and RECIPES[product][1] > 2:
                     sell_price = level_id * (RECIPES[product][1] * 3)
                          
    return sell_price


### Lilia Burkes ###
def sell(balance, deck, sell_price, product):
    """ Determines the players balance and deck after they sell an item.
    
    Args:
        balance (int): player's current coin amount
        deck (list): collection of ingredients available to the player
        sell_price (int): the calculated value of a product when sold based 
                            on player level.
        product (str): the item the player is attempting to sell        

    Side Effects:
        balance (int): increases in value based on the sell price of their
                        product
        deck (list): sold items are removed from the deck
        
    Returns:
        balance (int): with added sell_price
        deck (list): missing one item
        
    
    """
        
    balance += sell_price
    
    deck.remove(product) 
    
    return balance, deck  

# Ngoc Nguyen   
def main():
    
    name = input("Enter your Chef Name: ")
    p = Player(name)
    game = GameManager(p)
    
    available_to_buy = ["apple", "strawberry"]
    
    # Siddhant
    premium_items = ["juice", "jam", "puree", "syrup"]
    
    print(f"\nWelcome Chef {p.name} to the Dessert Feast Merge Challenge!")
    print("\n                     HOW TO PLAY\n")
    print("input 'b' to buy, 'm' to merge, or 'q' to end the game\n")
    print("You start with 500 coins to buy ingredients, and you don't get any more, so use them wisely!\n")
    print("To merge, you must have 2 of the same ingredient\n")
    print("You can merge to the special dessert feast by having the key ingredients\n")
    print("Level up by merging to certain foods to unlock more foods to buy and merge\n")
    print("Levels: Novice Chef, Advanced Chef, Expert Chef\n")
    print("Goal: Use your 500 coins to create as many Dessert Feasts as possible\n")
    print(f"Good luck Chef {p.name}!\n")
    
    try:
        while game.is_running:
            print(f"\nSTATUS: \n{p}")
            action = input("\nAction: [B]uy, [M]erge, [S]ell, [H]int, [Q]uit: ").strip().upper()
            
            if action == "B":
                print(f"Marketplace: {shop_prices(available_to_buy)}")
                #siddhant chintaluri
                #print(f"Premium (Requires Advanced Chef level): {premium_items}")
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
                    if RECIPES[target][0] in RECIPES:
                        p.points, p.balance, result = calculate_merge(target, p.balance, p.points)
                        p.deck = merge(p.deck, target, result)
                        game.completed_recipes.append(result)
                        print(f"Merge successful! You now have {result}.")
                        
                        unlock_ingredients = {"juice": "banana", "pudding": "blueberry"}
                        new_item = unlock_ingredients.get(result)
                        p.level, available_to_buy = update_store_items(
                            game.completed_recipes, p.level, available_to_buy, new_item
                        )
                    elif RECIPES[target][0] not in RECIPES:
                        print("You can't merge that any further")
                else:
                    print(f"Not enough {target} items to merge.")
                    
                    
            elif action == "S":
                product = input("What do you want to sell?: ").lower()
                
                if product in p.deck:
                    sell_price = sell_value(product, game.get_level_id())
                    
                    sell_question = input(f"\nSell {product} for {sell_price} coins? [Y]es/[N]o: ").strip().upper()
                    
                    if sell_question == "Y":
                            
                        p.balance, p.deck = sell(p.balance, p.deck, \
                                                    sell_price, product)
                            
                    else:
                        pass
                    
                else:
                    print(f"You don't have any {product}s to sell.")
                    
            elif action == "H":
                
                # Lilia Burkes
                
                hints = give_hint()
                
                random_index = random.randint(0, len(hints) - 1)
                
                hint = hints[random_index] 
                
                print(f"Hint: {hint}")
                

            elif action == "Q":
                game.is_running = False
            
            elif action != "":
                    print(f"Invalid action: '{action}'. Please use B, M, or Q.")
        
    except ValueError as e:
        print(f"\nGAME OVER: {e}")  
           
    print("\n" + "="*30)
    print("FINAL RESULTS")
    print(repr(p))
    print(f"Feasts Created: {p.deck.count('dessert feast')}")
    print("="*30)

if __name__ == "__main__":
    main()
# Ngoc Nguyen