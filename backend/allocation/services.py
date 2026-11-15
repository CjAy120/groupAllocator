
import random

from django.db import transaction

from .models import Group, Student, ReservedIndex


class AllocationError(Exception):
    pass


class DuplicateIndexError(AllocationError):
    pass


@transaction.atomic
def register_student(full_name, index_number):
    full_name = " ".join(full_name.split())
    index_number = index_number.strip().upper()

    if not full_name:
        raise AllocationError("Full name is required.")

    if not index_number:
        raise AllocationError("Index number is required.")

    # Lock all groups so simultaneous registrations
    # cannot allocate the same remaining place.
    groups = list(
        Group.objects.select_for_update().order_by("number")
    )

    if Student.objects.filter(index_number=index_number).exists():
        raise DuplicateIndexError(
            "This index number has already been registered."
        )

    # Check whether this student has a reserved group.
    reservation = (
        ReservedIndex.objects
        .select_for_update()
        .select_related("group")
        .filter(index_number=index_number)
        .first()
    )

    if reservation:
        selected_group = next(
            (group for group in groups if group.pk == reservation.group_id),
            None
        )

        if selected_group is None:
            raise AllocationError("The reserved group does not exist.")

        if selected_group.students.count() >= selected_group.capacity:
            raise AllocationError(
                "The reserved group has no remaining capacity."
            )

        student = Student.objects.create(
            full_name=full_name,
            index_number=index_number,
            group=selected_group,
        )

        reservation.delete()

        return student

    # Find groups with places that are not reserved
    # for other students.
    available_groups = []

    for group in groups:
        registered = group.students.count()
        reserved = group.reserved_indices.count()

        if registered + reserved < group.capacity:
            available_groups.append(group)

    if not available_groups:
        raise AllocationError(
            "Registration is closed. All group places are occupied or reserved."
        )

    # Random selection among eligible groups.
    selected_group = random.choice(available_groups)

    student = Student.objects.create(
        full_name=full_name,
        index_number=index_number,
        group=selected_group,
    )

    return student
