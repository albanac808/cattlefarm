SEASON_MULTIPLIERS = {
    'spring': 1.2,
    'summer': 1.0,
    'autumn': 0.9,
    'winter': 0.8
}

class Mammal:
    def __init__(self, age, weight, health):
        self.age = age
        self.weight = weight
        self.health = 100
        self.food_consumed = 0

class Cattle(Mammal):
    def __init__(self, age, weight, breed_type):
        super().__init__(age, weight, 100)  # Pass 100 directly for health
        self.breed_type = breed_type
    
    def eat(self, food_amount):
        self.food_consumed += food_amount


class Bull(Cattle):
    def __init__(self, age, weight, breed_type):
        super().__init__(age, weight, breed_type)
        self.virility = 50
        self.recovery_time = 0  # days until ready again
        
    def milk(self, bucket):
        print("*ANGRY MOO*")
        print("The bull kicks down the barn door!")
        raise Exception("You tried to milk a bull. What were you expecting?")
        
    def can_breed(self):
        if self.recovery_time > 0:
            return False
        if self.health < 60:  # bulls need to be healthy too!
            return False
        return self.virility >= 50
        
    def breed(self):
        if not self.can_breed():
            raise Exception("Bull isn't quite UP for it right now")
        self.recovery_time = 3  # needs a few days to recover
        self.virility -= 10  # gets tired

class Cow(Cattle):
    def __init__(self, age, weight, breed_type, udder_count=4):
        super().__init__(age, weight, breed_type)
        self.udder_count = udder_count
        self.last_milking = 0
        self.is_pregnant = False
        self.pregnancy_days = 0
        self.GESTATION_PERIOD = 283  # constant

    def milk(self, bucket, season_multiplier=1.0):
        if self.age < 2:
            raise Exception("Too young to produce milk!")
            
        # Base milk production (liters)
        base_milk = (self.udder_count * 0.5)
        
        # Food bonus (more food = more milk)
        food_bonus = self.food_consumed * 0.1
        
        # Age penalty (older cows produce less)
        age_penalty = max(0, (self.age - 5) * 0.1)
        
        # Apply seasonal multiplier
        milk_produced = (base_milk + food_bonus - age_penalty) * season_multiplier
        
        bucket.add_milk(milk_produced)
        self.food_consumed = 0
        return milk_produced
    
    def update_pregnancy(self):
        if self.is_pregnant:
            self.pregnancy_days += 1
            if self.pregnancy_days >= self.GESTATION_PERIOD:
                # Time for the miracle of life!
                self.is_pregnant = False
                self.pregnancy_days = 0
                return True  # Signal that a calf is born
        return False

    def can_breed(self):
        if self.is_pregnant:
            raise Exception("This cow is already expecting!")
        if self.health < 70:
            raise Exception("Cow needs to be healthier for breeding")
        return True
        
    def breed(self, bull):
        if not bull.can_breed():
            return False
        if not self.can_breed():
            return False
        self.is_pregnant = True
        bull.breed()  # trigger bull's... recovery time
        return True


class MilkBucket:
    def __init__(self):
        self.capacity = 5.0  # liters
        self.current_volume = 0
        
    def add_milk(self, amount):
        if self.current_volume + amount > self.capacity:
            remaining_space = self.capacity - self.current_volume
            if remaining_space <= 0:
                raise Exception("Bucket is full! Need a new bucket!")
        self.current_volume += amount

    def empty(self):
        volume = self.current_volume
        self.current_volume = 0
        return volume
    

