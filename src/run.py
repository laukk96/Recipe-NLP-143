from recipe import Recipe
from webscraper import scrape
import copy
import os

def main():
    print('please enter url from allrecipes.com: ')
    log_file = open("errors.log", "a")
    user_input = input()
    scaled = False
    scaled_recipe = None
    # Test Input: 
    # user_input = "https://www.allrecipes.com/recipe/247363/chef-johns-grilled-lamb-with-mint-orange-sauce/"
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
    recipe = copy.deepcopy(og_recipe)
    while user_input != 0:
        os.system("clear")
        
        

        if scaled:
            print(scaled_recipe)
        else:
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
        print('8 to revert to original')
        print('9 to enter new url')
        try:
            user_input = input(":")

            if user_input == '0':
                break
            elif user_input == '1':
                recipe = recipe.transform_to_vegetarian()
                
            elif user_input == '2':
                recipe = recipe.transform_to_nonvegetarian()
                
            elif user_input == '3':
                recipe = recipe.transform_to_healthy()
                
            elif user_input == '4':
                recipe = recipe.transform_to_unhealthy()
                
            elif user_input == '5':
                recipe = recipe.transform_to_indian()
                
            elif user_input == '6':
                recipe = recipe.transform_to_chinese()
                
            elif user_input == '7':
                print('enter a factor by which you would like to transform the recipe scale:')
                factor_input = input()
                float_input = float(factor_input)
                scaled_recipe = recipe.transform_by_scale_factor(float_input)
                #print(scaled_recipe)
                scaled = True
            elif user_input == '8':
                recipe = copy.deepcopy(og_recipe)
                scaled = False
                scaled_recipe = None
                os.system("clear")
                print(recipe)
            elif user_input == '9':
                url = input("URL -> ")
                og_recipe = scrape(url)
                recipe  = copy.deepcopy(og_recipe)
                scaled = False
                scaled_recipe = None
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
