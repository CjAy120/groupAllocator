
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Group(models.Model):
    number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(18)
        ]
    )

    capacity = models.PositiveSmallIntegerField(default=4)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(number__gte=1, number__lte=18),
                name="valid_group_number"
            ),
            models.CheckConstraint(
                condition=models.Q(capacity__gte=1, capacity__lte=4),
                name="valid_group_capacity"
            ),
        ]

    def __str__(self):
        return f"Group {self.number}"

    @property
    def student_count(self):
        return self.students.count()

    @property
    def is_full(self):
        return self.student_count >= self.capacity

    @property
    def reserved_count(self):
        return self.reserved_indices.count()

    @property
    def available_places(self):
        return max(
            0,
            self.capacity - self.student_count - self.reserved_count
        )


class ReservedIndex(models.Model):
    index_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="reserved_indices"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["index_number"]

    def save(self, *args, **kwargs):
        self.index_number = self.index_number.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.index_number} → Group {self.group.number}"


class Student(models.Model):
    full_name = models.CharField(max_length=150)

    index_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name="students"
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def save(self, *args, **kwargs):
        self.index_number = self.index_number.strip().upper()
        self.full_name = " ".join(self.full_name.split())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.index_number})"
