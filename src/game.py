from datetime import datetime


class Game:
    def __init__(self, li_tag):
        self.li_tag = li_tag
        self.when_format = "%d/%m/%Y %H:%M:%S"
        self.info = {}
        self.build_info()

    def __str__(self):
        return str(self.info)

    def __bool__(self):
        return bool(self.info.get("hosting", None) is not None
                    and self.info.get("visiting", None) is not None)

    @property
    def when(self):
        return datetime.strptime(self.info["when"], self.when_format)

    def format_when(self, dt):
        return dt.strftime(self.when_format)

    def build_info(self):
        self.add_when()
        self.add_pretty_when()
        self.add_teams()

    def add_when(self):
        day_month = self.li_tag.find("span", class_="week").contents[0]
        time = self.li_tag.find("span", class_="hour").contents[0].replace("h", "")
        data = f"{day_month}/{datetime.today().year} {time}"
        pattern = "%d/%m/%Y %H:%M"
        self.info["when"] = self.format_when(datetime.strptime(data, pattern))

    def add_pretty_when(self):
        self.info["pretty_when"] = self.when.strftime("%d/%m %H:%M")

    def add_teams(self):
        teams = self.li_tag.find("div", class_="title-team").find_all(attrs={"itemprop": "name"})
        if teams:
            self.info["hosting"] = teams[0].contents[0]
            self.info["visiting"] = teams[1].contents[0]
