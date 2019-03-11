# Natural Language Powered Recipe Parsing and Transformation

This is a NLP oriented parser that applies natural language oriented semantic/extraction methods to parse recipes from the [allrecipes.com](https://www.allrecipes.com/) website. We are able to extract (from the webpage) the ingredients, the steps, the primary, secondary methods and the tools used in the recipe.

1. ### Installation:
      1. Clone the repository on your local machine with `git clone https://github.com/rhettdsouza13/Recipe-NLP.git`
      2. Run the package installer with the command `sh package.sh` if BeautifulSoup and unidecode dependancies are not met.

2. ### Running The Parser/Transformer:
      1. Open a CLI of your choice.
      2. Navigate to the `src` folder in the repository.
      3. Run `python run.py`.

3. ### Using the Interface:
      1. Enter the recipe url from `allrecipes.com`.
      2. Follow the CLI instructions that are printed on the screen to make the appropriate transformations to the recipe.
      3. The appropriate transformation and instruction codes have to be entered at the `:` command prompt.
