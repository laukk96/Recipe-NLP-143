import random
import re
from unicodedata import numeric
from fractions import Fraction
import KBLoader
import string
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


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
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.chinese_foods = ['frozen mixed thawed vegetables,', 'lap cheong', 'oyster sauce', 'green bell pepper', 'ginger piece', 'green lentil', 'Kikkoman Oyster Sauce', 'soy', 'fillet red snapper', 'chili pepper', 'crushed red pepper flakes', 'button mushrooms', 'tree ear mushrooms', 'choy sum', 'kecap manis', 'ruby port', 'pork bouillon cube', 'rice', 'dried minced onion', 'pickled radish', 'mushroom powder', 'steamed white rice', 'black rice', 'quail eggs', 'taro', 'nut oil', 'medium dry sherry', 'citric acid powder', 'black tea', 'chicken-flavored soup powder', 'chinese noodles', 'white rice', 'whole milk', 'mustard powder', 'flavored wine', 'seeds', 'teriyaki marinade', 'ginseng tea', 'red chili peppers', 'vanilla essence', 'chinese plum sauce', 'sake', 'chinese chives', 'seaweed', 'black garlic', 'chili paste with garlic', 'garland chrysanthemum', 'soybean paste', 'fermented bean curd', 'sliced green onions', 'Chinese sesame paste', 'Fuyu persimmons', 'safflower oil', 'white sesame seeds', 'white rice flour', 'bone in chicken thighs', 'canned corn', 'slaw mix', 'steamed brown rice', 'distilled vinegar', 'gluten-free oyster sauce', 'tiger lily buds', 'shell-on shrimp', 'lump crab meat', 'roast', 'minced garlic', 'zest', 'rock salt', 'pork shoulder boston butt', 'chinese buns', 'granulated white sugar', 'fresh spinach', 'chopped fresh mint', 'black', 'dry mustard', 'ground beef', 'orange extract', 'powdered garlic', 'fresh ginger root', 'frosting', 'ginkgo nut', 'loin pork roast', 'dark leafy greens', 'frozen pastry puff sheets', 'minced ginger', 'minced beef', 'bean curd stick', 'store bought low sodium chicken stock', 'chinese five-spice powder', 'seitan', 'cinnamon sticks', 'cassia cinnamon', 'shiitake', 'yellow split peas', 'onion tops', 'vidalia onion', 'gluten-free tamari sauce', 'wine', 'basil', 'ginger root', 'savoy cabbage', 'gari', 'garlic', 'curry paste', 'sweet soy sauce', 'grated lemon zest', 'bird chile', 'torn romain lettuc leav', 'tomato paste', 'green pepper', 'hot chili paste', 'tapioca flour', 'vegetable stock', 'baby corn', 'egg roll wraps', 'linguine', 'stir fry sauce', 'dashi', 'coconut sugar', 'char', 'garlic bulb', 'ginseng', 'leaf lettuce', 'lime leaves', 'ramen noodles', 'sunflower oil', 'cooked brown rice', 'dumpling dough', 'food colouring', 'vanilla powder', 'fish balls', 'pickle juice', 'dried black mushrooms', 'rice pilaf', 'kimchi', 'adzuki beans', 'water chestnuts', 'garlic oil', 'sichuan peppercorn oil', 'fresh chives', 'rice wine', 'snow pea pods', 'dry sherry', 'Chinese egg noodles', 'asparagus', 'globe eggplant', 'brown mushroom', 'tomato ketchup', 'frozen petit pois', 'gluten-free tamari', 'cherries', 'chuck', 'hot chili oil', 'diced onions', 'celery stick', 'wheat free soy sauce', 'pork loin chops', 'frozen edamame beans', 'mint sprigs', 'mango chutney', 'dry white wine', 'red pepper flakes', 'Tabasco Pepper Sauce', 'e-fu noodl', 'all-purpose flour', 'trout', 
'balsamic vinegar', 'fillet steaks', 'red bliss potato', 'cider vinegar', 'tapioca pearls', 'mace', 'silken tofu', 'semi firm tofu', 'pork rind', 'red beans', 'hawaiian sweet rolls', 'quick cooking brown rice', 'hearts of romaine', 'crisco', 'star anise', 
'sesame chili oil', 'rapeseed oil', 'vegetables', 'pickled vegetables', 'vegetarian oyster sauce', 'merluza', 'red bell pepper', 'garlic cloves', 'toasted almonds', 'varnish clams', 'mixed mushrooms', 'cooking wine', 'uncooked vermicelli', 'unsweetened coconut milk', 'fresh pineapple', 'dried dates', 'soup', 'shredded cabbage', 'beef tenderloin', 'raw honey', 'chopped fresh chives', 'mein', 'juice', 'chicken pieces', 'diced red onions', 'pork tenderloin', 'capsicum', 'white distilled vinegar', 'peapods', 'ground pork', 'fat free less sodium beef broth', 'brisket', 'yams', 'parsley', 'pork sausages', 'chinese pea pods', 'dough', 'lobster tails', 'grape tomatoes', 'pickling cucumbers', 'ground chicken breast', 'chicken thighs', 'olives', 'duck', 'yellow curry paste', 'shanghai bok choy', 'low-sodium low-fat chicken broth', 'whole grain thin spaghetti', 'flowering garlic chives', 'portabello mushroom', 'chinese black mushrooms', 'fat free less sodium chicken broth', 'champagne', 'celery root', 'pork loin', 'semi-sweet chocolate morsels', 'prawns', 'Japanese mountain yam', 'chile sauce', 'thyme', 'rabbit', 'savory', 'broccoli stems', 'loin', 'liquid aminos', 'palm sugar', 'scallops', 'chopped leaves', 'egg roll skins', 'boneless sirloin', 'ramps', 'tangzhong roux', 'cabbage leaves', 'cod fillets', 'onions', 'instant rice', 'romaine lettuce hearts', 'toasted sesame seeds', 'vanilla extract', 'ground sage', 'lotus roots', 'evaporated milk', 'vegetable shortening', 'nonstick spray', 'honey mustard', 'lemon grass', 'apple cider vinegar', 'dried rice noodles', 'lamb', 'fresh green bean', 'center cut pork roast', 'carp', 'egg yolks', 'hot pepper sauce', 'fresh asparagus', 'daikon', 'romaine lettuce leaves', 'simple syrup', 'bread flour', 'whole wheat spaghetti', 'lean minced beef', 'caster sugar', 'radishes', 'boar', 'vinegar', 'chinese celery', 'dried lentils', 'club soda', 'corn flour', 'soy milk', 'boneless chicken', 'tart shells', 'pork stock', 'broccoli rabe', 'sushi rice', 'dried cherry', 'baby spinach', 'bibb lettuce', 'pea pods', 'sirloin', 'chili bean paste', 'brown rice vinegar', 'whipped cream', 'spring greens', 'pineapple chunks', 'sweet pepper', 'cilantro sprigs', 'double-acting baking powder', 'coconut oil', 'chuka soba noodles', 'rum', 'black bean garlic sauce', 'fillet of beef', 'coconut extract', 'red bean paste', 'pork spare ribs', 'new york strip steaks', 'pink peppercorns', 'canned low sodium chicken broth', 'whole chicken', 'dry yeast', 'frozen orange juice concentrate', 'green cabbage', 'cubed beef', 'goji berries', 'taco shells', 'Italian parsley leaves', 'garbanzo beans', 'sweet rice wine', 'ground cayenne pepper', 'boiling water', 'rib', 'chinese celery cabbage', 'thick-cut bacon', 'pig', 'other vegetables', 'sweet basil', 'fat skimmed reduced sodium chicken broth', 'rice flour', 'licorice root', 'boneless skinless chicken', 'kale', 'dark soy sauce', 'ponzu', 'brown rice', 'Korean chile flakes', 'dark sesame oil', 'small eggs', 'fry mix', 'scrod fillets', 'butterflied leg of lamb', 'coca-cola', 'peppercorns', 'coleslaw', 'cooked chicken', 'baby gem lettuce', 'lentils', 'white wine', 'fresh coriander', 'fillets', 'longan', 'chicken meat', 'ground black pepper', 'potatoes', 'brandy', 'serrano peppers', 'toasted slivered almonds', 'low sodium beef broth', 

'boiling potatoes', 'stevia', 'shrimp stock', 'pangasius', 'ground roasted sichuan peppers', 'sesame seeds', 'lapsang souchong', 'soy nuts', 'baking soda', 'shallots', 'granulated garlic', 'baby back ribs', 'mustard greens', 'duck drumsticks', 'hot sauce', 'forest mushroom', 'thai chile', 'egg roll wrappers', 'cornflour', 'plum wine', 'sunflower seeds', 'green tomatoes', 'store bought low sodium vegetable stock', 'boneless chicken thighs', 'salted seaweed', 'snow pea shoots', 'apricot preserves', 'fat free beef broth', 'corn syrup', 'bean paste', 'beef brisket', 'low sodium vegetable broth', 'black bean sauce with garlic', 'roasted white sesame seeds', 'Soy VayÂ® Toasted Sesame Dressing & Marinade', 'anise', 'reduced sodium teriyaki sauce', 'chicken bouillon', 'nian gao', 'romaine lettuce', 'natto', 'natural peanut butter', 'lemon pepper', 'habanero', 'chinese sausage', 'green apples', 'salted fish', 'almond paste', 'gingerroot', 'turkey meat', 'sirloin steak', 'vermicelli', 'dressing', 'yardlong beans', 'dried soba', 'dried shiitake mushrooms', 'chicken carcass', 'cooked rice', 'sambal chile paste', 'cooking spray', 'char siu sauce', 'chilli paste', 'maldon sea salt', 'aspic', 'lo bok', 'mi', 'barley flakes', 'purple onion', 'lean ground beef', 'white rice vinegar', 'mandarin orange segments', 'white miso', 'Lea & Perrins Worcestershire Sauce', 'fresh basil leaves', 'unsalted dry roast peanuts', 'edamame', 'breast of lamb', 'giblet', 'frozen popcorn chicken', 'cream of mushroom soup', 'lemon wedge', 'whiskey', 'angel hair', 'egg noodles', 'chinese jujubes', 'almond extract', 'thai basil', 'sugar substitute', 'steamer', 'sesame oil', 'muscovado sugar', 'white flour', 'gluten-free hoisin sauce', 'cooked quinoa', '33 less sodium smoked fully cooked ham', 'orange zest', 'lower sodium chicken broth', 'asian fish sauce', 'glutinous rice', 'cocktail cherries', 'wheatberries', 'bread crumbs', 
'chopped onion', 'cooked bacon', 'store bought low sodium chicken broth', 'sweet rice', 'bread', 'raw sugar', 'steak', 'broiler-fryer chicken', 'low sodium gluten free soy sauce', 'potsticker wrappers', 'frozen garden peas', 'celery', 'pepper flakes', 'white button mushrooms', 'spring roll wrappers', 'buttermilk', 'flowering chives', 'bacon', 'chinese rock sugar', 'regular soy sauce', 'pickles', 'coarse salt', 'scallions', 'rainbow trout', 'spices', 'leeks', 'tofu puffs', 'regular sugar', 'teas', 'chicken fingers', 'celery seed', 'lamb shoulder', 'leftover steak', 'plantains', 'fermented bean paste', 'yellow chives', 'golden brown sugar', 'vietnamese fish sauce', 'seasoning', 'arugula', 'frozen peas', 'century eggs', 'chili powder', 'ground nutmeg', 'chili sauce', 'whole peppercorn', 'groundnut', 'bone-in chicken breasts', 'fronds', 'spinach leaves', 'milk', 'hand', 'low sodium stock', 'walnuts', 'curry powder', 'chicken stock cubes', 'minced chicken', 'puff pastry sheets', 'coarse kosher salt', 'stem ginger in syrup', 'mushrooms', 'roasted hazelnuts', 'tree ears', 'gyoza', 'bai cai', 'ground white pepper', 'chinese pancakes', 'dumplings', 'chinese mustard', 'rotisserie chicken', 'asian barbecue sauce', 'hot pepper', 'oysters', 'corn starch', 'skinless chicken breasts', 'fresh chicken stock', 'shrimp heads', 'peaches', 'green cardamom', 'pak choi', 'buns', 'top sirloin steak', 'orange peel', 'baby portobello mushrooms', 'orange', 'pork spareribs', 'beef stock', 'halibut fillets', 'fresh thyme leaves', 'liquorice', 'tarragon', 'large egg yolks', 'chicken thigh fillets', 'chinese black vinegar', 'chilli bean sauce', 'serrano chile', 'fresh tomatoes', 'ketchup', 'pears', 'rub', 'coriander seeds', 'side pork', 'Chinese rose wine', 'iceberg lettuce', 'hoisin sauce', 
'wide rice noodles', 'freshly ground pepper', 'caramel sauce', 'onion salt', 'fish paste', 'gluten free soy sauce', 'cracker crumbs', 'curly kale', 'nuts', 'lemongrass', 'fresh chili', 'Lipton Sparkling Diet Green Tea with Strawberry Kiwi', 'konbu', 'flavored oil', 'salted roast peanuts', 'fresh pork fat', 'top round steak', 'sweet corn', 'grated carrot', 'green onions', 'red chile sauce', 'peeled prawns', 'boiled ham', 'won ton skins', 'wine vinegar', 'chile paste with garlic', 'crushed pineapples in juice', 'vegetable broth', 'red radishes', 'beef sirloin', 'frozen broccoli', 'lower sodium soy sauce', 'sliced cucumber', 'low sodium teriyaki sauce', 'roasted sesame seeds', 'medium egg noodles', 'peanut sauce', 'Argo Corn Starch', 'dumpling wrappers', 'chicken', 'turbinado', 'pinenuts', 'fat-free chicken broth', 'yolk', 'red snapper', 'sweet and sour sauce', 'adobo', 'beef', 'serrano chilies', 'white bread', 'long grain white rice', 'meat bones', 'lobster', 'frozen shelled edamame', 'chinese red rice vinegar', 'ghee', 'beans', 'black vinegar', 'cayenne pepper', 'spring roll skins', 'dried prawns', 'reduced fat creamy peanut butter', 'glutinous rice flour', 'hot mustard', 'cabbage', 'long green chilies', 'extra large shrimp', 'beef consomme', 'wheat flour', 'salad greens', 'beef stew meat', 'fresh mushrooms', 'condensed milk', 'white rum', 'cayenne', 'curing salt', 'fresh mint', 'beef bones', 'hamburger', 'cane vinegar', 'grapeseed oil', 'jalapeno chilies', 'regular sour cream', 'black moss', 'imitation crab meat', 'soy sauce', 'peeled fresh ginger', 'chinese radish', 'Soy VayÂ® Hoisin Garlic Marinade & Sauce', 'reduced-fat sour cream', 
'honey', 'ground chicken', 'pork cutlets', 'haricots verts', 'filet', 'low sodium store bought chicken stock', 'rice stick noodles', 'vegan chicken flavored bouillon', 'marsala wine', 'cranberries', 'active dry yeast', 'medium shrimp', 'red vinegar', 'granulated sugar', 'goma', 'chopped cilantro', 'self raising flour', 'rice vermicelli', 'Thai chili garlic sauce', 'medium firm tofu', 'beaten eggs', 'cold water', 'calamari steak', 'squid', 'cooking oil', 'lean beef', 'fresh chile', 'eggplant', 'boneless sirloin steak', 'jasmine rice', 'chinese hot mustard', 'chow mein noodles', 'lemon juice', 'chenpi', 'bicarbonate of soda', 'fruit', 'tahini', 'finely chopped onion', 'white vinegar', 'white mushrooms', 'fresh udon', 'greater yam', 'chinese roast pork', 'reduced sodium soy sauce', 'tea cake', 'fresh lemon juice', 'sweet potato starch', 'soba noodles', 'starch', 'poppy seeds', 'crosswise', 'dates', 'chopped walnuts', 'black bean stir fry sauce', 'sweet bean sauce', 'spareribs', 'bamboo shoots', 'Japanese soy sauce', 'cut up chicken', 'pineapple', 'black pepper', 'shredded lettuce', 'peeled tomatoes', 'flavoring', 'cooked long-grain brown rice', 'white truffle oil', "I Can't Believe It's Not Butter!Â® Spread", 'baking potatoes', 'fish sauce', 'large garlic cloves', 'comice pears', 'deveined shrimp', 'green leaf lettuce', 'mung bean sprouts', 'dried Thai chili', 'free-range eggs', 'wax beans', 'lamb chops', 'clove', 'diced green chilies', 'carrots', 'roasted cashews', 'coconut flour', 'chicken stock', 'country crock calcium plus vitamin d', 'liqueur', 'fresh cilantro', 'cream', 'beets', 'rooster', 'corn oil', 'chopped garlic', 'pineapple rings', 'jujube', 'spam', 'corn kernels', 'rice vinegar', 'vegetable oil spray', 'coconut', 'ramen soup mix', 'black peppercorns', 
'chiles', 'mint', 'low sodium chicken broth', 'San Marzano tomatoes', 'lemon zest', 'skim milk', 'chili pepper flakes', 'red preserved bean curd', 'ground cinnamon', 'asparagus spears', 'butter', 'rice noodles', 'yellow squash', 'chinese cabbage', 'free-range chickens', 'meat sauce', 'salt water', 'all purpose unbleached flour', 'tri-tip roast', 'hong kong-style noodles', 'broccoli slaw', 'bean curd', 'coconut aminos', 'all potato purpos', 'chillies', 'chilegarlic sauce', 'white peppercorns', 'green chile', 'won ton wrappers', 'udon', 'deep-fried tofu', 'clams', 'jicama', 'beef gravy', 'diced ham', 'plum tomatoes', 'less sodium beef broth', 'orange juice', 'bell pepper', 'whitefish fillets', 'braising beef', 'mo hanh', 'king prawns', 'smoked salmon', 'roast red peppers, drain', 'french fried onions', 'low-sodium fat-free chicken broth', 'kirby cucumbers', 'black sesame seeds', 'tea bags', 'dried udon', 'panko breadcrumbs', 'Tyson Crispy Chicken Strips', 'se', 'salt', 'water']
        self.chinese_food_embeddings = self.model.encode(self.chinese_foods)
        self.indian_foods = ['asafetida (powder)', 'hing (powder)', 'besan (flour)', 'chicken bones', 'buns', 'gravy', 'lemon grass', 'ancho powder', 'cracked black pepper', 'fresh peas', 'arhar dal', 'dried chickpeas', 'baking potatoes', 'ground blanched almonds', 'ground turkey', 'canned chopped tomatoes', 'roast beef', 'radishes', 'broad beans', 'waxy potatoes', 'boneless, skinless chicken breast', 'fresh ginger root', 'breast', 'white kidney beans', 'chicken tenderloin', 'fresh chile', 'curry', 'cooking spray', 'bread flour', 'flat leaf parsley', 'evaporated cane juice', 'strong white bread flour', 'baguette', 'curry sauce', 'fresno chiles', 
'ground chicken breast', 'chat masala', 'boneless rib eye steaks', 'onion rings', 'frozen mixed vegetables', 'moong dal', 'anise', 'kashmiri chile', 'brown rice', 'tamarind water', 'mixed bell peppers', 'kaffir lime leaves', 'low-fat buttermilk', 'Italian parsley leaves', 'coarse sea salt', 'chicken bouillon granules', 'half & half', 'lime zest', 'rice stick noodles', 'water', 'crushed red pepper', 'homemade chicken stock', 'pinenus', 'fruit juice', 'acorn squash', 'dry mustard', 'paneer cheese', 'mung beans', 'vegetables', 'rotisserie chicken', 'diced celery', 'salted peanuts', , 'turmeric root', 'self rising flour', 'fresh lime juice', 'yellow mustard seeds', 'softened butter', 'red capsicum', 'toasted sesame seeds', 'ice', 'spring onions', 'boneless skinless chicken breasts', 'chapati flour', 'lite coconut milk', 'black salt', 'lower sodium chicken broth', 'whole wheat flour', 'salted butter', 'paste tomato', 'cooking cream', 'phyllo', 'golden raisins', 'fresh prawn', 'green onions', 'white fleshed fish', 'plain yogurt', 'yellow lentils', 'biscuit dough', 'onion soup mix', 'ground cardamom', 'chopped almonds', 'minced meat', 'diced tomatoes', 'shoulder lamb chops', 'plain soy yogurt', 'fresh spinach', 'white wine vinegar', 'mustard powder', 'garlic cloves', 'amba', 'bengal gram', 'meat', 'beef sirloin', 'chicken breast tenders', 'candied ginger', 'non dairy milk', 'capsicum', 'grated cauliflower', 'frozen chopped spinach', 'marjoram', 'tomato paste', 'sourdough bread', 'pink lentil', 'palm sugar', 'skinless chicken thighs', 'Elmlea single', 'brown cardamom', 'green chile', 'tea leaves', 'Himalayan salt', 'scallops', 'cilantro stems', 'heavy whipping cream', 'yoghurt', 'trout fillet', 'double concentrate tomato paste', 'large tomato', 'granny smith apples', 'maida flour', 'sooji', 'canned tomatoes', 'diced lamb', 'lemon slices', 'head cauliflower', 'tomato juice', 'smoked haddock', 'minced beef', 'hot red pepper flakes', 'fresh basil', 'coarse salt', 'lamb leg steaks', 'chopped garlic', 'Vadouvan curry', 'lamb stock', 'small red potato', 'lemongrass', 'peaches', 'dates', 'fresh lemon juice', 'bread crumbs', 'mango chutney', 'serrano', 'roasted peanuts', 'cubed potatoes', 'mahimahi', 'celery root', 'yellow peppers', 'orange flower water', 'low sodium chicken stock', 'small tomatoes', 'cooking sherry', 'purple onion', 'chili paste', 'brown mustard', 'large garlic cloves', 'center cut loin pork chop', 'vegetable stock', 'nonfat greek yogurt', 'ground ginger', 'pearl couscous', 'crimini mushrooms', 'king prawns', 'idli', 'oil', 'tapioca pearls', 'puff pastry', 'garlic', 'red pepper', 'roasted cashews', 'chicken strips', 'peppermint', 'rice', 'white mushrooms', 'Thai red curry paste', 'cumin', 'ginger root', 'chopped celery', 'salmon fillets', 'taro', 'cooked rice', 'raita', 'ground cinnamon', 'buckwheat flour', 'dried red chile peppers', 'green chilies', 'catfish fillets', 'cucumber', 'lime slices', 'lamb shoulder', 'almond extract', 'papad', 'mussels', 'pickling spices', 'yellow summer squash', 'hot curry powder', 'chile de arbol', 'meat tenderizer', 'soy', 'sliced almonds', 'herbs', 'green lentil', 'boiled eggs', 'unsweetened soymilk', 'loin pork chops', 'passata', 'steamed white rice', 'whole wheat pastry flour', 'cooked turkey', 'arbol chile', 'arrowroot flour', 'english cucumber', 'raw almond', 'clove garlic, fine chop', 'red food coloring', 'red chili powder', 'frozen green beans', 'pistachios', 'fresh red chili', 'tea bags', 'chile pepper', 'boiling potatoes', 'cooking fat', 'granulated garlic', 'ground mustard', 'rock salt', 'instant rice', 'ground turmeric', 'yellow corn meal', 'plain whole-milk yogurt', 'sliced green onions', 'chile paste', 'diced red onions', 'paratha', 'gooseberries', 'roast red peppers, drain', 'nutmeg', 'masur dal', 'powdered milk', 'lamb shoulder chops', 'dried cranberries', 'plain flour', 'noodles', 'natural yogurt', 'crushed ice', 'yogurt cheese', 'habanero powder', 'hot pepper', 'basmati', 'snappers', 'lemon pepper', 'black sesame seeds', 'tomatoes with juice', 'fresh thyme', 'all-purpose flour', 'vermicelli noodles', 'active dry yeast', 'chana dal', 'cream yogurt', 'pork butt', 'olives', 'silver', 'melted butter', 'pomegranate seeds', 'frozen pastry puff sheets', 'tandoori paste', 'panko breadcrumbs', 'coconut', 'citrus juice', 'whole milk', 'balsamic vinegar', 'cilantro sprigs', 'cooked white rice', 'fresh basil leaves', 'sirloin steak', 'strawberry syrup', 'fat-free mayonnaise', 'curry paste', 'plums', 'ground nutmeg', 'clarified butter', 'wheat bread', 'grated lemon zest', 'chicken broth low fat', 'mung bean sprouts', 'flat leaf spinach', 'turkey breast', 'jalape', 'bitter gourd', 'squid', 'cheese', 'cardamom', 'star anise', 'chipotle chile', 'fresh pineapple', 'port wine', 'corn kernel whole', 'grated orange peel', 'ground almonds', 'pappadams', 'finely chopped onion', 'oyster sauce', "Quorn Chik''n Tenders", 'arrowroot powder', 'whole peeled tomatoes', 'bone in skin on chicken thigh', 'cod', 'apple juice', 'orange zest', 'crust', 'fillets', 'toasted buns', 'butternut squash', 'dried Thai chili', 'apricots', 'wafer', 'swordfish', 'lotus roots', 'tofu', 'white cake mix', 'pork loin chops', 'sherry vinegar', 'beef tenderloin', 'crÃ¨me fraÃ®che', 'red chile powder', 'chicken breast halves', 'peas', 'keema', 'full-fat plain yogurt', 'tapioca flour', 'mushrooms', 'green bell pepper', 'chicken fingers', 'seasoned rice wine vinegar', 'mooli', 'pork tenderloin', 'cauliflower flowerets', 'chicken', 'parsley flakes', 'pie dough', '(14 oz.) sweetened condensed milk', 'steamer', 'semolina', 'red curry paste', 'black peppercorns', 'frozen peas', 'sole fillet', 'sourdough starter', 'orange juice', 'nut oil', 'finely chopped fresh parsley', 'nonfat evaporated milk', 'fennel seeds', 'black lentil', 'currant', 'oregano', 'anise seed', 'lemon wedge', 'curry powder', 'fresh dill', 'chili', 'whole garam masala', 'cream', 'gin', 'khoa', 'raisins', 'saffron threads', 'white onion', 'bone in chicken thighs', 'unsalted roasted peanuts', 'strawberries', 'stone flower', 'extra firm tofu', 'ground peanut', 'chili powder', 'boneless chicken', 'bhaji', 'urad dal split', 'reduced fat creamy peanut butter', 'halibut', 'tamarind extract', 'frozen spinach', 'fresh curry', 'kirby cucumbers', 'heavy cream', 'mild green chiles', 'fresh yeast', 'lamb fillet', 'pickled carrots', 'chicken stock cubes', 'yoghurt natural low fat', 'ceylon cinnamon', 'caster sugar', 'white button mushrooms', 'new potatoes', 'hard-boiled egg', 'string beans', 'salt and ground black pepper', 'pita bread', 'sea salt', 'seeds', 'figs', 'juice', 'granular sucrolose sweetener', 'tofu sour cream', 'cubed mango', 'asafetida', 'portabello mushroom', 'diced bell pepper', 'shrimp', 'naan', 'shredded zucchini', 'vegetable oil', 'onions', 'roast', 'chopped fresh mint', 'yellow curry paste', 'salami', 'white flour', 'mini marshmallows', 'vinegar', 'cuminseed', 'Turkish bay leaves', 'tomato soup', 'reduced sodium chicken broth', 'red snapper', 'edamame', 'hothouse cucumber', 'gold potatoes', 'baby spinach', 'mixed nuts', 'wholemeal flour', 'spices', 'center-cut salmon fillet', 'chicken fillets', 'asafoetida powder', 'whole almonds', 'medium tomatoes', 'potato flakes', 
'slivered almonds', 'garden peas', 'frying oil', 'sultana', 'sun-dried tomatoes', 'fire roasted diced tomatoes', 'chapatti flour', 'low salt chicken broth', 'toasted cashews', 'ground cumin', 'chopped green chilies', 'bone-in chicken', 'unsulphured molasses', 'garbonzo bean', 'greens', 'dried parsley', 'black gram', 'greek yogurt', 'deveined shrimp', 'spanish onion', 'cane sugar', 
'apples', 'almond meal', 'salt water', 'pumpkin', 'whipping cream', 'split yellow lentils', 'clotted cream', 'yellow squash', 'short-grain rice', 'crushed red pepper flakes', 'wheat crackers', 'batter', 'kingfish', 'dried arbol chile', 'lamb stew meat', 'mulato chiles', 'green pepper', 'iceberg lettuce', 'lamb', 'chunky peanut butter', 'puffed rice', 'stewed tomatoes', 'avocado oil', 'methi', 'glaze', 'chow mein noodles', 'firmly packed light brown sugar', 'chili oil', 'japanese eggplants', 'bird chile', 'sweet corn', 'meat bones', 'jalapeno chilies', 'chicken thighs', 'roasted sesame seeds', 'channa dal', 'minced onion', 'dried thyme', 'semolina flour', 'idaho potatoes', 'chicken drumsticks', 'candlenuts', 'dried kidney beans', 'firmly packed brown sugar', 
'fresh green bean', 'serrano chilies', 'splenda', 'rockfish', 'aleppo pepper', 'coffee granules', 'sun-dried tomatoes in oil', 'zucchini', 'mint', 'golden delicious apples', 'nonfat milk powder', 'curry mix', 'pepper flakes', 'kasuri methi', 'chopped parsley', 'cooking oil', 'garlic naan', 'canned low sodium chicken broth', 'nuts', 'soda', 'runny honey', 'corn kernels', 'vine tomatoes', 'tahini', 'cremini mushrooms', 'chickpea flour', 'ginger purÃ©e', 'plantains', 'carrots', 'kewra water', 'poha', 'baby spinach leaves', 'lamb chops', 'nonfat yogurt', 'frozen spring roll wrappers', 'Manischewitz Matzo Meal', 'fruit', 'soy yogurt', 'minced chicken', 'cornish game hens', 'mustard seeds', 'whipped cream', 'chicken thigh fillets', 'coconut cream', 'aioli', 'chile paste with garlic', 'cut up chicken', 'hot dog bun', 'lime wedges', 'leg of lamb', 'kosher salt', 'burger buns', 'less sodium beef broth', 'fat free milk', 'dry bread crumbs', 'cauliflower florets', 'top sirloin steak', 'yellow mustard', 'toasted sesame oil', 'corn tortillas', 'demerara sugar', 'chicken broth', 'rosewater', 'dry yeast', 'gluten free all purpose flour', 'korma paste', 'asafetida powder', 'cooked vegetables', 'black pepper', 'reduced fat mayonnaise', 'yellow heirloom tomatoes', 'salted mixed nuts', 'cardamom pods', 'kabuli channa', '2% reduced-fat milk', 'fat-free buttermilk', 'and fat free half half', 'whole nutmegs', 'fresh cilantro', 'reduced fat firm tofu', 'large shrimp', 'poppyseeds', 'dried minced onion', 'organic coconut milk', 'dry milk powder', 'margarine', 'baby greens', 'creamed coconut', 'dry coconut', 'cantaloupe', 'fresh veget', 'couscous', 'fish', 'butter beans', 'non-fat sour cream', 'leeks', 'pork meat', 'cilantro leaves', 'hamburger buns', 'French lentils', 'natural low-fat yogurt', 'whey', 'jasmine rice', 'corn', 'toasted unsweetened coconut', 'raw sugar', 'shredded cabbage', 'coarse kosher salt', 'kiwi', 'CURRY GUY Smoked Garam Masala', 'fine sea salt', 'fresh green peas', 'garlic chili sauce', 'free range egg', 'cream cheese, soften', 'molasses', 'asafoetida', 'egg whites', 'seitan', 'haddock fillets', 'sugarcane juice', 'skinless chicken breasts', 'red pepper flakes', 'lamb cutlet', 'soft fresh goat cheese', 'salted cashews', 'bone broth', 'chicken wing drummettes', 'finely ground coffee', 'condensed milk', 'malt vinegar', 'hot chili sauce', 'Nakano Seasoned Rice Vinegar', 'alphabet pasta', 'red apples', 'yeast', 'vanilla yogurt', 'tomato sauce', 'yellow food coloring', 'seasoning', 'potato chips', 'dal', 'yeast extract', 'skinless chicken pieces', 'unsalted butter', 'chaat masala', 'serrano chile', 'green tomatoes', 'low sodium chicken broth', 'white vinegar', 'store bought low sodium chicken broth', 'champagne vinegar', 'black cumin seeds', 'tandoori seasoning', 'horseradish root', 'methi leaves', 'unsalted almonds', 'light molasses', 'Spring! Water', 'red chili peppers', 'roasted salted cashews', 
'halibut fillets', 'monkfish fillets', 'tamarind juice', 'french fried onions', 'pepitas', 'farina', 'whole wheat pita', 'hot green chile', 'soft-boiled egg', 'cake flour', 'dry roasted peanuts', 'lettuce leaves', 'instant yeast', 'diced potatoes', 'vegetable bouillon', 'canned beef broth', 'roast turkey', 'bittersweet chocolate chips', 'mint sprigs', 'eggplant', 'butter', 'drummettes', 'cashew milk', 'garlic paste', 'coriander seeds', 'barley', 'baton', 'rib eye steaks', 'unsweetened coconut milk', 'bread crumb fresh', 'medium curry powder', 'unsweetened almond milk', 'raw pistachios', 'whole grain mustard', 'cardamom seeds', 'unsweetened shredded dried coconut', 'pork loin', 'nonfat dry milk powder', 'smoked paprika', 'tandoori spices', 'ground lamb', 'pitted date', 'atta', 'cauliflower', 'corn husks', 'fat free yogurt', 'sour cream', 'Flora Buttery', 'cooked quinoa', 'tikka masala curry paste', 'teas', 'coconut sugar', 'pita bread rounds', 'syrup', 'corn oil', 'petite peas', 'Lipton Lemon Iced Tea Mix', 'vegetable shortening', 'coriander', 'dill weed', 'basmati rice', 'nonfat yogurt plain', 'canned chicken broth', 'pumpkin purÃ©e', 'chinese five-spice powder', 'Massaman curry paste', 'scallions', 'adobo sauce', 'hungarian paprika', 'winter melon', 'pork chops', 'beef boneless meat stew', 'orange', 'green bell pepper, slice', 'beef', 'chili sauce', 'cream of coconut', 'rice noodles', 'crabmeat', 'reduced fat coconut milk', 'lemon juice', 'red swiss chard', 'papaya', 'red wine', 'salt', 
'water', 'beef broth']
        self.indian_food_embeddings = self.model.encode(self.indian_foods)

    # removes the listed bad words from an ingredient string
    def _clean_ingredient(self, ingredient):
        
        list_bad_words = ['chopped', 'peeled', 'diced', 'minced', 'grated', 'sliced', 'fresh', 'organic']
        for word in list_bad_words:
            ingredient = re.sub(word, ' ', ingredient)
        return ingredient
    

    # finds ingredients/meats in recipe_ingredients that exist on kaggle
    # and adds them to self.meats and self.ingredients

    def _populate_ingredients(self):
        print(self.recipe_ingredients)
        
        for ingredient in self.recipe_ingredients:
            try:
                # Step 1: Split ingredients by commas
                ingredient_list = [i.strip() for i in ingredient.split('\n\n\n') if i.strip()]
                print(f"Ingredient List: {ingredient_list}")  # Debug

                for ingredient in ingredient_list:
                    # Step 2: Clean the ingredient
                    ingredient = self._clean_ingredient(ingredient)
                    print(f"Cleaned Ingredient: {ingredient}")  # Debug

                    # Step 3: Tokenize the ingredient string
                    lst_key_words = ingredient.lower().split()
                    lst_key_words = [word.replace(',', '') for word in lst_key_words]
                    print(f"Tokenized Keywords: {lst_key_words}")  # Debug

                    # Initialize variables for parsing
                    amount_quan_list = []
                    key_word_search = None
                    matched_word = None

                    # Step 4: Search for food keywords in the ingredient string
                    for i in range(len(lst_key_words)):
                        key_word_search = ' '.join(lst_key_words[i:])
                        if key_word_search in self.KBfoods:
                            matched_word = key_word_search
                            amount_quan_list = lst_key_words[:i]
                            for val in key_word_search.split():
                                if val in self.KBmeats:
                                    self.meats.add(val)
                                    break
                            break
                        if lst_key_words[i] in self.KBfoods:
                            if matched_word is None:
                                matched_word = lst_key_words[i]
                                amount_quan_list = lst_key_words[:i]
                            if matched_word in self.KBmeats:
                                self.meats.add(matched_word)
                                break

                    print(f"Matched Word: {matched_word}, Amount/Quantity List: {amount_quan_list}")  # Debug

                    # Step 5: Extract amount, measure type, and ingredient type
                    amount = None
                    measure_type = None
                    ingredient_type = None

                    # Handle amounts and measure types
                    if amount_quan_list:
                        try:
                            # First attempt to parse fractions, then handle whole numbers or text-based quantities
                            amount = str(Fraction(amount_quan_list[0]))  # Convert amount to a fraction
                        except ValueError:
                            # Check if amount is a number or just a descriptor like 'softened'
                            if amount_quan_list[0].isalpha():
                                amount = None
                            else:
                                amount = amount_quan_list[0]  # Fallback to raw value if not parsable

                        # Extract measure type
                        measure_types = ['cup', 'ounce', 'tablespoon', 'teaspoon', 'pound', 'gram', 'liter','cups', 'ounces', 'tablespoons', 'teaspoons', 'pounds', 'grams', 'liters', 'clove', 'cloves', 'pinch', 'pinches', 'quarts', 'quart']
                        for word in amount_quan_list[1:]:
                            if word in measure_types:
                                measure_type = word
                                break

                        # Extract ingredient type (after measure type)
                        if len(amount_quan_list) > 2:
                            ingredient_type = ' '.join(amount_quan_list[2:])

                        
                    
                    print(f"Parsed Details - Amount: {amount}, Measure Type: {measure_type}, Ingredient Type: {ingredient_type}")  # Debug

                    # Step 6: Add the parsed ingredient to the ingredients list
                    if matched_word is not None:
                        ingr = Ingredient(amount, measure_type, matched_word, ingredient_type)
                        self.ingredients.append(ingr)
                        print(f"Added Ingredient: {ingr}")  # Debug

            except Exception as e:
                print(f"Error processing ingredient '{ingredient}': {e}")  # Debug

    # finds primary and secondary cooking methods in self.recipe_steps and adds 
    # them to self.primary_methods, self.secondary_methods, self.tools
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
            for i in range(len(step_lst)): # goes thru each word in individual step
                val = step_lst[i]
                val = re.sub(r'[^\w\s]','',val)
                # categorizes/maps each cooking method
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
                # adds tools to self.tools
                if val in primary_tools:
                    self.tools.add(val)
        # [print(i) for i in self.recipe_steps]

    # removes ingr from self.ingredients
    def delete_ingredient(self, ingr):
        new_ingredients = []
        for i in range(len(self.ingredients)):
            if self.ingredients[i] != ingr:
                new_ingredients.append(self.ingredients[i])
        self.ingredients = new_ingredients

    def _get_best_meat_substitute(self, ingredient, vegetarian_substitutes):
        """
        This function finds the best vegetarian substitute by computing cosine similarity
        between the ingredient embedding and each substitute.
        """
        # Get the embedding for the ingredient
        ingredient_embedding = self.model.encode(ingredient, convert_to_tensor=True)
        
        # Get the embeddings for the vegetarian substitutes
        substitute_embeddings = self.model.encode(vegetarian_substitutes, convert_to_tensor=True)
        
        # Compute cosine similarities between the ingredient and all substitutes
        similarities = util.pytorch_cos_sim(ingredient_embedding, substitute_embeddings)[0]
        
        # Find the index of the most similar substitute
        best_substitute_idx = similarities.argmax()
        return vegetarian_substitutes[best_substitute_idx]
    def _clean_dup_step(self, step):
        """
        Clean duplicate words from recipe steps introduced by replacements.
        """
        words = step.split()
        return ' '.join(sorted(set(words), key=words.index))  # Removes duplicates while keeping order

    def transform_to_vegetarian(self):  # REQUIRED
        print('############', [str(ing) for ing in self.ingredients], self.meats)
        print('in transform to veg')

        # Predefined list of vegetarian substitutes
        vegetarian_substitutes = [
                    "tofu",
                    "tempeh",
                    "seitan",
                    "lentils",
                    "chickpeas",
                    "black beans",
                    "mushrooms",
                    "portobello mushrooms",
                    "jackfruit",
                    "cauliflower",
                    "zucchini",
                    "eggplant",
                    "vegetable patties",
                    "quinoa",
                    "soy protein",
                    "vegetable stew",
                    "coconut meat",
                    "pea protein",
                    "vegan cheese",
                    "vegan yogurt",
                    "vegan sausages",
                    "vegan bacon",
                    "almonds",
                    "crispy chickpeas",
                    "tofu scramble",
                    "butternut squash",
                    "soy milk",
                    "oat milk",
                    "rice paper",
                    "vegetable crumbles",
                    "vegan chicken strips",
                    "vegan ground meat",
                    "miso",
                    "lima beans",
                    "sweet potato",
                    "vegan meatballs",
                    "tofu skin",
                    "coconut bacon",
                    "tempeh bacon",
                    "vegetable broth"
                    
                ]

        if len(self.meats) > 0:
            for i in range(len(self.ingredients)):
                # Split the ingredient into words for matching
                search_list = self.ingredients[i].ingr.lower().split(' ')
                
                # Check if any word in the ingredient matches an item in self.meats
                if any(k in self.meats for k in search_list):
                    tmp_ingr = self.ingredients[i].ingr
                    print('-------------- Found meat ingredient:', tmp_ingr)

                    # Get a vegetarian substitute using Sentence-BERT
                    repl = self._get_best_meat_substitute(tmp_ingr, vegetarian_substitutes)
                    if not repl:
                        print("No substitute found for", tmp_ingr)
                        continue  # Skip if no substitute is found
                    
                    # Replace the ingredient with its substitute
                    self.ingredients[i].ingr = repl
                    
                    # Update recipe steps with the substitute
                    for j in range(len(self.recipe_steps)):
                        step = self.recipe_steps[j]
                        
                        # Replace all occurrences of the meat ingredient in the step
                        print(f"## Updating step: {step}")
                        for k in search_list:
                            if k in self.meats:
                                step = re.sub(rf'\b{k}\b', repl, step, flags=re.IGNORECASE)
                        
                        # Handle general phrases related to meat
                        step = re.sub(r' meat\.', f' {repl}.', step, flags=re.IGNORECASE)
                        step = re.sub(r' meat\b', '', step, flags=re.IGNORECASE)
                        step = re.sub(r' no longer pink and', '', step, flags=re.IGNORECASE)
                        step = re.sub(r'skin and bones', 'veggie scraps', step, flags=re.IGNORECASE)
                        step = re.sub(r'bones', repl, step, flags=re.IGNORECASE)
                        step = re.sub(r'skin', repl, step, flags=re.IGNORECASE)
                        step = re.sub(r' fat\b', '', step, flags=re.IGNORECASE)
                        
                        # Clean duplicate words introduced by replacements
                        new_step = self._clean_dup_step(step)
                        self.recipe_steps[j] = new_step
                        print(f"Updated step: {self.recipe_steps[j]}")

            # Clear the meats set after transformation
            self.meats = set()
            return self
        
        else:
            print("ELSE: No meats found to transform.")
            return self

    def _get_nonveg_ingredient(self):
        """
        This function returns a randomly selected non-vegetarian ingredient.
        """
        amount = random.choice([1, 2, 3, 4])
        type_ingr = random.choice(['cups', 'ounces'])
        meat = random.choice([
            'cooked crab', 'pulled pork', 'pan-fried bacon', 'cooked sausages', 'grilled chicken', 
            'fried shrimp', 'prosciutto', 'pan-seared fish'
        ])
        return Ingredient(amount, type_ingr, meat)

    def transform_to_nonvegetarian(self):  # REQUIRED
        # Predefined list of non-vegetarian substitutes
        non_veg_substitutes = [
            'cooked crab', 'pulled pork', 'pan-fried bacon', 'cooked sausages', 'grilled chicken', 
            'fried shrimp', 'prosciutto', 'pan-seared fish', 'beef steak', 'roast lamb', 'turkey breast',
    "jerky",
"primal cut",
"reptile meat",
"wild boar meat",
"turkey meat",
"camel meat",
"smoked meat",

"escalope",
"shawarma",
"minced meat",
"ambelopoulia",

"bison meat",
"meat on the bone",
"elephant meat",
"goat meat",
"kassler",

"quail meat",
'salt-cured meat',
"calf head",
"iguana meat",
"duck meat",


"mutton",
"whale meat",
"kutha meat",
"game",
"jhatka",

"kangaroo meat",

"pse meat",
"white meat",
"veal",
"shank",
"squab",

"salmon",
"beef",
"seal meat",
"confit",
"alligator meat",

"ttavas",
"chicken",
"red meat",
"poultry",
"in vitro meat",
"horse meat",
"canned meat",
"bushmeat",
"raw meat",

"rabbit meat",
"ventresca",
"brisket",

"pork",
"steak frites",
"dried meat",
"pastrami",
"lamb",
"goat",
"chicken",
"steak",
"beef",
"cow",
"shrimp",
"fish",

"pork sausage",
"sausage",
"crab",
"lobster",
"shellfish",
"oysters",
"venison",
"bacon",
"ham",
"salami",
"duck",
"pheasant",
"turkey",
"rabbit",
"boar",
"wild boar",
"ribs",
"sheep",
"goose",
"veal",
"jamon",
"prosciutto",
"lamb chops",
"pork chops",
"lamb loin chops","beef broth", "chicken broth"

]
        

        if len(self.meats) == 0:
            # Get a non-vegetarian ingredient using Sentence-BERT
            ingr = self._get_best_nonveg_ingredient(non_veg_substitutes)
            self.ingredients.append(ingr)
            
            # Get the first ingredient (lhs_ingredient) and append the new non-veg ingredient
            lhs_ingredient = self.ingredients[0].ingr
            repl_string = lhs_ingredient + ' and the ' + ingr.ingr
            
            # Update recipe steps with the new non-veg ingredient
            for j in range(len(self.recipe_steps)):
                self.recipe_steps[j] = re.sub(lhs_ingredient, repl_string, self.recipe_steps[j])
            
            return self
        else:
            return self

    def _get_best_nonveg_ingredient(self, non_veg_substitutes):
        """
        This function finds the best non-vegetarian ingredient by computing cosine similarity
        between the current recipe context and the list of possible non-vegetarian ingredients.
        """
        # Assume the current ingredient list has some context for selection
        context = ' '.join([ingredient.ingr for ingredient in self.ingredients])
        
        # Get the embedding for the context (all ingredients so far)
        context_embedding = self.model.encode(context, convert_to_tensor=True)
        
        # Get the embeddings for the non-vegetarian substitutes
        substitute_embeddings = self.model.encode(non_veg_substitutes, convert_to_tensor=True)
        
        # Compute cosine similarities between the context and all non-veg substitutes
        similarities = util.pytorch_cos_sim(context_embedding, substitute_embeddings)[0]
        
        # Find the index of the most similar non-vegetarian ingredient
        best_substitute_idx = similarities.argmax()
        return Ingredient(random.choice([1, 2, 3, 4]), random.choice(['cups', 'ounces']), non_veg_substitutes[best_substitute_idx])



    

    def float_to_fraction_string(self, value):
        # Handle common fractional values
        fraction_map = {
            0.5: "½",
            0.25: "¼",
            0.75: "¾",
            0.3333333333333333: "⅓",
            0.6666666666666666: "⅔",
            0.125: "⅛",
            0.375: "⅜",
            0.625: "⅝",
            0.875: "⅞"
        }

        if value in fraction_map:
            return fraction_map[value]

        # If not a common fraction, return the value as a regular fraction
        frac = Fraction(value).limit_denominator(100)
        if frac.denominator == 1:
            return str(frac.numerator)  # Just a whole number
        else:
            return f"{frac.numerator}/{frac.denominator}"

    def transform_by_scale_factor(self, factor):
        for ingredient in self.ingredients:
            if ingredient is not None and ingredient.amount is not None:
                try:
                # Attempt to parse the amount as a Fraction
                    amount = str(Fraction(ingredient.amount))
                except ValueError:
                # If parsing fails, handle symbolic fractions like ¼, ½, etc.
                    try:
                        amount = numeric(ingredient.amount)  # Converts symbolic fraction to float
                    except (TypeError, ValueError):
                        print(f"Could not parse amount '{ingredient.amount}'")
                        continue
                scaled_amount = float(Fraction(amount) * factor)
                # Convert the scaled amount back to a cute fractional string
                ingredient.amount = self.float_to_fraction_string(scaled_amount)
        return self


    def transform_to_indian(self):
        print('Transforming recipe to indian cuisine')
        
        # Iterate through the ingredients to find non-indian ones
        for i in range(len(self.ingredients)):
            ingredient = self.ingredients[i].ingr.lower()  # Convert to lowercase for matching
            
            # If ingredient is not indian, replace it with the most similar indian ingredient
            if ingredient not in self.indian_foods:
                print(f'Ingredient "{self.ingredients[i].ingr}" is not indian.')
                
                # Find the most similar indian ingredient
                repl = self.get_most_similar_indian_ingredient(ingredient)
                
                # Replace the ingredient in the recipe
                ingredient_to_replace = self.ingredients[i].ingr
                self.ingredients[i].ingr = repl
                
                # Replace ingredient in recipe steps
                for j in range(len(self.recipe_steps)):
                    self.recipe_steps[j] = re.sub(ingredient_to_replace, repl, self.recipe_steps[j])
                    self.recipe_steps[j] = self._clean_dup_step(self.recipe_steps[j])
                    
        return self

    def get_most_similar_indian_ingredient(self, non_indian_ingredient):
        # Encode the non-indian ingredient and all indian ingredients using Sentence-BERT
        non_indian_embedding = self.model.encode(non_indian_ingredient, convert_to_tensor=True)
        indian_embeddings = self.model.encode(self.indian_foods, convert_to_tensor=True)
        
        # Compute cosine similarities between the non-indian ingredient and all indian ingredients
        similarities = util.pytorch_cos_sim(non_indian_embedding, indian_embeddings)[0]
        
        # Get the index of the most similar indian ingredient
        most_similar_index = similarities.argmax().item()
        
        # Return the most similar indian ingredient
        return self.indian_foods[most_similar_index]

    def transform_to_chinese(self):
        print('Transforming recipe to Chinese cuisine')
        
        # Iterate through the ingredients to find non-Chinese ones
        for i in range(len(self.ingredients)):
            ingredient = self.ingredients[i].ingr.lower()  # Convert to lowercase for matching
            
            # If ingredient is not Chinese, replace it with the most similar Chinese ingredient
            if ingredient not in self.chinese_foods:
                print(f'Ingredient "{self.ingredients[i].ingr}" is not Chinese.')
                
                # Find the most similar Chinese ingredient
                repl = self.get_most_similar_chinese_ingredient(ingredient)
                
                # Replace the ingredient in the recipe
                ingredient_to_replace = self.ingredients[i].ingr
                self.ingredients[i].ingr = repl
                
                # Replace ingredient in recipe steps
                for j in range(len(self.recipe_steps)):
                    self.recipe_steps[j] = re.sub(ingredient_to_replace, repl, self.recipe_steps[j])
                    self.recipe_steps[j] = self._clean_dup_step(self.recipe_steps[j])
                    
        return self

    def get_most_similar_chinese_ingredient(self, non_chinese_ingredient):
        # Encode the non-Chinese ingredient and all Chinese ingredients using Sentence-BERT
        non_chinese_embedding = self.model.encode(non_chinese_ingredient, convert_to_tensor=True)
        chinese_embeddings = self.model.encode(self.chinese_foods, convert_to_tensor=True)
        
        # Compute cosine similarities between the non-Chinese ingredient and all Chinese ingredients
        similarities = util.pytorch_cos_sim(non_chinese_embedding, chinese_embeddings)[0]
        
        # Get the index of the most similar Chinese ingredient
        most_similar_index = similarities.argmax().item()
        
        # Return the most similar Chinese ingredient
        return self.chinese_foods[most_similar_index]
    
    


    def pretty_print_ingredients(self):
        for ingr in self.ingredients:
            val_string = ''
            if ingr.amount is not None:
                val_string = val_string + str(ingr.amount)
            # self.measure_type = measure_type
            # self.ingredient_type = ingredient_type
            if ingr.measure_type is not None:
                val_string = val_string +' '+str(ingr.measure_type)
            if ingr.ingredient_type is not None:
                val_string = val_string +' '+str(ingr.ingredient_type)
            if ingr.ingr is not None:
                val_string = val_string +' '+str(ingr.ingr)
            print(val_string)

    def __str__(self):
        print('==== ORIGINAL INGREDIENTS ====')
        [print(ingr) for ingr in self.recipe_ingredients]
        # for step in self.recipe_ingredients:
        #     for segment in step.split(".\n"):
        #         segment = segment.strip(" ")
        #         print("•", segment, "\n")
        print(' ')
        print('==== PARSED INGREDIENTS: ====')
        [print(ingr) if ingr is not None else print('') for ingr in self.ingredients]
        print(' ')
        print('==== CONVERTED RECIPE INGREDIENTS ====')
        self.pretty_print_ingredients()
        print(' ')
        print('==== STEPS ====')
        for step in self.recipe_steps:
            for segment in step.split("."):
                segment = segment.strip(" ")
                print("•", segment, "\n")
        # [print("segment") for segment in step.split(",") for step in self.recipe_steps]
        print(' ')
        print('==> PRIMARY_COOKING_METHOD: {}'.format(self.print_list(list(self.primary_methods))))

        print('==> SECONDARY_COOKING_METHOD: {}'.format(self.print_list([m for m in self.secondary_methods])))
        print('==> TOOLS: {}'.format(self.print_list([m for m in self.tools])))
        return ''
    def print_list(self, lst):
        return ', '.join(lst)
        # print(lst)
        # print(len(lst))
        # returnstr = ''
        # for i in range(len(lst)):
        #     print('i:',i)
        #     print(lst[i])
        #
        #     if i < len(lst):
        #         returnstr = returnstr + ' ' + lst[i] + ','
        #     else:
        #         returnstr = returnstr + ' ' + lst[i]
        # return returnstr
def main():
    pass
    #Recipe()


if __name__ == "__main__":
    main()
