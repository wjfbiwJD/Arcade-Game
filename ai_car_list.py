import arcade
import random
from ai_car import AICar
from constants import CAR_SCALE
from pyglet.graphics import Batch
import logging

logger = logging.getLogger("arcade")


class AICarList(arcade.SpriteList):

    def __init__(self, 
                 num_cars: int, 
                 checkpoints: dict[int, arcade.SpriteList], 
                 image_filename: str, 
                 *args, 
                 cur_checkpoint: int=0, 
                 scale: float=CAR_SCALE, 
                 spawnpoint: tuple[int, int]=None, 
                 movements_per_iteration: int=15000,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.num_cars = num_cars
        self.checkpoints = checkpoints
        self.distances = self._get_distances_between_checkpoints()
        self.image_filename = image_filename
        self.scale = scale
        self.cur_checkpoint = cur_checkpoint
        self.spawnpoint = spawnpoint if spawnpoint is not None else (0, 0)

        self.generation = 0
        self.best_movements = None
        self.best_progress = 0.0
        self.generations_without_improvement = 0

        self.movements_per_iteration = movements_per_iteration
        self.car_text_batch = Batch()

    def _get_ordered_checkpoint_keys(self) -> list:
        """Return checkpoint keys ordered numerically (as strings) when possible."""
        keys = list(self.checkpoints.keys())
        try:
            keys = sorted(keys, key=lambda k: int(k))
        except Exception:
            keys = sorted(keys)
        return keys

    def _get_distances_between_checkpoints(self) -> list[float]:
        """Return distances between consecutive checkpoint centers in order; includes last->first for lap closure."""
        ordered = self._get_ordered_checkpoint_keys()
        distances = []
        if len(ordered) < 2:
            return distances
        centers = []
        for key in ordered:
            sprite_list = self.checkpoints.get(key, arcade.SpriteList())
            centers.append(self._get_checkpoint_average_position(sprite_list))
        for i in range(len(centers)):
            a = centers[i]
            b = centers[(i + 1) % len(centers)]
            distances.append(arcade.math.get_distance(*a, *b))
        return distances

    def _get_checkpoint_average_position(self, sprite_list: arcade.SpriteList) -> tuple[float, float]:
        """ Returns the average position of a given sprite list. Returns (0,0) for empty lists. """
        x = 0.0
        y = 0.0
        num_pos = len(sprite_list)

        if num_pos == 0:
            return (0.0, 0.0)

        for sprite in sprite_list:
            x += sprite.position[0]
            y += sprite.position[1]

        x /= num_pos
        y /= num_pos
        return (x, y)
    
    def generate_cars(self, spawnpoint: tuple[int, int] =(0, 0)):
        self.spawnpoint = spawnpoint
        for _ in range(self.num_cars):
            car = AICar(self.cur_checkpoint, self.checkpoints, self.image_filename, scale=self.scale, position=spawnpoint, num_movements=self.movements_per_iteration)
            car._debug_text = arcade.Text(f"Car #{car.car_number}", car.position[0], car.position[1] + 20, arcade.color.WHITE, 12, batch=self.car_text_batch)
            self.append(car)


    def _movements_to_list(self, movements_source) -> list:
        """Convert movements (list or generator) to a concrete list of frames sized to movements_per_iteration.
        Pads with [0] (idle) frames if shorter, or truncates if longer.
        """
        if movements_source is None:
            return [[0] for _ in range(self.movements_per_iteration)]

        # If it's a generator (like AICar.generate_movements), turn into a list
        try:
            if isinstance(movements_source, list):
                seq = [[f for f in frame] for frame in movements_source]
            else:
                seq = [[f for f in frame] for frame in list(movements_source)]
        except Exception:
            # Fallback to an empty idle sequence
            seq = []

        if len(seq) > self.movements_per_iteration:
            seq = seq[: self.movements_per_iteration]
        else:
            # pad with idle frames
            while len(seq) < self.movements_per_iteration:
                seq.append([0])
        return seq

    def eval_generation(self):
        """Evaluate the completed generation and create the next generation."""
        if len(self) == 0 or not all(not car.replay_movements for car in self):
            return

        self.generation += 1

        population = sorted(self, key=self.get_progress, reverse=True)
        best_car = population[0]
        best_progress = self.get_progress(best_car)

        if best_progress > self.best_progress:
            self.best_progress = best_progress
            self.generations_without_improvement = 0
        else:
            self.generations_without_improvement += 1

        logger.info(
            f"Best car on generation #{self.generation}: "
            f"Car #{best_car.car_number} with {best_progress:.2f}% progress. "
            f"Generations without improvement: "
            f"{self.generations_without_improvement}"
        )

        best_sequence = self._movements_to_list(
            best_car.recorded_movements
            if best_car.recorded_movements
            else best_car.movements
        )

        if self.generations_without_improvement >= 10:
            preserved_fraction = 0.50
            mutation_rate = 0.15
        elif self.generations_without_improvement >= 5:
            preserved_fraction = 0.65
            mutation_rate = 0.10
        else:
            preserved_fraction = 0.75
            mutation_rate = 0.05

        completed_frames = len(best_car.recorded_movements)
        mutation_start = int(completed_frames * (1.0 - preserved_fraction))

        # Keep the best car's sequence completely unchanged.
        best_car.reset(
            self.spawnpoint,
            0,
            new_movements=[[action for action in frame] for frame in best_sequence]
        )

        # Mutate copies for every other car.
        for car in population[1:]:
            child = [[action for action in frame] for frame in best_sequence]

            self.mutate(
                child,
                car.rng,
                mutation_start,
                mutation_rate
            )

            car.reset(
                self.spawnpoint,
                0,
                new_movements=child
            )

        self.distances = self._get_distances_between_checkpoints()
    
    def mutate(self, seq, rng, start_index=0, mutation_rate=0.05):
        """Mutates movement and steering while favoring controlled driving."""

        start_index = max(0, min(start_index, len(seq)))

        # Movement action probabilities favor forward driving.
        movement_choices = [1, 1, 1, 1, 2, 2, 3]
        steering_choices = [0, 4, 5]

        # Mutate movement in continuous segments.
        def mutate_movement():
            i = start_index

            while i < len(seq):
                if rng.random() < mutation_rate:
                    duration = rng.randint(8, 60)
                    action = rng.choice(movement_choices)

                    for j in range(i, min(i + duration, len(seq))):
                        frame = seq[j]
                        frame[:] = [a for a in frame if a not in (1, 2, 3, 6)]

                        if action != 0:
                            frame.append(action)

                    i += duration
                else:
                    i += 1

        # Introduce continuous steering segments independently of existing turns.
        def mutate_steering():
            i = start_index

            while i < len(seq):
                if rng.random() < mutation_rate * 2:
                    duration = rng.randint(10, 35)
                    action = rng.choice(steering_choices)

                    for j in range(i, min(i + duration, len(seq))):
                        frame = seq[j]
                        frame[:] = [a for a in frame if a not in (4, 5)]

                        if action != 0:
                            frame.append(action)

                    i += duration
                else:
                    i += 1

        mutate_movement()
        mutate_steering()

        # Resolve incompatible actions and prevent idle frames.
        for frame in seq[start_index:]:
            if 6 in frame:
                frame[:] = [6]
            else:
                frame[:] = [a for a in frame if a != 0]

                if not any(a in (1, 2, 3) for a in frame):
                    frame.append(1)

                if not any(a in (4, 5) for a in frame):
                    pass

    def get_progress(self, car: AICar) -> float:
        """Returns a car's overall progress around the course as a percentage.

        Progress is computed by summing the traveled distance along completed segments
        plus the fraction completed on the current segment, divided by total course length.
        """
        if not self.distances:
            return 0.0

        ordered_keys = self._get_ordered_checkpoint_keys()
        total_course_length = sum(self.distances)
        if total_course_length == 0:
            return 0.0

        # Map the car's numeric checkpoint to an index in the ordered keys
        try:
            cur_key = str(car.cur_checkpoint)
            cur_index = ordered_keys.index(cur_key)
        except Exception:
            # Fallback: if mapping fails, try using 0
            cur_index = 0

        # Sum lengths of fully passed segments (segments before cur_index)
        passed_length = sum(self.distances[i] for i in range(cur_index))

        # Distance to next checkpoint
        distance_to_next = car.check_distance()
        segment_length = self.distances[cur_index]
        if segment_length <= 0:
            frac = 0.0
        else:
            # fraction completed along this segment. clamp between 0..1
            frac = max(0.0, min(1.0, 1.0 - (distance_to_next / segment_length)))

        traveled = passed_length + (segment_length * frac)
        progress = (traveled / total_course_length) * 100.0
        return max(0.0, min(100.0, progress))