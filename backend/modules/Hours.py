# hours class

class Hours:
    def __init__(self, day: str, openHour: int, openMinute: int, closeHour: int, closeMinute: int) -> None:
        self.openDay = day
        self.timeOpenHour = openHour
        self.timeOpenMinute = openMinute
        self.timeCloseHour = closeHour
        self.timeCloseMinute = closeMinute
    
    # Getter methods
    def getOpenDay(self) -> str: return self.openDay
    def getTimeOpenHour(self) -> int: return self.timeOpenHour
    def getTimeOpenMinute(self) -> int: return self.timeOpenMinute
    def getTimeCloseHour(self) -> int: return self.timeCloseHour
    def getTimeCloseMinute(self) -> int: return self.timeCloseMinute
    
    # Setter methods
    def setOpenDay(self, day: str) -> None: self.openDay = day
    def setTimeOpenHour(self, hour: int) -> None: self.timeOpenHour = hour
    def setTimeOpenMinute(self, minute: int) -> None: self.timeOpenMinute = minute
    def setTimeCloseHour(self, hour: int) -> None: self.timeCloseHour = hour
    def setTimeCloseMinute(self, minute: int) -> None: self.timeCloseMinute = minute
