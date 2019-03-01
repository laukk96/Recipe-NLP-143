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
        self.meats = []
        self.tools = []
        self.steps = []
        self.KBfoods = KBLoader.get_kaggle_foods()
        self.KBfoodscusine = KBLoader.get_kaggle_food_with_cusine()
        self.KBmeats = KBLoader.get_all_meats()
        self._populate_ingredients()

    def _populate_ingredients(self):
        for ingredient in self.recipe_ingredients:
            ingredient = ingredient.split(',')[0]
            ingredient = re.sub(' \(.*\)', '', ingredient)
            lst_key_words = ingredient.lower().split(' ')
            amount_quan_list = []
            key_word_search = None
            for i in range(len(lst_key_words)):
                key_word_search = ' '.join(lst_key_words[i:len(lst_key_words)])
                if key_word_search in self.KBfoods:
                    amount_quan_list = lst_key_words[0:i]
                    for val in key_word_search.split(' '):
                        if val in self.KBmeats:
                            self.meats.append(val)
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

    def transform_to_vegetarian(self):  # REQUIRED
        pass

    def transform_to_nonvegetarian(self):  # REQUIRED
        pass

    def transform_to_indian(self):  # REQUIRED
        pass

    def transform_to_chinese(self):  # OPTIONAL
        pass

    def transform_to_healthy(self):  # REQUIRED
        pass

    def transform_to_stirfry(self):  # REQUIRED
        pass

    def __str__(self):
        print('INGREDIENTS:')
        [print(ingr) for ingr in self.ingredients]
        print('STEPS:')
        [print(step) for step in self.steps]
        return ''

def main():
    pass
    # Recipe()


if __name__ == "__main__":
    main()
