from django.db import models
import datetime

class Contestant(models.Model):
    first_name = models.CharField("First Name", max_length=25)
    middle_name = models.CharField("Middle Name", max_length=25, blank=True)
    last_name = models.CharField("Last Name", max_length=25)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    gender = models.CharField("Gender", max_length=1,
                                      choices=GENDER_CHOICES,
                                      default=MALE)

    age = models.IntegerField("Age")

    def __str__(self):
        mid = ""
        if self.middle_name != "":
            mid = self.middle_name[0] + " "
        return (self.first_name + " " + mid + self.last_name).strip()

    def getBiggestFish(self):
        self.biggest_fish = self.getFirstFish('-weight')

    # def getSmallestFish(self):
        # self.smallest_fish = self.getFirstFish('', 'weight')

    def getFirstFish(self, orderString):
        results = self.fish_set
        results = results.order_by(orderString)
        if len(results) > 0:
             return results[:1][0]
        else:
            return None

class Fish(models.Model):
    contestant = models.ForeignKey(Contestant)
    
    weight = models.FloatField("Weight")
    weigh_time = models.DateTimeField("Weigh Time", auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.weigh_time = datetime.datetime.now()
        return super(Fish, self).save(*args, **kwargs)

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return str(self.weight)
    
    
    
