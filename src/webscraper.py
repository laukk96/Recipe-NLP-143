import requests
from bs4 import BeautifulSoup


def scrape(url):
    print(url)
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())
        # print(list(soup.children))
        tmp_lst = soup.find_all(class_="checkList__line")
        ingredients = set()
        for item in tmp_lst:
            tmp = tmp_lst[0].text.lstrip().rstrip()
            ingredients.add(tmp)

        print(ingredients)

        # print(tmp_lst[0])
        print(type(soup))
    else:
        print('BAD REQUEST status:{1} WITH URL {0}'.format(url, page.status_code))


def main():
    list_of_urls = [
        'https://www.allrecipes.com/recipe/220560/kashmiri-lamb/?internalSource=staff%20pick&referringId=233&referringContentType=Recipe%20Hub&clickId=cardslot%206',
        'https://www.allrecipes.com/recipe/221131/baked-buffalo-chicken-dip/?internalSource=hub%20recipe&referringContentType=Search',
        'https://www.allrecipes.com/recipe/21176/baked-dijon-salmon/?internalSource=staff%20pick&referringId=1642&referringContentType=Recipe%20Hub',
        'https://www.allrecipes.com/recipe/25016/coconut-macaroon-brownies/?internalSource=streams&referringId=838&referringContentType=Recipe%20Hub&clickId=st_trending_b',
        'https://www.allrecipes.com/recipe/12009/creamy-cajun-chicken-pasta/?internalSource=hub%20recipe&referringContentType=Search&clickId=cardslot%202']

    for url in list_of_urls[1:2]:
        scrape(url)


if __name__ == "__main__":
    main()
