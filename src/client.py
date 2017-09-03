import packets

class Client():

    def __init__(self, conn, addr, ship):
        self.conn = conn
        self.addr = addr
        self.ship = ship
        self.keys = {"up":False, "down":False, "left":False, "right":False, "space":False}

        