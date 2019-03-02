import json

f = open('all_cusine_ingredient.json')
json_data = json.load(f)

ingredients_recipies = set()
all_ingredients = set()

print(json_data[0])
print(json_data[0]['cuisine'])
print(json_data[0]['ingredients'])

for object in json_data:
    cuisine_type = object['cuisine']
    ingredient_lst = object['ingredients']
    for i in range(len(ingredient_lst)):
        ingredients_recipies.add(ingredient_lst[i] + '#' + cuisine_type)
        all_ingredients.add(ingredient_lst[i])

#     print('###################')
#     for attribute, value in object.items():
#         print(attribute, ' ', value)
#         print(json_data['cuisine'])


print(len(all_ingredients))
print(len(ingredients_recipies))

with open('all_food_list.txt', 'w') as f:
    for item in all_ingredients:
        f.write("%s\n" % item)
with open('all_food_with_cuisine.txt', 'w') as f:
    for item in ingredients_recipies:
        f.write("%s\n" % item)

print(all_ingredients)

if __name__ == '__main__':
    print('cleaning kaggle')
