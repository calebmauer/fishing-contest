from fishingcontest.models import Contestant, Fish
import random

random.seed()

def createTestFisher(attribs):
	""" Add a contestant to the database. Adds a random number
	of fish with random weights. """
    rand_age = random.randrange(3, 16)
    c = Contestant.objects.create(first_name=attribs[0],
                                  middle_name=attribs[1],
                                  last_name=attribs[2],
                                  gender=attribs[3],
                                  age=rand_age)

    n_fish = random.randrange(0, 8)
    for fish in range(n_fish):
        randomweight = random.randrange(0, 1000)
        randomweight = float(randomweight)
        if randomweight == 0.0:
            None
        else:
            c.fish_set.create(weight=randomweight/100)

def createTestFishers():
    MALE = Contestant.MALE
    FEMALE = Contestant.FEMALE
    
	# List of contestants to add to the database
    list(map(createTestFisher,
             (("Caleb", "", "Mayor", MALE),
             ("Cody", "", "Appleseed", MALE),
             ("Connor", "", "Mayor", MALE),
             ("Fish", "", "Man", MALE),
             ("Fisher", "", "Man", MALE),
             ("Agent", "Two", "Smith", MALE),
             ("Fish", "Two", "Man", MALE),
             ("Fisher", "", "Man", MALE),
             ("The", "", "One", MALE),
             ("Jim", "John", "Jimmy", MALE),
             ("George", "", "Washington", MALE),
             ("Abe", "", "Lincoln", MALE),
             ("Uly", "", "Grant", MALE),
             ("John", "The", "Fisherman", MALE),
             ("Bernie", "", "Mac", MALE),
             ("Freddie", "Two", "Mae", MALE),
             ("Derek", "Two", "Seuss", MALE),
             ("Albert", "", "Einstein", MALE),
             ("Harry", "", "Potter", MALE),
             ("Barry", "Two", "Plotter", MALE),
             ("John", "Two", "Grisham", MALE),
             ("Robert", "Two", "Jordan", MALE),
             ("Patrick", "Kvothe", "Rothfuss", MALE),
             ("Ron", "", "Weasley", MALE),
             ("Brandon", "Two", "Sanderson", MALE),
             
             ("Shirley", "", "Temple", FEMALE),
             ("Shirley2", "", "Temple2", FEMALE),
             ("Princess", "", "Peach", FEMALE),
             ("Joanna", "", "Dark", FEMALE),
             ("Pam", "", "Steeple", FEMALE),
             ("Missy", "", "Mosque", FEMALE),
             ("Harper", "", "Meiser", FEMALE),
             ("Miss", "", "Piggy", FEMALE),
             ("Mary", "", "Lincoln", FEMALE),
             ("Eleanor", "The", "Roosevelt", FEMALE),
             ("Betsy", "", "Ross", FEMALE),
             ("Anabell", "", "Lee", FEMALE),
             ("Jen", "", "Granholm", FEMALE),
             ("Sarah", "", "Palin", FEMALE),
             ("Jody", "", "Foster", FEMALE),
             ("Amy", "", "Schumer", FEMALE),
             ("Liz", "", "Farley", FEMALE),
             ("Anne", "", "McCafrey", FEMALE),
             ("Ursula", "K", "LeGuin", FEMALE),
             ("Samantha", "", "Bee", FEMALE),
             ("Prof", "", "McGonagal", FEMALE),
             ("Hermione", "", "Granger", FEMALE))))

createTestFishers()