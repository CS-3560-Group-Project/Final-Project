# location class

class Location:
    
    def __init__(self, building: int, room: int) -> None:
        self.buildingNumber = building
        self.roomNumber = room
    
    # Getter methods
    def getBuildingNumber(self) -> int: return self.buildingNumber
    def getRoomNumber(self) -> int: return self.roomNumber
    
    # Setter methods
    def setBuildingNumber(self, building: int) -> None: self.buildingNumber = building
    def setRoomNumber(self, room: int) -> None: self.roomNumber = room
