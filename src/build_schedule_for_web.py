from schedule_builder import ScheduleBuilder


def main():
    builder = ScheduleBuilder()
    builder.add_html_games()
    builder.save_hitorical_games_file()
    builder.save_recent_games_file()


if __name__ == "__main__":
    main()
