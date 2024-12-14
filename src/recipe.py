import random
import re
from unicodedata import numeric
from fractions import Fraction
import KBLoader
import string
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


class Ingredient:
    def __init__(self, amount, measure_type, ingr, ingredient_type=None):
        self.amount = amount
        self.measure_type = measure_type
        self.ingredient_type = ingredient_type
        self.ingr = ingr

    def __str__(self):
        return 'Amount = {0}, MeasureType = {1}, IngredientType = {2}, Ingredient = {3} '.format(self.amount,
                                                                               self.measure_type, self.ingredient_type,
                                                                               self.ingr)
class Recipe:
    def __init__(self, ingredients, steps):
        self.recipe_ingredients = ingredients
        self.recipe_steps = steps
        self.ingredients = []
        self.meats = set()
        self.tools = set()
        self.primary_methods = set()
        self.secondary_methods = set()
        self.KBfoods = KBLoader.get_kaggle_foods()
        self.KBfoodscusine = KBLoader.get_kaggle_food_with_cusine()
        self.KBmeats = KBLoader.get_all_meats()
        self._populate_ingredients()
        self._populate_methods_and_tools()
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.chinese_foods = ['frozen mixed thawed vegetables,', 'lap cheong', 'oyster sauce', 'green bell pepper', 'ginger piece', 'green lentil', 'Kikkoman Oyster Sauce', 'soy', 'fillet red snapper', 'chili pepper', 'crushed red pepper flakes', 'button mushrooms', 'tree ear mushrooms', 'choy sum', 'kecap manis', 'ruby port', 'pork bouillon cube', 'rice', 'dried minced onion', 'pickled radish', 'mushroom powder', 'steamed white rice', 'black rice', 'quail eggs', 'taro', 'nut oil', 'medium dry sherry', 'citric acid powder', 'black tea', 'chicken-flavored soup powder', 'chinese noodles', 'white rice', 'whole milk', 'mustard powder', 'flavored wine', 'seeds', 'teriyaki marinade', 'ginseng tea', 'red chili peppers', 'vanilla essence', 'chinese plum sauce', 'sake', 'chinese chives', 'seaweed', 'black garlic', 'chili paste with garlic', 'garland chrysanthemum', 'soybean paste', 'fermented bean curd', 'sliced green onions', 'Chinese sesame paste', 'Fuyu persimmons', 'safflower oil', 'white sesame seeds', 'white rice flour', 'bone in chicken thighs', 'canned corn', 'slaw mix', 'steamed brown rice', 'distilled vinegar', 'gluten-free oyster sauce', 'tiger lily buds', 'shell-on shrimp', 'lump crab meat', 'roast', 'minced garlic', 'zest', 'rock salt', 'pork shoulder boston butt', 'chinese buns', 'granulated white sugar', 'fresh spinach', 'chopped fresh mint', 'black', 'dry mustard', 'ground beef', 'orange extract', 'powdered garlic', 'fresh ginger root', 'frosting', 'ginkgo nut', 'loin pork roast', 'dark leafy greens', 'frozen pastry puff sheets', 'minced ginger', 'minced beef', 'bean curd stick', 'store bought low sodium chicken stock', 'chinese five-spice powder', 'seitan', 'cinnamon sticks', 'cassia cinnamon', 'shiitake', 'yellow split peas', 'onion tops', 'vidalia onion', 'gluten-free tamari sauce', 'wine', 'basil', 'ginger root', 'savoy cabbage', 'gari', 'garlic', 'curry paste', 'sweet soy sauce', 'grated lemon zest', 'bird chile', 'torn romain lettuc leav', 'tomato paste', 'green pepper', 'hot chili paste', 'tapioca flour', 'vegetable stock', 'baby corn', 'egg roll wraps', 'linguine', 'stir fry sauce', 'dashi', 'coconut sugar', 'char', 'garlic bulb', 'ginseng', 'leaf lettuce', 'lime leaves', 'ramen noodles', 'sunflower oil', 'cooked brown rice', 'dumpling dough', 'food colouring', 'vanilla powder', 'fish balls', 'pickle juice', 'dried black mushrooms', 'rice pilaf', 'kimchi', 'adzuki beans', 'water chestnuts', 'garlic oil', 'sichuan peppercorn oil', 'fresh chives', 'rice wine', 'snow pea pods', 'dry sherry', 'Chinese egg noodles', 'asparagus', 'globe eggplant', 'brown mushroom', 'tomato ketchup', 'frozen petit pois', 'gluten-free tamari', 'cherries', 'chuck', 'hot chili oil', 'diced onions', 'celery stick', 'wheat free soy sauce', 'pork loin chops', 'frozen edamame beans', 'mint sprigs', 'mango chutney', 'dry white wine', 'red pepper flakes', 'Tabasco Pepper Sauce', 'e-fu noodl', 'all-purpose flour', 'trout', 
'balsamic vinegar', 'fillet steaks', 'red bliss potato', 'cider vinegar', 'tapioca pearls', 'mace', 'silken tofu', 'semi firm tofu', 'pork rind', 'red beans', 'hawaiian sweet rolls', 'quick cooking brown rice', 'hearts of romaine', 'crisco', 'star anise', 
'sesame chili oil', 'rapeseed oil', 'vegetables', 'pickled vegetables', 'vegetarian oyster sauce', 'merluza', 'red bell pepper', 'garlic cloves', 'toasted almonds', 'varnish clams', 'mixed mushrooms', 'cooking wine', 'uncooked vermicelli', 'unsweetened coconut milk', 'fresh pineapple', 'dried dates', 'soup', 'shredded cabbage', 'beef tenderloin', 'raw honey', 'chopped fresh chives', 'mein', 'juice', 'chicken pieces', 'diced red onions', 'pork tenderloin', 'capsicum', 'white distilled vinegar', 'peapods', 'ground pork', 'fat free less sodium beef broth', 'brisket', 'yams', 'parsley', 'pork sausages', 'chinese pea pods', 'dough', 'lobster tails', 'grape tomatoes', 'pickling cucumbers', 'ground chicken breast', 'chicken thighs', 'olives', 'duck', 'yellow curry paste', 'shanghai bok choy', 'low-sodium low-fat chicken broth', 'whole grain thin spaghetti', 'flowering garlic chives', 'portabello mushroom', 'chinese black mushrooms', 'fat free less sodium chicken broth', 'champagne', 'celery root', 'pork loin', 'semi-sweet chocolate morsels', 'prawns', 'Japanese mountain yam', 'chile sauce', 'thyme', 'rabbit', 'savory', 'broccoli stems', 'loin', 'liquid aminos', 'palm sugar', 'scallops', 'chopped leaves', 'egg roll skins', 'boneless sirloin', 'ramps', 'tangzhong roux', 'cabbage leaves', 'cod fillets', 'onions', 'instant rice', 'romaine lettuce hearts', 'toasted sesame seeds', 'vanilla extract', 'ground sage', 'lotus roots', 'evaporated milk', 'vegetable shortening', 'nonstick spray', 'honey mustard', 'lemon grass', 'apple cider vinegar', 'dried rice noodles', 'lamb', 'fresh green bean', 'center cut pork roast', 'carp', 'egg yolks', 'hot pepper sauce', 'fresh asparagus', 'daikon', 'romaine lettuce leaves', 'simple syrup', 'bread flour', 'whole wheat spaghetti', 'lean minced beef', 'caster sugar', 'radishes', 'boar', 'vinegar', 'chinese celery', 'dried lentils', 'club soda', 'corn flour', 'soy milk', 'boneless chicken', 'tart shells', 'pork stock', 'broccoli rabe', 'sushi rice', 'dried cherry', 'baby spinach', 'bibb lettuce', 'pea pods', 'sirloin', 'chili bean paste', 'brown rice vinegar', 'whipped cream', 'spring greens', 'pineapple chunks', 'sweet pepper', 'cilantro sprigs', 'double-acting baking powder', 'coconut oil', 'chuka soba noodles', 'rum', 'black bean garlic sauce', 'fillet of beef', 'coconut extract', 'red bean paste', 'pork spare ribs', 'new york strip steaks', 'pink peppercorns', 'canned low sodium chicken broth', 'whole chicken', 'dry yeast', 'frozen orange juice concentrate', 'green cabbage', 'cubed beef', 'goji berries', 'taco shells', 'Italian parsley leaves', 'garbanzo beans', 'sweet rice wine', 'ground cayenne pepper', 'boiling water', 'rib', 'chinese celery cabbage', 'thick-cut bacon', 'pig', 'other vegetables', 'sweet basil', 'fat skimmed reduced sodium chicken broth', 'rice flour', 'licorice root', 'boneless skinless chicken', 'kale', 'dark soy sauce', 'ponzu', 'brown rice', 'Korean chile flakes', 'dark sesame oil', 'small eggs', 'fry mix', 'scrod fillets', 'butterflied leg of lamb', 'coca-cola', 'peppercorns', 'coleslaw', 'cooked chicken', 'baby gem lettuce', 'lentils', 'white wine', 'fresh coriander', 'fillets', 'longan', 'chicken meat', 'ground black pepper', 'potatoes', 'brandy', 'serrano peppers', 'toasted slivered almonds', 'low sodium beef broth', 

'boiling potatoes', 'stevia', 'shrimp stock', 'pangasius', 'ground roasted sichuan peppers', 'sesame seeds', 'lapsang souchong', 'soy nuts', 'baking soda', 'shallots', 'granulated garlic', 'baby back ribs', 'mustard greens', 'duck drumsticks', 'hot sauce', 'forest mushroom', 'thai chile', 'egg roll wrappers', 'cornflour', 'plum wine', 'sunflower seeds', 'green tomatoes', 'store bought low sodium vegetable stock', 'boneless chicken thighs', 'salted seaweed', 'snow pea shoots', 'apricot preserves', 'fat free beef broth', 'corn syrup', 'bean paste', 'beef brisket', 'low sodium vegetable broth', 'black bean sauce with garlic', 'roasted white sesame seeds', 'Soy VayÂ® Toasted Sesame Dressing & Marinade', 'anise', 'reduced sodium teriyaki sauce', 'chicken bouillon', 'nian gao', 'romaine lettuce', 'natto', 'natural peanut butter', 'lemon pepper', 'habanero', 'chinese sausage', 'green apples', 'salted fish', 'almond paste', 'gingerroot', 'turkey meat', 'sirloin steak', 'vermicelli', 'dressing', 'yardlong beans', 'dried soba', 'dried shiitake mushrooms', 'chicken carcass', 'cooked rice', 'sambal chile paste', 'cooking spray', 'char siu sauce', 'chilli paste', 'maldon sea salt', 'aspic', 'lo bok', 'mi', 'barley flakes', 'purple onion', 'lean ground beef', 'white rice vinegar', 'mandarin orange segments', 'white miso', 'Lea & Perrins Worcestershire Sauce', 'fresh basil leaves', 'unsalted dry roast peanuts', 'edamame', 'breast of lamb', 'giblet', 'frozen popcorn chicken', 'cream of mushroom soup', 'lemon wedge', 'whiskey', 'angel hair', 'egg noodles', 'chinese jujubes', 'almond extract', 'thai basil', 'sugar substitute', 'steamer', 'sesame oil', 'muscovado sugar', 'white flour', 'gluten-free hoisin sauce', 'cooked quinoa', '33 less sodium smoked fully cooked ham', 'orange zest', 'lower sodium chicken broth', 'asian fish sauce', 'glutinous rice', 'cocktail cherries', 'wheatberries', 'bread crumbs', 
'chopped onion', 'cooked bacon', 'store bought low sodium chicken broth', 'sweet rice', 'bread', 'raw sugar', 'steak', 'broiler-fryer chicken', 'low sodium gluten free soy sauce', 'potsticker wrappers', 'frozen garden peas', 'celery', 'pepper flakes', 'white button mushrooms', 'spring roll wrappers', 'buttermilk', 'flowering chives', 'bacon', 'chinese rock sugar', 'regular soy sauce', 'pickles', 'coarse salt', 'scallions', 'rainbow trout', 'spices', 'leeks', 'tofu puffs', 'regular sugar', 'teas', 'chicken fingers', 'celery seed', 'lamb shoulder', 'leftover steak', 'plantains', 'fermented bean paste', 'yellow chives', 'golden brown sugar', 'vietnamese fish sauce', 'seasoning', 'arugula', 'frozen peas', 'century eggs', 'chili powder', 'ground nutmeg', 'chili sauce', 'whole peppercorn', 'groundnut', 'bone-in chicken breasts', 'fronds', 'spinach leaves', 'milk', 'hand', 'low sodium stock', 'walnuts', 'curry powder', 'chicken stock cubes', 'minced chicken', 'puff pastry sheets', 'coarse kosher salt', 'stem ginger in syrup', 'mushrooms', 'roasted hazelnuts', 'tree ears', 'gyoza', 'bai cai', 'ground white pepper', 'chinese pancakes', 'dumplings', 'chinese mustard', 'rotisserie chicken', 'asian barbecue sauce', 'hot pepper', 'oysters', 'corn starch', 'skinless chicken breasts', 'fresh chicken stock', 'shrimp heads', 'peaches', 'green cardamom', 'pak choi', 'buns', 'top sirloin steak', 'orange peel', 'baby portobello mushrooms', 'orange', 'pork spareribs', 'beef stock', 'halibut fillets', 'fresh thyme leaves', 'liquorice', 'tarragon', 'large egg yolks', 'chicken thigh fillets', 'chinese black vinegar', 'chilli bean sauce', 'serrano chile', 'fresh tomatoes', 'ketchup', 'pears', 'rub', 'coriander seeds', 'side pork', 'Chinese rose wine', 'iceberg lettuce', 'hoisin sauce', 
'wide rice noodles', 'freshly ground pepper', 'caramel sauce', 'onion salt', 'fish paste', 'gluten free soy sauce', 'cracker crumbs', 'curly kale', 'nuts', 'lemongrass', 'fresh chili', 'Lipton Sparkling Diet Green Tea with Strawberry Kiwi', 'konbu', 'flavored oil', 'salted roast peanuts', 'fresh pork fat', 'top round steak', 'sweet corn', 'grated carrot', 'green onions', 'red chile sauce', 'peeled prawns', 'boiled ham', 'won ton skins', 'wine vinegar', 'chile paste with garlic', 'crushed pineapples in juice', 'vegetable broth', 'red radishes', 'beef sirloin', 'frozen broccoli', 'lower sodium soy sauce', 'sliced cucumber', 'low sodium teriyaki sauce', 'roasted sesame seeds', 'medium egg noodles', 'peanut sauce', 'Argo Corn Starch', 'dumpling wrappers', 'chicken', 'turbinado', 'pinenuts', 'fat-free chicken broth', 'yolk', 'red snapper', 'sweet and sour sauce', 'adobo', 'beef', 'serrano chilies', 'white bread', 'long grain white rice', 'meat bones', 'lobster', 'frozen shelled edamame', 'chinese red rice vinegar', 'ghee', 'beans', 'black vinegar', 'cayenne pepper', 'spring roll skins', 'dried prawns', 'reduced fat creamy peanut butter', 'glutinous rice flour', 'hot mustard', 'cabbage', 'long green chilies', 'extra large shrimp', 'beef consomme', 'wheat flour', 'salad greens', 'beef stew meat', 'fresh mushrooms', 'condensed milk', 'white rum', 'cayenne', 'curing salt', 'fresh mint', 'beef bones', 'hamburger', 'cane vinegar', 'grapeseed oil', 'jalapeno chilies', 'regular sour cream', 'black moss', 'imitation crab meat', 'soy sauce', 'peeled fresh ginger', 'chinese radish', 'Soy VayÂ® Hoisin Garlic Marinade & Sauce', 'reduced-fat sour cream', 
'honey', 'ground chicken', 'pork cutlets', 'haricots verts', 'filet', 'low sodium store bought chicken stock', 'rice stick noodles', 'vegan chicken flavored bouillon', 'marsala wine', 'cranberries', 'active dry yeast', 'medium shrimp', 'red vinegar', 'granulated sugar', 'goma', 'chopped cilantro', 'self raising flour', 'rice vermicelli', 'Thai chili garlic sauce', 'medium firm tofu', 'beaten eggs', 'cold water', 'calamari steak', 'squid', 'cooking oil', 'lean beef', 'fresh chile', 'eggplant', 'boneless sirloin steak', 'jasmine rice', 'chinese hot mustard', 'chow mein noodles', 'lemon juice', 'chenpi', 'bicarbonate of soda', 'fruit', 'tahini', 'finely chopped onion', 'white vinegar', 'white mushrooms', 'fresh udon', 'greater yam', 'chinese roast pork', 'reduced sodium soy sauce', 'tea cake', 'fresh lemon juice', 'sweet potato starch', 'soba noodles', 'starch', 'poppy seeds', 'crosswise', 'dates', 'chopped walnuts', 'black bean stir fry sauce', 'sweet bean sauce', 'spareribs', 'bamboo shoots', 'Japanese soy sauce', 'cut up chicken', 'pineapple', 'black pepper', 'shredded lettuce', 'peeled tomatoes', 'flavoring', 'cooked long-grain brown rice', 'white truffle oil', "I Can't Believe It's Not Butter!Â® Spread", 'baking potatoes', 'fish sauce', 'large garlic cloves', 'comice pears', 'deveined shrimp', 'green leaf lettuce', 'mung bean sprouts', 'dried Thai chili', 'free-range eggs', 'wax beans', 'lamb chops', 'clove', 'diced green chilies', 'carrots', 'roasted cashews', 'coconut flour', 'chicken stock', 'country crock calcium plus vitamin d', 'liqueur', 'fresh cilantro', 'cream', 'beets', 'rooster', 'corn oil', 'chopped garlic', 'pineapple rings', 'jujube', 'spam', 'corn kernels', 'rice vinegar', 'vegetable oil spray', 'coconut', 'ramen soup mix', 'black peppercorns', 
'chiles', 'mint', 'low sodium chicken broth', 'San Marzano tomatoes', 'lemon zest', 'skim milk', 'chili pepper flakes', 'red preserved bean curd', 'ground cinnamon', 'asparagus spears', 'butter', 'rice noodles', 'yellow squash', 'chinese cabbage', 'free-range chickens', 'meat sauce', 'salt water', 'all purpose unbleached flour', 'tri-tip roast', 'hong kong-style noodles', 'broccoli slaw', 'bean curd', 'coconut aminos', 'all potato purpos', 'chillies', 'chilegarlic sauce', 'white peppercorns', 'green chile', 'won ton wrappers', 'udon', 'deep-fried tofu', 'clams', 'jicama', 'beef gravy', 'diced ham', 'plum tomatoes', 'less sodium beef broth', 'orange juice', 'bell pepper', 'whitefish fillets', 'braising beef', 'mo hanh', 'king prawns', 'smoked salmon', 'roast red peppers, drain', 'french fried onions', 'low-sodium fat-free chicken broth', 'kirby cucumbers', 'black sesame seeds', 'tea bags', 'dried udon', 'panko breadcrumbs', 'Tyson Crispy Chicken Strips', 'se']
        self.chinese_food_embeddings = self.model.encode(self.chinese_foods)

    def _clean_ingredient(self, ingredient):
        
        list_bad_words = ['chopped', 'peeled', 'diced', 'minced', 'grated', 'sliced', 'fresh', 'organic']
        for word in list_bad_words:
            ingredient = re.sub(word, ' ', ingredient)
        return ingredient
    
    def _populate_ingredients(self):
        print(self.recipe_ingredients)
        
        for ingredient in self.recipe_ingredients:
            try:
                # Step 1: Split ingredients by commas
                ingredient_list = [i.strip() for i in ingredient.split('\n\n\n') if i.strip()]
                print(f"Ingredient List: {ingredient_list}")  # Debug

                for ingredient in ingredient_list:
                    # Step 2: Clean the ingredient
                    ingredient = self._clean_ingredient(ingredient)
                    print(f"Cleaned Ingredient: {ingredient}")  # Debug

                    # Step 3: Tokenize the ingredient string
                    lst_key_words = ingredient.lower().split()
                    lst_key_words = [word.replace(',', '') for word in lst_key_words]
                    print(f"Tokenized Keywords: {lst_key_words}")  # Debug

                    # Initialize variables for parsing
                    amount_quan_list = []
                    key_word_search = None
                    matched_word = None

                    # Step 4: Search for food keywords in the ingredient string
                    for i in range(len(lst_key_words)):
                        key_word_search = ' '.join(lst_key_words[i:])
                        if key_word_search in self.KBfoods:
                            matched_word = key_word_search
                            amount_quan_list = lst_key_words[:i]
                            for val in key_word_search.split():
                                if val in self.KBmeats:
                                    self.meats.add(val)
                                    break
                            break
                        if lst_key_words[i] in self.KBfoods:
                            if matched_word is None:
                                matched_word = lst_key_words[i]
                                amount_quan_list = lst_key_words[:i]
                            if matched_word in self.KBmeats:
                                self.meats.add(matched_word)
                                break

                    print(f"Matched Word: {matched_word}, Amount/Quantity List: {amount_quan_list}")  # Debug

                    # Step 5: Extract amount, measure type, and ingredient type
                    amount = None
                    measure_type = None
                    ingredient_type = None

                    # Handle amounts and measure types
                    if amount_quan_list:
                        try:
                            # First attempt to parse fractions, then handle whole numbers or text-based quantities
                            amount = str(Fraction(amount_quan_list[0]))  # Convert amount to a fraction
                        except ValueError:
                            # Check if amount is a number or just a descriptor like 'softened'
                            if amount_quan_list[0].isalpha():
                                amount = None
                            else:
                                amount = amount_quan_list[0]  # Fallback to raw value if not parsable

                        # Extract measure type
                        measure_types = ['cup', 'ounce', 'tablespoon', 'teaspoon', 'pound', 'gram', 'liter','cups', 'ounces', 'tablespoons', 'teaspoons', 'pounds', 'grams', 'liters', 'clove', 'cloves', 'pinch', 'pinches', 'quarts', 'quart']
                        for word in amount_quan_list[1:]:
                            if word in measure_types:
                                measure_type = word
                                break

                        # Extract ingredient type (after measure type)
                        if len(amount_quan_list) > 2:
                            ingredient_type = ' '.join(amount_quan_list[2:])

                        
                    
                    print(f"Parsed Details - Amount: {amount}, Measure Type: {measure_type}, Ingredient Type: {ingredient_type}")  # Debug

                    # Step 6: Add the parsed ingredient to the ingredients list
                    if matched_word is not None:
                        ingr = Ingredient(amount, measure_type, matched_word, ingredient_type)
                        self.ingredients.append(ingr)
                        print(f"Added Ingredient: {ingr}")  # Debug

            except Exception as e:
                print(f"Error processing ingredient '{ingredient}': {e}")  # Debug


    def _populate_methods_and_tools(self):
        primary_cooking_methods = {'bake', 'fry', 'roast', 'grill', 'steam', 'poach', 'simmer', 'broil',
                                   'blanch', 'braise', 'stew', 'saute', 'stir-fry', 'stirfry', 'sear', 'boil',
                                   'barbeque', 'baste', 'smoke', 'brine', 'heat', 'whisk'}
        primary_cooking_mapping = {'heat': 'stirfry'}
        secondary_cooking_methods = {'al dente', 'bake', 'barbecue', 'batter', 'beat', 'blend', 'caramelize',
                                     'chop', 'clarify', 'cure', 'deglaze', 'degrease', 'dice', 'dissolve',
                                     'dredge', 'drizzle', 'dust', 'fillet', 'flake', 'flambe', 'fold', 'fricassee',
                                     'garnish', 'glaze', 'grate', 'gratin', 'grind', 'julienne', 'knead', 'marinate',
                                     'meuniere', 'mince', 'mix', 'parboil', 'pare', 'peel', 'pickle', 'pinch', 'pit',
                                     'planked', 'plump', 'poach', 'puree', 'reduce', 'refresh', 'render', 'scald',
                                     'scallop', 'score', 'shred', 'sift', 'skim', 'steep', 'sterilize', 'stir', 'toss',
                                     'truss', 'whip', 'mixture'}
        secondary_cooking_mapping = {'mixture':'mix'}
        primary_tools = {'pan', 'dish', 'board', 'knife', 'spoon', 'fork', 'opener', 'bowl', 'colander', 'peeler','masher',
                         'whisker', 'spinner', 'grater', 'scissors', 'shears', 'juicer', 'press', 'rod',
                         'skillet', 'saucepan', 'pot', 'instapot', 'stockpot', 'spatula', 'tongs', 'ladle', 'mitts',
                         'trivet', 'guard', 'thermometer', 'blender', 'scale', 'container', 'foil', 'paper', 'towels',
                         'towel','sponge', 'rack', 'tray', 'brush', 'oven'}
        for step in self.recipe_steps:
            step_lst = step.lower().split(' ')
            for i in range(len(step_lst)):
                val = step_lst[i]
                val = re.sub(r'[^\w\s]','',val)
                if val in primary_cooking_methods:
                    if val in primary_cooking_mapping:
                        if len(self.primary_methods) == 0:
                            self.primary_methods.add(primary_cooking_mapping[val])
                    else:
                        if len(self.primary_methods) == 0:
                            self.primary_methods.add(val)
                if val in secondary_cooking_methods:
                        if val in secondary_cooking_mapping:
                            self.secondary_methods.add(secondary_cooking_mapping[val])
                        else:
                            self.secondary_methods.add(val)
                if val in primary_tools:
                    self.tools.add(val)
        # [print(i) for i in self.recipe_steps]

    def delete_ingredient(self, ingr):
        new_ingredients = []
        for i in range(len(self.ingredients)):
            if self.ingredients[i] != ingr:
                new_ingredients.append(self.ingredients[i])
        self.ingredients = new_ingredients

    def _get_best_meat_substitute(self, ingredient, vegetarian_substitutes):
        """
        This function finds the best vegetarian substitute by computing cosine similarity
        between the ingredient embedding and each substitute.
        """
        # Get the embedding for the ingredient
        ingredient_embedding = self.model.encode(ingredient, convert_to_tensor=True)
        
        # Get the embeddings for the vegetarian substitutes
        substitute_embeddings = self.model.encode(vegetarian_substitutes, convert_to_tensor=True)
        
        # Compute cosine similarities between the ingredient and all substitutes
        similarities = util.pytorch_cos_sim(ingredient_embedding, substitute_embeddings)[0]
        
        # Find the index of the most similar substitute
        best_substitute_idx = similarities.argmax()
        return vegetarian_substitutes[best_substitute_idx]
    def _clean_dup_step(self, step):
        """
        Clean duplicate words from recipe steps introduced by replacements.
        """
        words = step.split()
        return ' '.join(sorted(set(words), key=words.index))  # Removes duplicates while keeping order

    def transform_to_vegetarian(self):  # REQUIRED
        print('############', [str(ing) for ing in self.ingredients], self.meats)
        print('in transform to veg')

        # Predefined list of vegetarian substitutes
        vegetarian_substitutes = [
                    "tofu",
                    "tempeh",
                    "seitan",
                    "lentils",
                    "chickpeas",
                    "black beans",
                    "mushrooms",
                    "portobello mushrooms",
                    "jackfruit",
                    "cauliflower",
                    "zucchini",
                    "eggplant",
                    "vegetable patties",
                    "quinoa",
                    "soy protein",
                    "vegetable stew",
                    "coconut meat",
                    "pea protein",
                    "vegan cheese",
                    "vegan yogurt",
                    "vegan sausages",
                    "vegan bacon",
                    "almonds",
                    "crispy chickpeas",
                    "tofu scramble",
                    "butternut squash",
                    "soy milk",
                    "oat milk",
                    "rice paper",
                    "vegetable crumbles",
                    "vegan chicken strips",
                    "vegan ground meat",
                    "miso",
                    "lima beans",
                    "sweet potato",
                    "vegan meatballs",
                    "tofu skin",
                    "coconut bacon",
                    "tempeh bacon",
                    "vegetable broth"
                    
                ]

        if len(self.meats) > 0:
            for i in range(len(self.ingredients)):
                # Split the ingredient into words for matching
                search_list = self.ingredients[i].ingr.lower().split(' ')
                
                # Check if any word in the ingredient matches an item in self.meats
                if any(k in self.meats for k in search_list):
                    tmp_ingr = self.ingredients[i].ingr
                    print('-------------- Found meat ingredient:', tmp_ingr)

                    # Get a vegetarian substitute using Sentence-BERT
                    repl = self._get_best_meat_substitute(tmp_ingr, vegetarian_substitutes)
                    if not repl:
                        print("No substitute found for", tmp_ingr)
                        continue  # Skip if no substitute is found
                    
                    # Replace the ingredient with its substitute
                    self.ingredients[i].ingr = repl
                    
                    # Update recipe steps with the substitute
                    for j in range(len(self.recipe_steps)):
                        step = self.recipe_steps[j]
                        
                        # Replace all occurrences of the meat ingredient in the step
                        print(f"## Updating step: {step}")
                        for k in search_list:
                            if k in self.meats:
                                step = re.sub(rf'\b{k}\b', repl, step, flags=re.IGNORECASE)
                        
                        # Handle general phrases related to meat
                        step = re.sub(r' meat\.', f' {repl}.', step, flags=re.IGNORECASE)
                        step = re.sub(r' meat\b', '', step, flags=re.IGNORECASE)
                        step = re.sub(r' no longer pink and', '', step, flags=re.IGNORECASE)
                        step = re.sub(r'skin and bones', 'veggie scraps', step, flags=re.IGNORECASE)
                        step = re.sub(r'bones', repl, step, flags=re.IGNORECASE)
                        step = re.sub(r'skin', repl, step, flags=re.IGNORECASE)
                        step = re.sub(r' fat\b', '', step, flags=re.IGNORECASE)
                        
                        # Clean duplicate words introduced by replacements
                        new_step = self._clean_dup_step(step)
                        self.recipe_steps[j] = new_step
                        print(f"Updated step: {self.recipe_steps[j]}")

            # Clear the meats set after transformation
            self.meats = set()
            return self
        
        else:
            print("ELSE: No meats found to transform.")
            return self

    def _get_nonveg_ingredient(self):
        """
        This function returns a randomly selected non-vegetarian ingredient.
        """
        amount = random.choice([1, 2, 3, 4])
        type_ingr = random.choice(['cups', 'ounces'])
        meat = random.choice([
            'cooked crab', 'pulled pork', 'pan-fried bacon', 'cooked sausages', 'grilled chicken', 
            'fried shrimp', 'prosciutto', 'pan-seared fish'
        ])
        return Ingredient(amount, type_ingr, meat)

    def transform_to_nonvegetarian(self):  # REQUIRED
        # Predefined list of non-vegetarian substitutes
        non_veg_substitutes = [
            'cooked crab', 'pulled pork', 'pan-fried bacon', 'cooked sausages', 'grilled chicken', 
            'fried shrimp', 'prosciutto', 'pan-seared fish', 'beef steak', 'roast lamb', 'turkey breast',
    "jerky",
"primal cut",
"reptile meat",
"wild boar meat",
"turkey meat",
"camel meat",
"smoked meat",

"escalope",
"shawarma",
"minced meat",
"ambelopoulia",

"bison meat",
"meat on the bone",
"elephant meat",
"goat meat",
"kassler",

"quail meat",
'salt-cured meat',
"calf head",
"iguana meat",
"duck meat",


"mutton",
"whale meat",
"kutha meat",
"game",
"jhatka",

"kangaroo meat",

"pse meat",
"white meat",
"veal",
"shank",
"squab",

"salmon",
"beef",
"seal meat",
"confit",
"alligator meat",

"ttavas",
"chicken",
"red meat",
"poultry",
"in vitro meat",
"horse meat",
"canned meat",
"bushmeat",
"raw meat",

"rabbit meat",
"ventresca",
"brisket",

"pork",
"steak frites",
"dried meat",
"pastrami",
"lamb",
"goat",
"chicken",
"steak",
"beef",
"cow",
"shrimp",
"fish",

"pork sausage",
"sausage",
"crab",
"lobster",
"shellfish",
"oysters",
"venison",
"bacon",
"ham",
"salami",
"duck",
"pheasant",
"turkey",
"rabbit",
"boar",
"wild boar",
"ribs",
"sheep",
"goose",
"veal",
"jamon",
"prosciutto",
"lamb chops",
"pork chops",
"lamb loin chops","beef broth", "chicken broth"

]
        

        if len(self.meats) == 0:
            # Get a non-vegetarian ingredient using Sentence-BERT
            ingr = self._get_best_nonveg_ingredient(non_veg_substitutes)
            self.ingredients.append(ingr)
            
            # Get the first ingredient (lhs_ingredient) and append the new non-veg ingredient
            lhs_ingredient = self.ingredients[0].ingr
            repl_string = lhs_ingredient + ' and the ' + ingr.ingr
            
            # Update recipe steps with the new non-veg ingredient
            for j in range(len(self.recipe_steps)):
                self.recipe_steps[j] = re.sub(lhs_ingredient, repl_string, self.recipe_steps[j])
            
            return self
        else:
            return self

    def _get_best_nonveg_ingredient(self, non_veg_substitutes):
        """
        This function finds the best non-vegetarian ingredient by computing cosine similarity
        between the current recipe context and the list of possible non-vegetarian ingredients.
        """
        # Assume the current ingredient list has some context for selection
        context = ' '.join([ingredient.ingr for ingredient in self.ingredients])
        
        # Get the embedding for the context (all ingredients so far)
        context_embedding = self.model.encode(context, convert_to_tensor=True)
        
        # Get the embeddings for the non-vegetarian substitutes
        substitute_embeddings = self.model.encode(non_veg_substitutes, convert_to_tensor=True)
        
        # Compute cosine similarities between the context and all non-veg substitutes
        similarities = util.pytorch_cos_sim(context_embedding, substitute_embeddings)[0]
        
        # Find the index of the most similar non-vegetarian ingredient
        best_substitute_idx = similarities.argmax()
        return Ingredient(random.choice([1, 2, 3, 4]), random.choice(['cups', 'ounces']), non_veg_substitutes[best_substitute_idx])

    def _get_indian_ingredient(self):
        indian_spice = ['tikka-masala', 'garam-masala', 'red-chilli-powder', 'turmeric-powder', 'ginger',
                        'fennel','ajwain', 'tamarind-sauce', 'gooseberry', 'mustard',
                        'curry-powder']

        # if 'soy' in toReplace.split(' '):
        #     return (gen for gen in ['tamarind sauce']+random.shuffle(indian_spice))
        # if 'olive oil' == toReplace:
        #     return (gen for gen in ['ghee']+random.shuffle(indian_spice))
        random.shuffle(indian_spice)
        lst_to_return = ['ghee']+ indian_spice
        # indian_oil = {'ghee'}
        # indian_meat = {'goat', 'lamb', 'chicken'}
        # indian_cream = ['amla milk', 'gopi cream']
        # indian_spice = {'tikka', 'masala', 'milk', 'gopi cream', 'red chilli powder', 'turmeric', 'ginger'}
        return (n for n in lst_to_return)

    

    def float_to_fraction_string(self, value):
        # Handle common fractional values
        fraction_map = {
            0.5: "½",
            0.25: "¼",
            0.75: "¾",
            0.3333333333333333: "⅓",
            0.6666666666666666: "⅔",
            0.125: "⅛",
            0.375: "⅜",
            0.625: "⅝",
            0.875: "⅞"
        }

        if value in fraction_map:
            return fraction_map[value]

        # If not a common fraction, return the value as a regular fraction
        frac = Fraction(value).limit_denominator(100)
        if frac.denominator == 1:
            return str(frac.numerator)  # Just a whole number
        else:
            return f"{frac.numerator}/{frac.denominator}"

    def transform_by_scale_factor(self, factor):
        for ingredient in self.ingredients:
            if ingredient is not None and ingredient.amount is not None:
                try:
                # Attempt to parse the amount as a Fraction
                    amount = str(Fraction(ingredient.amount))
                except ValueError:
                # If parsing fails, handle symbolic fractions like ¼, ½, etc.
                    try:
                        amount = numeric(ingredient.amount)  # Converts symbolic fraction to float
                    except (TypeError, ValueError):
                        print(f"Could not parse amount '{ingredient.amount}'")
                        continue
                scaled_amount = float(Fraction(amount) * factor)
                # Convert the scaled amount back to a cute fractional string
                ingredient.amount = self.float_to_fraction_string(scaled_amount)
        return self


    def transform_to_indian(self):  # REQUIRED
        food_with_cusine_map = KBLoader.get_kaggle_food_with_cusine()
        print('print ingredients that are indian')
        gen = self._get_indian_ingredient()
        for i in range(len(self.ingredients)):
            if self.ingredients[i].ingr in food_with_cusine_map:
                if 'indian' in food_with_cusine_map[self.ingredients[i].ingr]:
                    print('--', self.ingredients[i].ingr)
                else:
                    print('--------- not indian: ', self.ingredients[i].ingr)
                    try:
                        repl = next(gen)
                    except StopIteration:
                        repl = 'ghee'
                    ingredient_to_replace = self.ingredients[i].ingr
                    self.ingredients[i].ingr = repl
                    for j in range(len(self.recipe_steps)):
                        key_search = ingredient_to_replace.split(' ')
                        # print('REPLACE: ', key_search)
                        # for k in range(len(key_search)):
                        self.recipe_steps[j] = re.sub(ingredient_to_replace, repl, self.recipe_steps[j])
                            # break;
                        self.recipe_steps[j] = self._clean_dup_step(self.recipe_steps[j])
        return self

    def transform_to_chinese(self):
        print('Transforming recipe to Chinese cuisine')
        
        # Iterate through the ingredients to find non-Chinese ones
        for i in range(len(self.ingredients)):
            ingredient = self.ingredients[i].ingr.lower()  # Convert to lowercase for matching
            
            # If ingredient is not Chinese, replace it with the most similar Chinese ingredient
            if ingredient not in self.chinese_foods:
                print(f'Ingredient "{self.ingredients[i].ingr}" is not Chinese.')
                
                # Find the most similar Chinese ingredient
                repl = self.get_most_similar_chinese_ingredient(ingredient)
                
                # Replace the ingredient in the recipe
                ingredient_to_replace = self.ingredients[i].ingr
                self.ingredients[i].ingr = repl
                
                # Replace ingredient in recipe steps
                for j in range(len(self.recipe_steps)):
                    self.recipe_steps[j] = re.sub(ingredient_to_replace, repl, self.recipe_steps[j])
                    self.recipe_steps[j] = self._clean_dup_step(self.recipe_steps[j])
                    
        return self

    def get_most_similar_chinese_ingredient(self, non_chinese_ingredient):
        # Encode the non-Chinese ingredient and all Chinese ingredients using Sentence-BERT
        non_chinese_embedding = self.model.encode(non_chinese_ingredient, convert_to_tensor=True)
        chinese_embeddings = self.model.encode(self.chinese_foods, convert_to_tensor=True)
        
        # Compute cosine similarities between the non-Chinese ingredient and all Chinese ingredients
        similarities = util.pytorch_cos_sim(non_chinese_embedding, chinese_embeddings)[0]
        
        # Get the index of the most similar Chinese ingredient
        most_similar_index = similarities.argmax().item()
        
        # Return the most similar Chinese ingredient
        return self.chinese_foods[most_similar_index]
    
    def transform_to_healthy(self):  # REQUIRED

        dic = {frozenset({'chicken','turkey'}):{'meat', 'beef', 'brisket','pork','steak','lamb', 'bacon', 'ham'},
               frozenset({'avocado oil', 'olive oil', 'coconut oil'}):{'vegetable oil', 'canola oil', 'bacon fat', 'peanut oil' , 'lard'},
               frozenset({'maple sugar','substitute low-kcal sugar', 'coconut sugar'}):{'white sugar', 'icing sugar', 'castor sugar'},
               frozenset({'oat flour', 'almond flour', 'whole-wheat flour', 'coconut flour', 'spelt flour'}):{'bread flour', 'all-purpose flour', 'self-raising flour', 'maida'},
               frozenset({'whole-wheat pasta', 'spinach pasta'}):{'pasta'},
               frozenset({'fat-free milk', 'skimmed milk', '2% milk', 'almond milk', 'coconut milk', 'soy milk'}):{'milk'},
               frozenset({'cheese (low-fat)', 'cheese (low-sodium)'}):{'cheese'},
               frozenset({'butter (low-fat)', 'coconut butter', 'unsalted butter', 'butter (dairy-free)'}):{'butter' , 'lard'},
               frozenset({'light cream'}):{'heavy cream'}
                        }
        applied_new = {''}
        for ing in self.ingredients:
            for key,val in dic.items():
                for inx in val:
                    if re.search(inx, ing.ingr):
                        new_ingr_sel = random.sample(key,1)[0]
                        new_ingr = re.sub(inx,new_ingr_sel,ing.ingr)
                        print("----------Changing ingredient " + ing.ingr + " with " + new_ingr)
                        ing.ingr = new_ingr
                        if new_ingr_sel == 'chicken' or new_ingr_sel == 'turkey':
                            self.meats = {new_ingr_sel}
                        # if new_ingr_sel+inx in applied_new:
                        #     continue

                        split_list = list([inx]+ [inx.split()[-1]])
                        # print (split_list)
                        for chunk in split_list:
                            if chunk not in applied_new and any(re.search(chunk,step) for step in self.recipe_steps):
                                print (applied_new)
                                self.recipe_steps = [re.sub(chunk,new_ingr_sel,step) for step in self.recipe_steps]
                                applied_new.add(chunk)
                                break

                        break
        # for ing in self.ingredients:
        #     print(ing)
        return self

    def _get_unhealthy_ingredient(self):
        amount = random.choice([1,2,3,4])
        type_ingr = random.choice(['cups', 'ounces'])
        meat = random.choice(['pan-fried bacon','cooked sausages', 'bacon-bits'])
        amount_f = random.choice([1,2,3,4])
        type_ingr_f = random.choice(['cups', 'ounces'])
        fat = random.choice(['butter', 'bacon fat', 'lard'])
        return Ingredient(amount, type_ingr, meat),Ingredient(amount_f, type_ingr_f,fat)

    def transform_to_unhealthy(self):
        dic = {
               frozenset({'vegetable oil', 'canola oil'}):{'avocado oil', 'olive oil', 'coconut oil'},
               frozenset({'white sugar', 'castor sugar'}):{'substitute low-kcal sugar', 'coconut sugar', 'honey', 'maple sugar'},
               frozenset({'bread flour', 'all-purpose flour', 'self-raising flour', 'maida'}):{'oat flour', 'almond flour', 'whole-wheat flour', 'coconut flour', 'spelt flour'},
               frozenset({'pasta'}):{'whole-wheat pasta', 'spinach pasta'},
               frozenset({'full-fat milk'}):{'fat-free milk', 'skimmed milk', '2% milk', 'almond milk', 'coconut milk', 'soy milk', 'milk'},
               frozenset({'full-fat cheese'}):{'cheese (low-fat)', 'cashew cheese', 'cheese (low-sodium)', 'low-sodium cheese', 'low-fat cheese', 'cheese'},
               frozenset({'whole butter','lard'}):{'butter (low-fat)', 'coconut butter', 'unsalted butter', 'butter (dairy-free)'}
               }
        applied_new = {''}
        for ing in self.ingredients:
            for key,val in dic.items():
                for inx in val:
                    if re.search(inx, ing.ingr):
                        new_ingr_sel = random.sample(key,1)[0]
                        new_ingr = re.sub(inx,new_ingr_sel,ing.ingr)
                        print("----------Changing ingredient " + ing.ingr + " with " + new_ingr)
                        ing.ingr = new_ingr
                        # if new_ingr_sel+inx in applied_new:
                        #     continue

                        split_list = list([inx]+ [inx.split()[-1]])
                        # print (split_list)
                        for chunk in split_list:
                            if chunk not in applied_new and any(re.search(chunk,step) for step in self.recipe_steps):
                                print (applied_new)
                                self.recipe_steps = [re.sub(chunk,new_ingr_sel,step) for step in self.recipe_steps]
                                applied_new.add(chunk)
                                break

                        break
        ingr, _ = self._get_unhealthy_ingredient()

        if len(self.meats) == 0:
            self.ingredients.append(ingr)
            lhs_ingredient = self.ingredients[0].ingr
            repl_string = lhs_ingredient + ', ' + ingr.ingr
            print ("Adding in some:", ingr.ingr)
            for j in range(len(self.recipe_steps)):
                for strn in list([lhs_ingredient] + [lhs_ingredient.split()[-1]]):
                    self.recipe_steps[j], n_rep = re.subn(strn, repl_string, self.recipe_steps[j])
                    if n_rep > 0:
                        break

        i = 0
        q = False
        db = False

        from fractions import Fraction
        while q != True:
            _, fat = self._get_unhealthy_ingredient()
            for j,ing in enumerate(self.ingredients):
                if ing.ingr != fat.ingr:
                    q=True
                else:
                    q=False
                    if db != True:
                        self.ingredients[j].amount = float(sum(Fraction(s) for s in self.ingredients[j].amount.split()))*2
                        print ("Doubling amount of ", ing.ingr)
                        db = True
                    break
            i += 1
            if i == 7 and q != True:
                fat = None
                q = True


        if fat != None:
            self.ingredients.append(fat)

            lhs_ingredient = self.ingredients[0].ingr
            repl_string = lhs_ingredient + ', ' + fat.ingr
            print ("Adding in some:", fat.ingr)
            for j in range(len(self.recipe_steps)):
                for strn in list([lhs_ingredient] + [lhs_ingredient.split()[-1]]):
                    self.recipe_steps[j], n_rep = re.subn(strn, repl_string, self.recipe_steps[j])
                    if n_rep > 0:
                        break

        # for ing in self.ingredients:
        #     print(ing)
        # print("----------------------------------------------- Method Ends Here -----------------------------------------------")
        return self

    def transform_to_stirfry(self):  # OPTIONAL
        random.seed(10)
        liquid = ''
        method = ['stir-fry', 'cook']
        cook = random.choice(method)
        for i in self.recipe_ingredients:
            if re.match(".*oil.*", i):
                liquid = 'with oil as required'
                break;
            if re.match(".*butter.*", i):
                liquid = 'with butter as required'
                break;
            if re.match(".*ghee.*", i):
                liquid = 'with ghee as required'
                break;
        change_cooking = dict([
            (
                "place the (aluminum roasting pan|aluminium pan|roasting pan|pan|baking dish) on the (grill's grate|grills grate|grill grate|grill|grate|oven)",
                "place the pan on the stovetop"),
            ("place the pan on the .* grill .* grate", "place the pan on the stovetop"),
            ("in a pot style grill.* the bottom of grill", ""),
            ("in a lightly greased .* baking dish", "in a lightly greased skillet"),
            ("in a greased .* baking dish", "in a greased skillet"),
            ("line a baking sheet with aluminum foil", ""),
            ("prepare an outdoor grill with coals about [0-9] inches from the grate", "preheat the skillet " + liquid),
            ("preheat.*oven to (300|[0-2][0-9]?[0-9]?) degree(s|) f.*c[/)]",
             "preheat the skillet " + liquid + "  in low heat"),
            ("preheat.*oven to (400|[3][0-9][0-9]) degree(s|) f.*c[/)]",
             "preheat the skillet " + liquid + "  in medium heat"),
            ("preheat.*oven to ([4-9][0-9][0-9]) degree(s|) f.*c[/)]",
             "preheat the skillet " + liquid + " in high heat"),
            ("(preheat|heat).*oven to (300|[0-2][0-9]?[0-9]?) degree(s|).",
             "preheat the skillet " + liquid + "  in low heat"),
            ("(preheat|heat).*oven to (400|[3][0-9][0-9]) degree(s|).",
             "preheat the skillet " + liquid + "  in medium heat"),
            ("(preheat|heat).*oven to ([4-9][0-9][0-9]) degree(s|).",
             "preheat the skillet " + liquid + "  in high heat"),
            ("preheat your oven's broiler", "preheat the skillet " + liquid + " "),
            ("reduce heat to ([0-9][0-9][0-9]) degree(s|) f [/(]([0-9][0-9][0-9]) degree(s|) c[/)]", "reduce heat"),
            ("reduce heat to ([0-9][0-9][0-9]) degree(s|)", "reduce heat"),
            ("increase heat to ([0-9][0-9][0-9]) degree(s|) f [/(]([0-9][0-9][0-9]) degree(s|) c[/)]", "increase heat"),
            ("increase heat to ([0-9][0-9][0-9]) degree(s|)", "increase heat"),
            ("preheat.*grill.*medium-low heat", "preheat the skillet " + liquid + "  in medium-low heat"),
            ("preheat.*grill.*low-medium heat", "preheat the skillet " + liquid + "  in low-medium heat"),
            ("preheat.*grill.*medium-high heat", "preheat the skillet " + liquid + "  in medium-high heat"),
            ("preheat.*grill.*high-medium heat", "preheat the skillet " + liquid + "  in high-medium heat"),
            ("preheat.*grill.*medium heat", "preheat the skillet " + liquid + "  in medium heat"),
            ("preheat.*grill.*low heat", "preheat the skillet " + liquid + "  in low heat"),
            ("preheat.*grill.*high heat", "preheat the skillet " + liquid + "  in high heat"),
            ("place (on|in)( the|) (top|middle|center)( oven|) rack", "place on stove"),
            ("(lightly|) grease.*baking dish", " "),
            (
                "((and |)lightly oil the grill grate|(and |)lightly oil grill grate|(and |)lightly oil the grate|(and |)lightly oil grate|(and |)lightly oil the grill|(and |)lightly oil grill)",
                " "),
            ("grease a broiling pan or line pan with aluminum foil", ""),
            ("with (foil|aluminum foil)", "with lid"),
            ("remove (foil|aluminum foil)", "remove lid"),
            ("preheat oven.*c[/)][/.]", ' '),
            ("grease.*baking pan[., ]", " "),
            ("preheat.*grill.*heat[., ]", " "),
            ("cover the grill with the lid and open the vents.", ' '),
            ("[0-9](-| )quart", ""),
            ("adjust oven rack to lowest position", ""),
            ("[0-9](-| )inch(es|) from coal(s|)", ''),
            ("(outdoor|charcoals|charcoal)", ""),
            ("(preheated oven|preheated grill grate|preheated grill)", "preheated skillet"),
            (
                '([0-9](-| )inch round baking dish|[0-9][0-9]?x[0-9][0-9]?(-| )inch baking dish|round baking dish|baking dish|baking sheet)',
                'skillet'),
            ("(grilled|baked|roasted|broiled|barbequed|smoked)", "stir-fried"),
            ("(grilling|baking|roasting|broiling|barbequing|smoking)", "cooking"),
            ("(deep-fryer|slow cooker)", "skillet"),
            ("(grill the|^grill|[/.] grill|[/.]  grill|broil[., ]|bake|barbeque|smoke)", " " + cook),
            ("(grill's grate|grill grate|grate|grill)", "skillet"),
            ("large skillet or dutch oven", "large skillet"),
            ('oven', 'stove')
        ])
        for r in range(len(self.recipe_steps)):
            cook = random.choice(method)
            for i, j in change_cooking.items():
                self.recipe_steps[r] = re.sub(i, j, self.recipe_steps[r])
        self.tools = set()
        self.primary_methods = set()
        self.secondary_methods = set()
        self._populate_methods_and_tools()

        if len(self.primary_methods) == 0:
            self.primary_methods = {'stir-fry'}

        return self

    def pretty_print_ingredients(self):
        for ingr in self.ingredients:
            val_string = ''
            if ingr.amount is not None:
                val_string = val_string + str(ingr.amount)
            # self.measure_type = measure_type
            # self.ingredient_type = ingredient_type
            if ingr.measure_type is not None:
                val_string = val_string +' '+str(ingr.measure_type)
            if ingr.ingredient_type is not None:
                val_string = val_string +' '+str(ingr.ingredient_type)
            if ingr.ingr is not None:
                val_string = val_string +' '+str(ingr.ingr)
            print(val_string)

    def __str__(self):
        print('==== ORIGINAL INGREDIENTS ====')
        [print(ingr) for ingr in self.recipe_ingredients]
        # for step in self.recipe_ingredients:
        #     for segment in step.split(".\n"):
        #         segment = segment.strip(" ")
        #         print("•", segment, "\n")
        print(' ')
        print('==== PARSED INGREDIENTS: ====')
        [print(ingr) if ingr is not None else print('') for ingr in self.ingredients]
        print(' ')
        print('==== CONVERTED RECIPE INGREDIENTS ====')
        self.pretty_print_ingredients()
        print(' ')
        print('==== STEPS ====')
        for step in self.recipe_steps:
            for segment in step.split("."):
                segment = segment.strip(" ")
                print("•", segment, "\n")
        # [print("segment") for segment in step.split(",") for step in self.recipe_steps]
        print(' ')
        print('==> PRIMARY_COOKING_METHOD: {}'.format(self.print_list(list(self.primary_methods))))

        print('==> SECONDARY_COOKING_METHOD: {}'.format(self.print_list([m for m in self.secondary_methods])))
        print('==> TOOLS: {}'.format(self.print_list([m for m in self.tools])))
        return ''
    def print_list(self, lst):
        return ', '.join(lst)
        # print(lst)
        # print(len(lst))
        # returnstr = ''
        # for i in range(len(lst)):
        #     print('i:',i)
        #     print(lst[i])
        #
        #     if i < len(lst):
        #         returnstr = returnstr + ' ' + lst[i] + ','
        #     else:
        #         returnstr = returnstr + ' ' + lst[i]
        # return returnstr
def main():
    pass
    #Recipe()


if __name__ == "__main__":
    main()
