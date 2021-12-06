from json_games_builder import JsonGamesBuilder


def main():
    builder = JsonGamesBuilder()
    builder.add_html_games()
    builder.save_hitorical_games_file()
    builder.save_recent_games_file()


if __name__ == "__main__":
    main()
