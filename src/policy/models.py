from django.db import models
from django.template.defaultfilters import slugify
from core.db import TimeStampedModel
from customers.models import Customer


class Coverage(TimeStampedModel):
    """
    list the type of policy provided
    """
    title = models.CharField(max_length=100, blank=False, null=False)
    type = models.SlugField(null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    cover = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
    # overide the save method to slugify title
    def save(self, *args, **kwargs):
        if not self.type:
            self.type = slugify(self.title)
        return super().save(*args, **kwargs)


class AgePremiumDifferential(TimeStampedModel):
    """
    Coverage discounts based on age
    :param amount: negative value for reduction, positive value for increament
    """
    start_age = models.IntegerField(blank=False, null=False)
    end_age = models.IntegerField(blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    coverage = models.ForeignKey(Coverage, related_name="age_premium_differential", blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.amount)} differential on {self.coverage}'
    

class Policy(TimeStampedModel):
    """
    Policies customers have applied for
    """
    STATE = (
        ('new', 'New'),
        ('quoted', 'Quoted'),
        ('bound', 'Bound'),
        ('accepted', 'Accepted'),
        ('active', 'Active')
    )
    coverage = models.ForeignKey(Coverage, blank=False, null=False, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, related_name="policy", blank=False, null=False, on_delete=models.PROTECT)
    state = models.CharField(max_length=10, blank=False, null=False, choices=STATE)

    def __str__(self):
        return f'{self.coverage} policy for {self.customer}'

    @property
    def premium(self):
        # check if there is an age premium differential on the coverage
        if self.coverage.age_premium_differential.count():
            # find discount that applies to the customer age
            differential = self.coverage.age_premium_differential.filter(start_age__lte=self.customer.age, end_age__gte=self.customer.age)
            if differential.count():
                return self.coverage.premium + differential[0].amount
        return self.coverage.premium

    @property
    def cover(self):
        return self.coverage.cover
    

class PolicyHistory(TimeStampedModel):
    """
    History of customer policies
    """
    state = models.CharField(max_length=10, blank=False, null=False)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.policy} is {self.state}'
    