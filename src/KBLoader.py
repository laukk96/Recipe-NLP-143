import json

import requests
import unidecode


def get_kb_lists():
    all_food_query = '''SELECT DISTINCT ?foodLabel ?countryLabel
                        WHERE
                        {
                          ?food wdt:P279 wd:Q2095 .
                          OPTIONAL{?food wdt:P361 ?country}.

                          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                        }'''

    food_ingredient_query = '''SELECT DISTINCT ?food ?foodLabel ?country ?countryLabel
                        WHERE
                        {
                          ?food wdt:P31 wd:Q25403900 .
                          OPTIONAL{?food wdt:P361 ?country}


                          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                        }'''

    meats_query = '''SELECT DISTINCT ?food ?foodLabel ?country ?countryLabel
                        WHERE
                        {
                          ?food wdt:P279 wd:Q10990 .
                          OPTIONAL{?food wdt:P361 ?country}


                          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                        }'''
    vegetable_query = '''SELECT DISTINCT ?food ?foodLabel ?country ?countryLabel
                        WHERE
                        {
                        ?food wdt:P279 wd:Q11004 .
                        OPTIONAL{?food wdt:P361 ?country}


                        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                        }'''

    fruit_query = '''SELECT DISTINCT ?food ?foodLabel ?country ?countryLabel
                    WHERE
                    {
                      ?food wdt:P279 wd:Q3314483 .
                      OPTIONAL{?food wdt:P361 ?country}


                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                    }'''

    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

    all_food_json = requests.get(url, params={'query': all_food_query, 'format': 'json'}).json()
    food_ingredients_json = requests.get(url, params={'query': food_ingredient_query, 'format': 'json'}).json()
    meats_json = requests.get(url, params={'query': meats_query, 'format': 'json'}).json()
    vegetables_json = requests.get(url, params={'query': vegetable_query, 'format': 'json'}).json()
    fruit_json = requests.get(url, params={'query': fruit_query, 'format': 'json'}).json()

    with open('all_food.json', 'w') as outfile:
        json.dump(all_food_json, outfile)
    with open('food_ingredients.json', 'w') as outfile:
        json.dump(food_ingredients_json, outfile)
    with open('meats.json', 'w') as outfile:
        json.dump(meats_json, outfile)
    with open('vegetables.json', 'w') as outfile:
        json.dump(vegetables_json, outfile)
    with open('fruits.json', 'w') as outfile:
        json.dump(fruit_json, outfile)


def get_all_foods():
    all_food = set()
    try:
        file_pointer = open('all_food.json')
        all_food_json = json.load(file_pointer)
        # print(all_food_json)
        for item in all_food_json['results']['bindings']:
            foodlabel = unidecode.unidecode(item['foodLabel']['value'].lower())
            if 'countryLabel' in item:
                countryLabel = '_' + unidecode.unidecode(item['countryLabel']['value'].lower())
            else:
                countryLabel = ""
            all_food.add(foodlabel + countryLabel)
        return all_food
    except:
        print('FILE NOT FOUND, please run get_kb_lists()')

def get_all_foods_dic():
    all_food = dict()
    all_food['NO_COUNTRY'] = []
    try:
        file_pointer = open('all_food.json')
        all_food_json = json.load(file_pointer)
        # print(all_food_json)
        for item in all_food_json['results']['bindings']:
            print ("Here")
            foodlabel = unidecode.unidecode(item['foodLabel']['value'].lower())
            if 'countryLabel' in item:
                print("in")
                country_key = unidecode.unidecode(item['countryLabel']['value'].lower())
                if country_key in all_food.keys():
                    print("inner if")
                    all_food[country_key].append(foodlabel)
                else:
                    print("inner else")
                    all_food[country_key] = [foodlabel]
            else:
                print("outer else")
                all_food['NO_COUNTRY'].append(foodlabel)
                print("pass")

        return all_food
    except:
        print('FILE NOT FOUND, please run get_kb_lists()')

def get_all_ingredients():
    all_food = set()
    try:
        file_pointer = open('food_ingredients.json')
        all_food_json = json.load(file_pointer)
        for item in all_food_json['results']['bindings']:
            all_food.add(unidecode.unidecode(item['foodLabel']['value'].lower()))
        return all_food
    except:
        'FILE NOT FOUND, please run get_kb_lists()'


def get_all_meats():
    try:
        fp = open('all_meats.txt')
        all_foods = set()
        for line in fp:
            all_foods.add(line.strip())
        return all_foods
    except:
        print('FILE NOT FOUND: {}'.format('all_meats.txt'))

    # To query for new meats. Don't do this unless all_meats.txt is missing.

    # all_food = set()
    # try:
    #     file_pointer = open('meats.json')
    #     all_food_json = json.load(file_pointer)
    #     for item in all_food_json['results']['bindings']:
    #         all_food.add(unidecode.unidecode(item['foodLabel']['value'].lower()))
    #     with open('all_meats.txt', 'w') as f:
    #         for item in all_food:
    #             f.write("%s\n" % item)
    #     return all_food
    # except:
    #     'FILE NOT FOUND, please run get_kb_lists()'


def get_all_vegetables():
    all_food = set()
    try:
        file_pointer = open('vegetables.json')
        all_food_json = json.load(file_pointer)
        for item in all_food_json['results']['bindings']:
            all_food.add(unidecode.unidecode(item['foodLabel']['value'].lower()))
        return all_food
    except:
        'FILE NOT FOUND, please run get_kb_lists()'


def get_all_fruits():
    all_food = set()
    try:
        file_pointer = open('fruits.json')
        all_food_json = json.load(file_pointer)

        for item in all_food_json['results']['bindings']:
            all_food.add(unidecode.unidecode(item['foodLabel']['value'].lower()))
        return all_food
    except:
        print('FILE NOT FOUND, please run get_kb_lists()')


def get_kaggle_foods():
    try:
        fp = open('all_food_list.txt')
        all_foods = set()
        for line in fp:
            all_foods.add(line.strip().lower())
        fp.close()
        return all_foods
    except:
        print('FILE {} NOT FOUND'.format('all_food_list.txt'))
        return None


def get_kaggle_food_with_cusine():
    try:
        fp = open('all_food_with_cuisine.txt')
        all_foods = {}
        for line in fp:
            # print(line)
            lst_splitted = line.strip().lower().split('#')
            if lst_splitted[0] in all_foods:
                all_foods[lst_splitted[0]].add(lst_splitted[1])
            else:
                all_foods[lst_splitted[0]] = set()
                all_foods[lst_splitted[0]].add(lst_splitted[1])
        fp.close()
        return all_foods
    except:
        print('FILE {} NOT FOUND'.format('all_food_with_cuisine.txt'))
        return None

if __name__ == "__main__":
    pass
    # get_kb_lists()
    # print('FRUITS: {}'.format(get_all_fruits()))
    # print('VEGGIES: {}'.format(get_all_vegetables()))
    # print('MEATS: {}'.format(get_all_meats()))
    # print('INGREDIENTS: {}'.format(get_all_ingredients()))
    # print('ALLFOOD: {}'.format(get_all_foods()))
    # print(len(get_kaggle_foods()))
    # print(len(get_kaggle_food_with_cusine()))
    # print(get_kaggle_food_with_cusine())
