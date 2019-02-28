from src import KBLoader

class Recipe:
    def __init__(self, ingredients, steps):
        print('I am a recipe')
        self.recipe_ingredients = ingredients
        self.recipe_steps = steps
        self.ingredients = []
        self.tools = []
        self.methods = []
        self.KBfoods = KBLoader.get_kaggle_foods()
        self.KBfoodscusine = KBLoader.get_kaggle_food_with_cusine()
        self.populate_fields()

    def populate_fields(self):
        pass

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

def main():
    pass
    # Recipe()


if __name__ == "__main__":
    main()
