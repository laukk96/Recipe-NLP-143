import requests
from bs4 import BeautifulSoup

from recipe import Recipe


#test comment

def scrape(url):
    print(url)
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        tmp_lst = soup.find_all(class_="checkList__line")
        ingredients = []
        for item in tmp_lst:
            tmp = item.text.strip()
            if len(tmp) > 0 and tmp != 'Add all ingredients to list':
                ingredients.append(tmp)
        # print(ingredients)

        step_lst = soup.find_all(class_="recipe-directions__list--item")
        directions = []
        for step in step_lst:
            entry = step.text.lower().strip()
            if len(entry) > 0:
                directions.append(entry)
        # print(directions)
        recep = Recipe(ingredients, directions)
        # print(recep)
        # print('CONVERSION TO VEGETARIAN')
        # print(recep)
        # print(recep)
        # print('vegie')
        # recep = recep.transform_to_vegetarian()
        # print(recep)
        # print('back_to_meat')
        # recep = recep.transform_to_nonvegetarian()
        # print(recep)
        #
        # recep = recep.transform_to_indian()
        # print(recep)
        # print('##################################################TRANSFORMING')
        #comment2
        recep = recep.transform_to_indian()
        print(recep)
        return recep

    else:
        print('BAD REQUEST status:{1} WITH URL {0}'.format(url, page.status_code))
        return None

def main():
    list_of_urls = [
        'https://www.allrecipes.com/recipe/247363/chef-johns-grilled-lamb-with-mint-orange-sauce/?internalSource=streams&referringId=1021&referringContentType=Recipe%20Hub&clickId=st_trending_b',
        'https://www.allrecipes.com/recipe/76957/fast-chicken-soup-base/?internalSource=staff%20pick&referringId=15928&referringContentType=Recipe%20Hub&clickId=cardslot%202',
        'https://www.allrecipes.com/recipe/220560/kashmiri-lamb/?internalSource=staff%20pick&referringId=233&referringContentType=Recipe%20Hub&clickId=cardslot%206',
        'https://www.allrecipes.com/recipe/221131/baked-buffalo-chicken-dip/?internalSource=hub%20recipe&referringContentType=Search',
        'https://www.allrecipes.com/recipe/21176/baked-dijon-salmon/?internalSource=staff%20pick&referringId=1642&referringContentType=Recipe%20Hub',
        'https://www.allrecipes.com/recipe/25016/coconut-macaroon-brownies/?internalSource=streams&referringId=838&referringContentType=Recipe%20Hub&clickId=st_trending_b',
        'https://www.allrecipes.com/recipe/12009/creamy-cajun-chicken-pasta/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202',
        'https://www.allrecipes.com/recipe/26655/smothered-meatballs/?internalSource=popular&referringContentType=Homepage&clickId=cardslot%208',
        'https://www.allrecipes.com/recipe/265432/lemon-cheesecake-bars/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%2016',
        'https://www.allrecipes.com/recipe/85138/great-green-salad/?internalSource=streams&referringId=213&referringContentType=Recipe%20Hub&clickId=st_trending_s',
        'https://www.allrecipes.com/recipe/214080/kale-swiss-chard-chicken-and-feta-salad/','https://www.allrecipes.com/recipe/25317/carrot-chile-and-cilantro-soup/?internalSource=rotd&referringId=87&referringContentType=Recipe%20Hub',
        'https://www.allrecipes.com/recipe/245362/chef-johns-shakshuka/?internalSource=staff%20pick&referringId=87&referringContentType=Recipe%20Hub',
        'https://www.allrecipes.com/recipe/21528/pesto-pizza/?internalSource=staff%20pick&referringId=87&referringContentType=Recipe%20Hub',
        'https://www.allrecipes.com/recipe/256728/grilled-portobello-mushrooms-with-mashed-cannellini-beans-and-harissa-sauce/?internalSource=staff%20pick&referringId=87&referringContentType=Recipe%20Hub',

    ]

    for url in list_of_urls[:]:
        scrape(url)


if __name__ == "__main__":
    main()
