import arcade
import random
from ai_car import AICar
import ai_car
from constants import CAR_SCALE

class AICarList(arcade.SpriteList):

    def __init__(self, 
                 num_cars: int, 
                 checkpoints: dict[int, arcade.SpriteList], 
                 image_filename: str, 
                 *args, 
                 cur_checkpoint: int=0, 
                 scale: float=CAR_SCALE, 
                 spawnpoint: tuple[int, int]=None, 
                 movements_per_iteration: int=1000,
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
        self.movements_per_iteration = movements_per_iteration


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

    def _get_checkpoint_average_position(self, sprite_list: arcade.SpriteList) -> tuple[float, float]:                 # Added this
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
            self.append(AICar(self.cur_checkpoint, self.checkpoints, self.image_filename, scale=self.scale, position=spawnpoint, num_movements=self.movements_per_iteration))


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
        """ Evaluates if the current generation of AI cars has completed their movements and advances to the next generation if so.
        Implements a simple genetic algorithm: elitism, selection from top performers, crossover and mutation.
        """
        all_done = len(self) > 0 and all(not car.replay_movements for car in self)
        if not all_done:
            return

        self.generation += 1

        # Compute fitness for all cars
        scored = [(car, self.get_progress(car)) for car in self]
        scored.sort(key=lambda x: x[1], reverse=True)

        best_car, best_progress = scored[0]
        print(f"Best car on generation #{self.generation} is: Car #{best_car.car_number} with ~{best_progress}% progress.")

        population = [c for c, _ in scored]
        fitnesses = [f for _, f in scored]

        # Parameters
        population_size = len(population)
        elite_count = max(1, population_size // 10)  # keep top 10% unchanged
        parent_pool = max(2, population_size // 4)   # top 25% form parent pool
        mutation_rate = 0.05

        # Prepare parent movement sequences
        parent_seqs = [self._movements_to_list(p.recorded_movements if p.recorded_movements else p.movements) for p in population[:parent_pool]]

        # Replace population with new generation
        new_sequences = []

        # Elitism: carry forward top performers unchanged
        for i in range(elite_count):
            new_sequences.append(self._movements_to_list(population[i].recorded_movements if population[i].recorded_movements else population[i].movements))

        # Helper to perform single-point crossover
        def crossover(seq_a, seq_b):
            if not seq_a or not seq_b:
                return seq_a.copy() if seq_a else seq_b.copy()
            point = random.randint(1, len(seq_a) - 1)
            child = [frame.copy() for frame in (seq_a[:point] + seq_b[point:])]
            return child

        # Generate remaining children
        while len(new_sequences) < population_size:
            a_idx = random.randrange(parent_pool)
            b_idx = random.randrange(parent_pool)
            # avoid identical parent pairing too often
            if a_idx == b_idx and parent_pool > 1:
                b_idx = (b_idx + 1) % parent_pool
            parent_a = parent_seqs[a_idx]
            parent_b = parent_seqs[b_idx]
            child = crossover(parent_a, parent_b)
            new_sequences.append(child)

        # Assign new sequences to cars with mutation using each car's RNG for determinism
        for car, seq in zip(population, new_sequences):
            # mutate in-place
            for fi in range(len(seq)):
                frame = seq[fi]
                for ai in range(len(frame)):
                    if car.rng.random() < mutation_rate:
                        frame[ai] = car.rng.choice([0, 1, 2, 3, 4, 5, 6])
                # with small chance, occasionally add or remove an action from the frame
                if car.rng.random() < (mutation_rate * 0.2):
                    if car.rng.random() < 0.5 and len(frame) > 1:
                        # remove a random action
                        idx = car.rng.randrange(len(frame))
                        frame.pop(idx)
                    else:
                        # add a random action
                        frame.append(car.rng.choice([1, 2, 3, 4, 5, 6]))
            car.reset(self.spawnpoint, 0, new_movements=seq)

        # Recompute distances in case checkpoints changed (kept for safety)
        self.distances = self._get_distances_between_checkpoints()

            
    def get_progress(self, car: AICar) -> float:                 # Added this
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


    def debug_print(self):
        """ Prints the current state of the AI cars for debugging purposes """
        print(f"Generation: {self.generation}")
        for car in self:
            print(f"Car #{car.car_number}: Checkpoint {car.cur_checkpoint}, "
                  f"Replay: {car.replay_movements}, Recorded Movements: {len(car.recorded_movements)}, Movements Remaining: {len(car.movements)}, "
                  f"Progress: {self.get_progress(car):.2f}%")