class CattleFarm:

    SEASON_MULTIPLIERS = {
        'spring': 1.2,
        'summer': 1.0,
        'autumn': 0.9,
        'winter': 0.8
    }
    
    def __init__(self, name):
        self.name = name
        self.cattle = []
        self.milk_storage = 0
        self.storage_capacity = 100  # liters
        self.daily_buckets = [MilkBucket(), MilkBucket(), MilkBucket()]
    
    def add_cattle(self, animal):
        if isinstance(animal, (Cow, Bull)):
            self.cattle.append(animal)
        else:
            raise Exception("This is a cattle farm, not a petting zoo!")
    
    def feed_all_cattle(self, food_amount):
        for animal in self.cattle:
            animal.eat(food_amount)
            print(f"Fed {food_amount}kg to {animal.__class__.__name__}")
    
    def milk_all_cows(self, season='summer'):
        print(f"=== Milking Time at {self.name} ===")
        current_bucket = 0
        multiplier = self.SEASON_MULTIPLIERS[season]
        
        for animal in self.cattle:
            if isinstance(animal, Cow):
                while True:
                    try:
                        if current_bucket >= len(self.daily_buckets):
                            self.daily_buckets.append(MilkBucket())
                        milk_amount = animal.milk(self.daily_buckets[current_bucket], multiplier)
                        print(f"Got {milk_amount:.1f}L from cow!")
                        self.milk_storage += milk_amount  # Add to storage here!
                        break
                    except Exception:
                        current_bucket += 1

    def sell_milk(self, price_per_liter):
        # First empty buckets into storage
        for bucket in self.daily_buckets:
            new_milk = bucket.empty()
            if self.milk_storage + new_milk > self.storage_capacity:
                raise Exception("Storage tank full! Call the milk truck!")
            self.milk_storage += new_milk
        
        # Calculate revenue
        revenue = self.milk_storage * price_per_liter
        self.milk_storage = 0  # Empty storage after sale
        return revenue
    
    def breed_cattle(self, cow, bull):
        if not isinstance(cow, Cow):
            raise Exception("First animal must be a cow!")
        if not isinstance(bull, Bull):
            raise Exception("Second animal must be a bull!")
        
        # Cow conditions
        if cow.is_pregnant:  # We'll need to add this attribute to Cow class
            raise Exception("No room at the inn!")
        if cow.health < 70:  # Arbitrary threshold - what do you think?
            raise Exception("Cow needs to be healthier to breed")
        if cow.age < 2:
            raise Exception("Cow is too young")
            
        # Bull conditions
        if bull.age < 2:
            raise Exception("Bull is too young")
        if bull.virility < 50:  # We'll need to add virility to Bull class
            raise Exception("Bull isn't feeling up to it today...")
            
        # Season check
        if self.current_season == 'summer':
            raise Exception("Too hot for romance!")
        
    def test_breeding(self):
        # get first cow and bull from farm's cattle
        cow = next((animal for animal in self.cattle if isinstance(animal, Cow)), None)
        bull = next((animal for animal in self.cattle if isinstance(animal, Bull)), None)
        
        if not cow or not bull:
            print("Need both a cow and bull for breeding!")
            return
        
        # Try breeding ONCE
        print("=== Testing Breeding Program ===")
        try:
            success = cow.breed(bull)  # Let the cow.breed() method handle everything
            if success:
                print("Successful breeding!")
                print(f"Bull virility: {bull.virility}")
                print(f"Bull recovery time: {bull.recovery_time}")
                print(f"Cow pregnant: {cow.is_pregnant}")
            else:
                print("Breeding failed: animals not ready")
        except Exception as e:
            print(f"Breeding failed: {e}")

    def update_day(self):
        for animal in self.cattle:
            if isinstance(animal, Bull) and animal.recovery_time > 0:
                animal.recovery_time -= 1
            elif isinstance(animal, Cow) and animal.is_pregnant:
                animal.pregnancy_days += 1

# TESTING CODE HERE!

if __name__ == "__main__":
    # Create the farm
    farm = CattleFarm("Happy Hooves Farm")
    
    # Add some initial animals
    farm.add_cattle(Cow(3, 1000, breed_type="Holstein"))
    farm.add_cattle(Bull(3, 1200, breed_type="Angus"))
    
    # Run through a few days
    print("=== Starting Breeding Program ===")
    farm.test_breeding()
    
    # Wait a few days
    print("\n=== Three Days Later ===")
    for _ in range(3):
        farm.update_day()
    
    # Try breeding again
    print("\n=== Second Breeding Attempt ===")
    farm.test_breeding()