import random
import re
from unicodedata import numeric
from fractions import Fraction
import KBLoader
import string

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

    def _get_meat_substitute(self, name):
        meat_dict = {
            'lamb':['tofu', 'tempeh', 'seitan'],
            'chicken': ['potatoes', 'tempeh', 'jackfruit'],
            'goat': ['jackfruit', 'tempeh', 'seitan'],
            'pork': ['tofu', 'tempeh', 'seitan'],
            'meat': ['tofu', 'tempeh', 'seitan'],
            'buffalo': ['tofu', 'tempeh', 'seitan'],
            'salmon': ['seitan', 'tempeh'],
            'beef': ['seitan', 'tempeh', 'jackfruit'],
            'shrimp': ['tofu','jackfruit'],
            'sausage': ['tofu','seitan', 'potatoes']
        }
        for val in name.split(' '):
            if val in meat_dict:
                return random.choice(meat_dict[val])
            else:
                return random.choice(['tofu','seitan', 'potatoes'])
    def _clean_dup_step(self,step):
        filtered_list = []
        search = step.split(' ')
        for i in range(len(search)-1):
            lhs = search[i]
            rhs = search[i+1]
            search_vallhs = re.sub(r'[^\w\s]', '', lhs)
            search_valrhs = re.sub(r'[^\w\s]', '', rhs)
            if search_vallhs != search_valrhs:
                filtered_list.append(lhs)
        if re.sub(r'[^\w\s]', '', filtered_list[-1]) != re.sub(r'[^\w\s]', '', search[-1]):
            filtered_list.append(search[-1])
        return ' '.join(filtered_list)

    def transform_to_vegetarian(self):  # REQUIRED
        print('############', [str(ing) for ing in self.ingredients], self.meats)
        print('in transform to veg')
        
        if len(self.meats) > 0:
            for i in range(len(self.ingredients)):
                # Split the ingredient into words for matching
                search_list = self.ingredients[i].ingr.lower().split(' ')
                
                # Check if any word in the ingredient matches an item in self.meats
                if any(k in self.meats for k in search_list):
                    tmp_ingr = self.ingredients[i].ingr
                    print('-------------- Found meat ingredient:', tmp_ingr)
                    
                    # Get a vegetarian substitute
                    repl = self._get_meat_substitute(tmp_ingr)
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
        amount = random.choice([1,2,3,4])
        type_ingr = random.choice(['cups', 'ounces'])
        meat = random.choice(['cooked crab','pulled pork', 'pan-fried bacon', 'cooked sausages', 'grilled chicken', 'fried shrimp',
                              'prosciutto', 'pan-seared fish'])
        return Ingredient(amount, type_ingr, meat)

    def transform_to_nonvegetarian(self):  # REQUIRED
        if len(self.meats) == 0:
            ingr = self._get_nonveg_ingredient()
            self.ingredients.append(ingr)
            lhs_ingredient = self.ingredients[0].ingr
            repl_string = lhs_ingredient + ' and the ' + ingr.ingr
            for j in range(len(self.recipe_steps)):
                self.recipe_steps[j] = re.sub(lhs_ingredient, repl_string, self.recipe_steps[j])
            return self
        else:
            return self

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

    def _get_chinese_ingredient(self):
        chinese_spice = ['red sichuan peppercorn', 'green sichuan peppercorn', 'five spice powder', 'duce sauce', 'oyster sauce', 'hoisin sauce', 'black bean and garlic sauce','xo sauce','sweet and saur sauce', 'soy sauce', 'chinese black vinegar', 'sesame oil', 'rice wine']
        random.shuffle(chinese_spice)
        lst_to_return = ['douchi']+ chinese_spice
        #return random.choice(chinese_spice)
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

    def transform_to_chinese(self):  # optional
        food_with_cusine_map = KBLoader.get_kaggle_food_with_cusine()
        print('print ingredients that are Chinese')
        gen = self._get_chinese_ingredient()
        for i in range(len(self.ingredients)):
            if self.ingredients[i].ingr in food_with_cusine_map:
                if 'chinese' in food_with_cusine_map[self.ingredients[i].ingr]:
                    print('--', self.ingredients[i].ingr)
                else:
                    print('--------- not Chinese: ', self.ingredients[i].ingr)
                    try:
                        repl = next(gen)
                    except StopIteration:
                        repl = 'douchi'
                    ingredient_to_replace = self.ingredients[i].ingr
                    self.ingredients[i].ingr = repl
                    for j in range(len(self.recipe_steps)):
                        key_search = ingredient_to_replace.split(' ')
                        #print('REPLACE: ', key_search)
                        # for k in range(len(key_search)):
                        self.recipe_steps[j] = re.sub(ingredient_to_replace, repl, self.recipe_steps[j])
                            # break;
                        self.recipe_steps[j] = self._clean_dup_step(self.recipe_steps[j])
        return self 
    
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
