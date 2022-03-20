class ObjectPositions:
    def __init__(self):
        self.player = ()
        self.mobs = {}
        self.player_x_size = 20
        self.player_y_size = 20

    def set_position(self, object_type, pos_x, pos_y, mob_id=0):
        if object_type == 'player':
            self.player = (pos_x, pos_y)
        if object_type == 'mob':
            self.mobs[mob_id] = (pos_x, pos_y)

    def del_object(self, object_type, obj_id):
        if object_type == 'mob':
            self.mobs.pop(obj_id, None)

    def detect_collisions(self):
        collided = []
        for mob_id, coords in self.mobs.items():
            if (abs(coords[0]) <= self.player[0] + self.player_x_size and \
                abs(coords[0]) >= self.player[0] - self.player_x_size)\
                and (abs(coords[1]) <= self.player[1] + self.player_y_size and \
                     abs(coords[1]) >= self.player[1] - self.player_y_size):
                collided.append(mob_id)
        return collided