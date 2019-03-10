import random
import re

# import KBLoader
import KBLoader


# import KBLoader


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
        list_bad_words = [' chopped, ', ' skinless, ']
        for word in list_bad_words:
            ingredient = re.sub(word, ' ', ingredient)
        return ingredient
    def _populate_ingredients(self):
        for ingredient in self.recipe_ingredients:
            # print('INGREDIENT: {}'.format(ingredient))
            ingredient = self._clean_ingredient(ingredient)
            # print(ingredient)
            tmp_ingredients = ingredient.split(',')
            if len(tmp_ingredients) > 1:
                if len(ingredient.split(',')[1].strip().split(' ')) < len(ingredient.split(',')[0].strip().split(' ')):
                    ingredient = ingredient.split(',')[0]
                else:
                    pass
                    # print('fails this condition',ingredient)
                    # print(ingredient)
                    # print(ingredient.split(',')[1].split(' '))
                    # print(ingredient.split(',')[0].strip().split(' '))
            else:
                ingredient = ingredient.split(',')[0]
            ingredient = re.sub(' \(.*\)', '', ingredient)
            ingredient = re.sub(',', '', ingredient)
            lst_key_words = ingredient.lower().split(' ')
            # print(lst_key_words)
            # print('-----keyword search list: {}'.format(lst_key_words))
            amount_quan_list = []
            key_word_search = None
            matched_word = None
            for i in range(len(lst_key_words)):
                key_word_search = ' '.join(lst_key_words[i:len(lst_key_words)])
                list_of_matches = []  # This is to match with the longest phrase in the list.'

                if key_word_search in self.KBfoods:
                    matched_word = key_word_search
                    amount_quan_list = lst_key_words[0:i]
                    # print('-KEYWORDSEARCH: {}'.format(key_word_search))
                    for val in key_word_search.split(' '):
                        if val in self.KBmeats:
                            # print('-------------------------meats matched: {}'.format(val))
                            self.meats.add(val)
                            break

                    break
                if lst_key_words[i] in self.KBfoods:
                    if matched_word == None:
                        matched_word = lst_key_words[i]
                        amount_quan_list = lst_key_words[0:i]
                    if matched_word in self.KBmeats:
                        # print('-------------------------meats matched: {}'.format(matched_word))
                        self.meats.add(matched_word)
                        break

            amount = None
            measure_type = None
            ingredient_type = None

            # print('------{}'.format(amount_quan_list))
            if len(amount_quan_list) !=0:
                amount = amount_quan_list[0]
                if len(amount_quan_list) > 2:
                    ingredient_type = ' '.join(amount_quan_list[1:])
                else:
                    if len(amount_quan_list) > 1:
                        measure_type = amount_quan_list[1]

            # print('Amount: {}'.format(amount))
            # print('measure_type: {}'.format(measure_type))
            # print('ingredient_type: {}'.format(ingredient_type))
            # print('matched_word: {}'.format(key_word_search))

            if matched_word is not None:
                ingr = Ingredient(amount, measure_type, matched_word, ingredient_type)
                self.ingredients.append(ingr)
        print('MEATS FOUND: {}'.format(self.meats))

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
                val = re.sub('[^\w\s]','',val)
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
            search_vallhs = re.sub('[^\w\s]', '', lhs)
            search_valrhs = re.sub('[^\w\s]', '', rhs)
            if search_vallhs != search_valrhs:
                filtered_list.append(lhs)
        if re.sub('[^\w\s]', '', filtered_list[-1]) != re.sub('[^\w\s]', '', search[-1]):
            filtered_list.append(search[-1])
        return ' '.join(filtered_list)

    def transform_to_vegetarian(self):  # REQUIRED
        if len(self.meats) > 0:
            for i in range(len(self.ingredients)):
                search_list = self.ingredients[i].ingr.split(' ')
                if any(k in self.meats for k in search_list):
                    tmp_ingr = self.ingredients[i].ingr
                    print('--------------',tmp_ingr)
                    repl = self._get_meat_substitute(tmp_ingr)
                    self.ingredients[i].ingr = repl
                    for j in range(len(self.recipe_steps)):
                        look_up_phrase = tmp_ingr.split(' ')
                        matched_word = None
                        for u in range(len(look_up_phrase)):
                            key_word_search = ' '.join(look_up_phrase[u:len(look_up_phrase)])
                            print('##keywordsearch: ',key_word_search)
                            self.recipe_steps[j] = re.sub(key_word_search, repl, self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub(' meat\.', ' '+repl+'.', self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub(' meat','',self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub(' no longer pink and', '',self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub('skin and bones', 'veggie scraps', self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub(look_up_phrase[u], repl , self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub('bones', repl , self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub('skin', repl , self.recipe_steps[j])
                            self.recipe_steps[j] = re.sub(' fat', '', self.recipe_steps[j])
                        new_step = self._clean_dup_step(self.recipe_steps[j])
                        self.recipe_steps[j] = new_step
                            # break;
            self.meats = set()
            return self
        else:
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
        indian_spice = ['tikka-masala', 'garam-masala', 'gopi-cream', 'red-chilli-powder', 'turmeric-powder', 'ginger',
                        'fennel','ajwain', 'tamarind-sauce', 'basil', 'gooseberry', 'mustard',
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
                        print('REPLACE: ', key_search)
                        # for k in range(len(key_search)):
                        self.recipe_steps[j] = re.sub(ingredient_to_replace, repl, self.recipe_steps[j])
                            # break;
                        self.recipe_steps[j] = self._clean_dup_step(self.recipe_steps[j])
        return self

    def transform_to_chinese(self):  # OPTIONAL
        pass

    def transform_to_healthy(self):  # REQUIRED

        dic = {frozenset({'chicken','turkey'}):{'meat', 'beef', 'brisket','pork','steak','lamb'},
               frozenset({'avocado oil', 'olive oil', 'coconut oil'}):{'vegetable oil', 'canola oil'},
               frozenset({'maple sugar','substitute low-kcal sugar', 'coconut sugar'}):{'white sugar', 'icing sugar', 'castor sugar'},
               frozenset({'oat flour', 'almond flour', 'whole-wheat flour', 'coconut flour', 'spelt flour'}):{'bread flour', 'all-purpose flour', 'self-raising flour', 'maida'},
               frozenset({'whole-wheat pasta', 'spinach pasta'}):{'pasta'},
               frozenset({'fat-free milk', 'skimmed milk', '2% milk', 'almond milk', 'coconut milk', 'soy milk'}):{'milk'},
               frozenset({'cheese (low-fat)', 'cheese (low-sodium)'}):{'cheese'},
               frozenset({'butter (low-fat)', 'coconut butter', 'unsalted butter', 'butter (dairy-free)'}):{'butter'},
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
        for ing in self.ingredients:
            print(ing)
        print("----------------------------------------------- Method Ends Here -----------------------------------------------")
        return self

    def transform_to_unhealthy(self):
        dic = {
               frozenset({'vegetable oil', 'canola oil'}):{'avocado oil', 'olive oil', 'coconut oil'},
               frozenset({'white sugar', 'icing sugar', 'castor sugar'}):{'substitute low-kcal sugar', 'coconut sugar', 'honey', 'maple sugar'},
               frozenset({'bread flour', 'all-purpose flour', 'self-raising flour', 'maida'}):{'oat flour', 'almond flour', 'whole-wheat flour', 'coconut flour', 'spelt flour'},
               frozenset({'pasta'}):{'whole-wheat pasta', 'spinach pasta'},
                frozenset({'full-fat milk', 'milk'}):{'fat-free milk', 'skimmed milk', '2% milk', 'almond milk', 'coconut milk', 'soy milk'},
                frozenset({'cheese'}):{'cheese (low-fat)', 'cashew cheese', 'cheese (low-sodium)', 'low-sodium cheese', 'low-fat cheese'},
                frozenset({'butter'}):{'butter (low-fat)', 'coconut butter', 'unsalted butter', 'butter (dairy-free)'}
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
        for ing in self.ingredients:
            print(ing)
        print("----------------------------------------------- Method Ends Here -----------------------------------------------")
        return self

    def transform_to_stirfry(self):  # OPTIONAL
        pass

    def __str__(self):
        print('ACTUAL INGREDIENTS')
        [print(ingr) for ingr in self.recipe_ingredients]
        print('INGREDIENTS:')
        [print(ingr) for ingr in self.ingredients]
        print('STEPS:')
        [print(step) for step in self.recipe_steps]
        print('PRIMARY_COOKING_METHOD: {}'.format(self.primary_methods))
        print('SECONDARY_COOKING_METHOD: {}'.format([m for m in self.secondary_methods]))
        print('TOOLS: {}'.format([m for m in self.tools]))
        return ''

def main():
    pass
    # Recipe()


if __name__ == "__main__":
    main()
