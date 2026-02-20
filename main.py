from StoryMaker import StoryMaker
from FantasyHelper import FantasyHelper

def main():
    print(StoryMaker().get_api_url())
    print(StoryMaker().get_basic_prompt())
    print(StoryMaker().get_main_model())
    print(StoryMaker().get_fallback_model())
    pass


if __name__ == "__main__":
    main()
