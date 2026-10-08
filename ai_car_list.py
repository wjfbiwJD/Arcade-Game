import arcade 
from ai_car import AICar
from constants import CAR_SCALE

class AICarList(arcade.SpriteList):

    # Modification #3
    def __init__(self, num_cars, checkpoints, image_filename, *args, cur_checkpoint=0, scale=CAR_SCALE, spawnpoint=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_cars = num_cars
        self.checkpoints = checkpoints
        self.image_filename = image_filename
        self.scale = scale
        self.cur_checkpoint = cur_checkpoint
        self.spawnpoint = spawnpoint if spawnpoint is not None else (0, 0)

        self.generation = 0
        self.best_movements = None
        # TODO: Inside of AICar, change tracking movements to True
        # Change how cars with movement tracking are updated; the idea is they can still be updated if tracking movements

    def generate_cars(self, spawnpoint: tuple[int, int] =(0, 0)):
        self.spawnpoint = spawnpoint
        for car in range(self.num_cars):
            self.append(AICar(self.cur_checkpoint, self.checkpoints, self.image_filename, scale=self.scale, position=spawnpoint))


    def eval_generation(self):
        """ Evaluates if the current generation of AI cars has completed their movements and advances to the next generation if so """
        all_done = len(self) > 0 and all(not car.replay_movements for car in self)
        if all_done:
            self.generation += 1
            for car in self:
                print() # all attrs of car
                car.reset(self.spawnpoint, 0)
                print() # all attrs of car
                # see what changed --> first time works, second time fails to print likely due to car.replay_movements(**this) or car.record_movements


            print(f"Generation {self.generation} completed. Resetting cars for next generation.")