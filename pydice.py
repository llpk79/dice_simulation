from pymunk import Space, Segment, Poly, Body
from random import randint
import matplotlib.pyplot as plt


class DicePhysics:

    def __init__(self):
        # Setup space and dice variables.
        print('init')
        self.space = Space()
        self.space.gravity = 0, 0
        self.space.damping = 0.9  # Dice will lose velocity * (1 - damping)/sec. Imitates top-down physics.
        self.size = 10, 10
        self.density = 0.1
        self.elasticity = 0.5  # Bounciness.
        self.body_dict = {}
        self.box_dict = {}

        # Create an area to throw dice in.
        # Set the coordinates for the ends of walls.
        self.left_wall = Segment(self.space.static_body, (0, 0), (60, 0), 1)
        self.left_wall.collision_type = 2
        self.left_wall.elasticity = 0.5
        self.space.add(self.left_wall)

        self.bottom = Segment(self.space.static_body, (0, 0), (0, 120), 1)
        self.bottom.collision_type = 2
        self.bottom.elasticity = 0.5
        self.space.add(self.bottom)

        self.right_wall = Segment(self.space.static_body, (0, 120), (60, 120), 1)
        self.right_wall.collision_type = 2
        self.right_wall.elasticity = 0.5
        self.space.add(self.right_wall)

        self.top = Segment(self.space.static_body, (60, 0), (60, 120), 1)
        self.top.collision_type = 2
        self.top.elasticity = 0.5
        self.space.add(self.top)

        # Setup collision handlers.
        # Die on die collisions.
        self.handle = self.space.add_collision_handler(1, 1)
        self.handle.begin = self.touch_block
        # Die on wall collisions.
        self.handle1 = self.space.add_collision_handler(1, 2)
        self.handle1.begin = self.touch_wall

    # Make some dice models.
    def make_box(self):
        body = Body()
        body.position = 5, 5
        box = Poly.create_box(body, size=self.size)
        box.density = self.density
        box.collision_type = 1
        box.elasticity = self.elasticity
        return box

    # Get a notification when we hit a wall or dice bounce off each other.
    def touch_block(self, arbiter, space, stuff):
        print('block')
        return True

    def touch_wall(self, arbiter, space, stuff):
        print('wall')
        return True

    def add_dice(self, num_dice):
        # Add dice to box_dict as we make em.
        self.box_dict = {i: self.make_box() for i, position in enumerate(range(num_dice))}

        # Need access to bodies as well.
        self.body_dict = {key: box.body for key, box in self.box_dict.items()}

        # Dice are boxes and their bodies, add them to the space.
        for box, body in zip(self.box_dict.values(), self.body_dict.values()):
            self.space.add(box, body)

    def start_dice(self):
        # Get things moving.
        for shape in self.space.shapes:
            self.space.step(0.005)
            # Adjust the range of x and/or y randint(s) to change the trajectory of the dice.
            shape.body.apply_impulse_at_local_point((randint(450, 600), randint(750, 900)))  # body.apply...point(x, y)

    def roll_dice(self):
        # For plotting dice movement.
        colors = {0: 'bo', 1: 'go', 2: 'co', 3: 'yo', 4: 'ko', 5: 'ro'}
        dice = []
        for _ in range(len(self.box_dict)):
            dice.append(list())

        # Track dice until they slow down.
        while any([abs(body.velocity.int_tuple[1]) > 10 for body in self.body_dict.values()]):
            # Move things along a bit.
            self.space.step(1/60)
            for i, box in enumerate(self.body_dict.values()):
                # Keep a record of dice movement and plot new positions.
                dice[i].append(box.position.int_tuple)
                plt.plot(box.position.int_tuple[1], box.position.int_tuple[0], colors[i])

        # Clear the space.
        self.space.remove(self.space.shapes)
        plt.show()
        return dice
