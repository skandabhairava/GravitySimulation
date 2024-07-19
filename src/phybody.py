from pygame.math import Vector2
import random

# const
G = 10

# DAMPENING FACTORS AS SYSTEM LOOSES ENERGY TO HEAT
BOUNCE_DAMP = 0.5
GRAV_DAMP = 0.3

class Body:
    def __init__(self, id: int, color: tuple[int, int, int], size: int, mass: float, pos: Vector2, velocity: Vector2) -> None:

        self.id: int = id
        self.color: tuple[int, int, int] = color
        self.size: int = size
        self.mass: float = mass
        self.pos: Vector2 = pos

        self.velocity: Vector2 = velocity
        self.acceleration: Vector2 = Vector2(0, 0)

    def update(self):
        self.pos += self.velocity
        self.velocity += self.acceleration

    def gravity_calc(self, all_bodies: list['Body']):

        force: Vector2 = Vector2(0, 0)

        for body in all_bodies:
            if body.id == self.id:
                continue

            dist = self.pos.distance_to(body.pos)
            if dist < (self.size + body.size):
                # HANDLE COLLISION

                dist = self.size + body.size

                new_1_velocity = ((abs(self.mass - body.mass)/(self.mass + body.mass) * self.velocity) + (2 * body.mass * body.velocity)/(self.mass + body.mass)) * (1 - BOUNCE_DAMP)
                new_2_velocity = ((2 * self.mass * self.velocity)/(self.mass + body.mass) + (abs(body.mass - self.mass)/(self.mass + body.mass))*body.velocity) * (1 - BOUNCE_DAMP)

                direction = body.pos - self.pos
                direction_norm = direction.normalize()
                midpoint = ((direction)/2) + self.pos
                
                body.pos = midpoint + (direction_norm * (body.size))
                self.pos = midpoint - (direction_norm * (self.size))

                body.velocity = new_2_velocity if new_2_velocity.length() > 0.5 else Vector2(0, 0)
                self.velocity = new_1_velocity if new_1_velocity.length() > 0.5 else Vector2(0, 0)
            elif dist > (self.size + body.size) :
                # GRAVITY
                force += ((G * self.mass * body.mass)/( (dist**2) )) * (body.pos - self.pos).normalize()
                
            if random.random() < 0.5:
                self.update()
                body.update()
            else:
                body.update()
                self.update()


        self.acceleration = ((1 - GRAV_DAMP) * force)/self.mass
        self.update()