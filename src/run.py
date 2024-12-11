from recipe import Recipe
from webscraper import scrape
import copy

def main():
    print('please enter url from allrecipes.com: ')
    log_file = open("errors.log", "a")
    # user_input = input()
    # TODO: Remove test link 
    user_input = "https://www.allrecipes.com/recipe/247363/chef-johns-grilled-lamb-with-mint-orange-sauce/"
    try:
        og_recipe = scrape(user_input)
    except Exception as inst:
         print('Error occured wile parsing recipe from link. Please provide a link again:')
         msg = "Failed for url {0}: {1}\n".format(str(user_input), str(inst))
         print(msg)
         log_file.write(msg)
         log_file.flush()
    finally:
         log_file.close()

    while user_input != 0:
        recipe = copy.deepcopy(og_recipe)
        print(recipe)
        log_file = open("errors.log", "a")
        print('0 to Exit!')
        print('1 to convert to vegetarian')
        print('2 to convert to non-vegetarian')
        print('3 to convert to healthy')
        print('4 to convert to un-healthy')
        print('5 to convert to Indian')
        print('6 to convert to Chinese')
        print('7 to convert the scale')
        print('8 to convert to Stir-Fry')
        print('9 to enter new url')
        try:
            user_input = input(":")

            if user_input == '0':
                break
            elif user_input == '1':
                veg_recipe = recipe.transform_to_vegetarian()
                print(veg_recipe)
            elif user_input == '2':
                nonveg_recipe = recipe.transform_to_nonvegetarian()
                print(nonveg_recipe)
            elif user_input == '3':
                healthy_recipe = recipe.transform_to_healthy()
                print(healthy_recipe)
            elif user_input == '4':
                unhealthy_recipe = recipe.transform_to_unhealthy()
                print(unhealthy_recipe)
            elif user_input == '5':
                indian_recipe = recipe.transform_to_indian()
                print(indian_recipe)
            elif user_input == '6':
                chinese_recipe = recipe.transform_to_chinese()
                print(chinese_recipe)
            elif user_input == '7':
                print('enter a factor by which you would like to transform the recipe scale:')
                factor_input = input()
                float_input = float(factor_input)
                scaled_recipe = recipe.transform_by_scale_factor(float_input)
                print(scaled_recipe)
            elif user_input == '8':
                sf_recipe = recipe.transform_to_stirfry()
                print(sf_recipe)
            elif user_input == '9':
                url = input("URL -> ")
                og_recipe = scrape(url)
        except Exception as inst:
            print('Something went wrong. Please try again:')
            msg = "Failed for user input - {0}: {1}\n".format(str(user_input), str(inst.with_traceback()))
            print(msg)
            log_file.write(msg)
            log_file.flush()
        finally:
            log_file.close()
            #data = log_file.read()





if __name__ == "__main__":
    main()
