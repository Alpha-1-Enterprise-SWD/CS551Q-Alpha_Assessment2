from django.db import models

class GPPractices(models.Model):
    practice_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    list_size = models.IntegerField()
    address = models.CharField(max_length=300)
    postcode = models.CharField(max_length=10)
    telephone = models.CharField(max_length=20)
    health_board = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

class GPDetails(models.Model):
    medical_council_number = models.CharField(max_length=10, primary_key=True)
    designation = models.CharField(max_length=100)
    forename = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=10, null=True, blank=True)
    surname = models.CharField(max_length=100)
    sex = models.CharField(max_length=50, null=True, blank=True)
    practice = models.ForeignKey('GPPractices', on_delete=models.CASCADE, related_name="gp")

    def __str__(self):
        return f"{self.forename} {self.surname}"
    
    class Meta:
        ordering = ["surname", "forename"]

class GPPopulations(models.Model):
    practice = models.ForeignKey('GPPractices', on_delete=models.CASCADE, related_name="populations")
    sex = models.CharField(max_length=10)
    ages00to04  = models.IntegerField(default=0)
    ages05to09  = models.IntegerField(default=0)
    ages10to14  = models.IntegerField(default=0)
    ages15to19  = models.IntegerField(default=0)
    ages20to24  = models.IntegerField(default=0)
    ages25to29  = models.IntegerField(default=0)
    ages30to34  = models.IntegerField(default=0)
    ages35to39  = models.IntegerField(default=0)
    ages40to44  = models.IntegerField(default=0)
    ages45to49  = models.IntegerField(default=0)
    ages50to54  = models.IntegerField(default=0)
    ages55to59  = models.IntegerField(default=0)
    ages60to64  = models.IntegerField(default=0)
    ages65to69  = models.IntegerField(default=0)
    ages70to74  = models.IntegerField(default=0)
    ages75to79  = models.IntegerField(default=0)
    ages80to84  = models.IntegerField(default=0)
    ages85plus  = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.practice.name} - {self.sex}"

    class Meta:
        unique_together = ["practice", "sex"]
        ordering = ["practice", "sex"]
