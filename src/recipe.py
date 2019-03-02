import random
import re

from src import KBLoader


class Ingredient:
    def __init__(self, amount, measure_type, ingr, ingredient_type=None):
        self.amount = amount
        self.measure_type = measure_type
        self.ingredient_type = ingredient_type
        self.ingr = ingr

    def __str__(self):
        if self.ingredient_type != None:
            return self.amount + ' ' + self.measure_type + ' ' + self.ingredient_type + ' ' + self.ingr
        else:
            return self.amount + ' ' + self.measure_type + ' ' + self.ingr

        # print('------------------------')
        # print('ingredient_type: {}'.format(self.ingredient_type))
        # print('ingredient: {}'.format(self.ingr))
        # print('amount: {}'.format(self.amount))
        # print('measure_type: {}'.format(self.measure_type))
        # print('------------------------#')
        # return ''





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

    def _populate_ingredients(self):
        # print(self.recipe_ingredients)
        for ingredient in self.recipe_ingredients:
            ingredient = ingredient.split(',')[0]
            ingredient = re.sub(' \(.*\)', '', ingredient)
            lst_key_words = ingredient.lower().split(' ')
            amount_quan_list = []
            key_word_search = None
            for i in range(len(lst_key_words)):
                key_word_search = ' '.join(lst_key_words[i:len(lst_key_words)])
                # print('####{}'.format(key_word_search))
                if key_word_search in self.KBfoods:
                    amount_quan_list = lst_key_words[0:i]
                    for val in key_word_search.split(' '):
                        if val in self.KBmeats:
                            self.meats.add(val)
                            break
                    break
            amount = None
            measure_type = None
            ingredient_type = None
            if len(amount_quan_list) > 1:
                amount = amount_quan_list[0]
                measure_type = amount_quan_list[1]
            if len(amount_quan_list) > 2:
                ingredient_type = ' '.join(amount_quan_list[1:])
            ingr = Ingredient(amount, measure_type, key_word_search, ingredient_type)
            self.ingredients.append(ingr)

    def _populate_methods_and_tools(self):
        primary_cooking_methods = {'bake', 'fry', 'roast', 'grill', 'steam', 'poach', 'simmer', 'broil',
                                   'blanch', 'braise', 'stew', 'saute', 'stir-fry', 'stirfry', 'sear', 'boil',
                                   'barbeque', 'baste', 'smoke', 'brine', 'heat'}
        secondary_cooking_methods = {'al dente', 'bake', 'barbecue', 'batter', 'beat', 'blend', 'caramelize',
                                     'chop', 'clarify', 'cream', 'cure', 'deglaze', 'degrease', 'dice', 'dissolve',
                                     'dredge', 'drizzle', 'dust', 'fillet', 'flake', 'flambe', 'fold', 'fricassee',
                                     'garnish', 'glaze', 'grate', 'gratin', 'grind', 'julienne', 'knead', 'marinate',
                                     'meuniere', 'mince', 'mix', 'parboil', 'pare', 'peel', 'pickle', 'pinch', 'pit',
                                     'planked', 'plump', 'poach', 'puree', 'reduce', 'refresh', 'render', 'scald',
                                     'scallop', 'score', 'shred', 'sift', 'skim', 'steep', 'sterilize', 'stir', 'toss',
                                     'truss', 'whip'}
        primary_tools = {'pan', 'dish', 'board', 'knife', 'spoon', 'fork', 'opener', 'bowl', 'colander', 'peeler'
                                                                                                         'masher',
                         'whisker', 'spinner', 'grater', 'scissors', 'shears', 'juicer', 'press', 'rod',
                         'skillet', 'saucepan', 'pot', 'instapot', 'stockpot', 'spatula', 'tongs', 'ladle', 'mitts',
                         'trivet', 'guard', 'thermometer', 'blender', 'scale', 'container', 'foil', 'paper', 'towels',
                         'towel',
                         'sponge', 'rack', 'tray'}
        for step in self.recipe_steps:
            step_lst = step.lower().split(' ')
            for i in range(len(step_lst)):
                val = step_lst[i]
                if val in primary_cooking_methods:
                    self.primary_methods.add(val)
                if val in secondary_cooking_methods:
                    self.secondary_methods.add(val)
                if val in primary_cooking_methods:
                    self.tools.add(val)
        [print(i) for i in self.recipe_steps]

    def delete_ingredient(self, ingr):
        new_ingredients = []
        for i in range(len(self.ingredients)):
            if self.ingredients[i] != ingr:
                new_ingredients.append(self.ingredients[i])
        self.ingredients = new_ingredients

    def transform_to_vegetarian(self):  # REQUIRED
        if len(self.meats) > 0:
            for i in range(len(self.ingredients)):
                search_list = self.ingredients[i].ingr.split(' ')
                if any(i in self.meats for i in search_list):
                    tmp_ingr = self.ingredients[i].ingr
                    self.ingredients[i].ingr = 'potato'
                    for j in range(len(self.recipe_steps)):
                        for val in tmp_ingr.split(' '):
                            self.recipe_steps[j] = re.sub(val, 'potato', self.recipe_steps[j])
            self.meats = set()
            return self
        else:
            return self

    def transform_to_nonvegetarian(self):  # REQUIRED
        if len(self.meats) == 0:
            self.ingredients.append(Ingredient('3', 'cups', 'shrimp'))
            lhs_ingredient = self.ingredients[0].ingr
            repl_string = lhs_ingredient + ' and the ' + 'shrimp '
            for j in range(len(self.recipe_steps)):
                self.recipe_steps[j] = re.sub(lhs_ingredient, repl_string, self.recipe_steps[j])
            return self
        else:
            return self

    def _get_indian_ingredient(self):
        indian_spice = ['tikka', 'masala', 'yogurt', 'milk', 'gopi cream', 'red chilli powder', 'turmeric']
        return random.choice(indian_spice)

    def transform_to_indian(self):  # REQUIRED
        food_with_cusine_map = KBLoader.get_kaggle_food_with_cusine()

        print('print ingredients that are indian')
        for i in range(len(self.ingredients)):
            if self.ingredients[i].ingr in food_with_cusine_map:
                if 'indian' in food_with_cusine_map[self.ingredients[i].ingr]:
                    print('--', self.ingredients[i].ingr)
                else:
                    print('--------- not indian: ', self.ingredients[i].ingr)
                    ingredient_to_replace = self.ingredients[i].ingr
                    self.delete_ingredient(ingredient_to_replace)
                    for j in range(len(self.recipe_steps)):
                        self.recipe_steps[j] = re.sub(ingredient_to_replace, self._get_indian_ingredient(),
                                                      self.recipe_steps[j])

        return self

    def transform_to_chinese(self):  # OPTIONAL
        pass

    def transform_to_healthy(self):  # REQUIRED
        #healthy
        pass

    def transform_to_stirfry(self):  # OPTIONAL
        pass

    def __str__(self):
        print('INGREDIENTS:')
        [print(ingr) for ingr in self.ingredients]
        print('STEPS:')
        [print(step) for step in self.recipe_steps]
        print('PRIMARY_COOKING_METHOD: ')
        [print(m) for m in self.primary_methods]
        print('SECONDARY_COOKING_METHOD: ')
        [print(m) for m in self.secondary_methods]
        print('TOOLS: ')
        [print(m) for m in self.tools]
        # sub's psh
        return ''

def main():
    pass
    # Recipe()


if __name__ == "__main__":
    main()
