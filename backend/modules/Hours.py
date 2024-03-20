# hours class

class Hours:

    def __init__(self, day: str, openHour: int, openMinute: int, closeHour: int, closeMinute: int) -> None:
        self.openDay = day
        self.timeOpenHour = openHour
        self.timeOpenMinute = openMinute
        self.timeCloseHour = closeHour
        self.timeCloseMinute = closeMinute