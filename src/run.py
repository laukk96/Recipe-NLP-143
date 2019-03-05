from recipe import Recipe
from webscraper import scrape




def main():
    pass

    print('please enter url from allrecipes.com: ')
    user_input = input()

    recipe = scrape(user_input)

    while user_input != 0:
        print('0 to exit!')
        print('1 to convert to vegetarian')
        print('2 to convert to non-vegetarian')
        print('3 to convert to healthy')
        print('4 to convert to un-healthy')
        print('5 to convert to Indian')
        print('6 to convert to Chinese')
        print('9 to enter new url')
        
        user_input = input()

        if user_input == '0':
            break
        elif user_input == '1':
            veg_recipe = recipe.transform_to_vegetarian()
            print(veg_recipe)
        elif user_input == '2':
            nonveg_recipe = recipe.transform_to_nonvegetarian()
            print(nonveg_recipe)
        elif user_input == '3':
            recipe.transform_to_healthy()
        elif user_input == '5':
            indian_recipe = recipe.transform_to_indian()
            print(indian_recipe)
        elif user_input == '6':
            chinese_recipe = recipe.transform_to_chinese()
            print(chinese_recipe)    
        elif user_input == '9':
            url = user_input
            recipe = scrape(url)

    



if __name__ == "__main__":
    main()