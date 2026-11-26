
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone

from .models import Group, Student, ReservedIndex


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ("full_name", "index_number", "registered_at")
    readonly_fields = ("registered_at",)
    show_change_link = True


class ReservedIndexInline(admin.TabularInline):
    model = ReservedIndex
    extra = 2
    fields = ("index_number",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "capacity",
        "get_student_count",
        "get_reserved_count",
        "get_available_places",
        "get_status",
    )

    ordering = ("number",)
    inlines = [ReservedIndexInline, StudentInline]

    @admin.display(description="Registered")
    def get_student_count(self, obj):
        return obj.students.count()

    @admin.display(description="Reserved")
    def get_reserved_count(self, obj):
        return obj.reserved_indices.count()

    @admin.display(description="Open places")
    def get_available_places(self, obj):
        return obj.available_places

    @admin.display(description="Status")
    def get_status(self, obj):
        if obj.available_places <= 0:
            return "Full / Reserved"
        return "Available"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "index_number",
        "group",
        "registered_at",
    )

    search_fields = ("full_name", "index_number")
    list_filter = ("group",)
    readonly_fields = ("registered_at",)
    ordering = ("group__number", "full_name")

    change_list_template = "admin/students_changelist.html"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "export-csv/",
                self.admin_site.admin_view(self.export_csv),
                name="students-export-csv",
            ),
        ]

        return custom_urls + urls

    def export_csv(self, request):
        students = Student.objects.select_related(
            "group"
        ).order_by(
            "group__number",
            "full_name"
        )

        response = HttpResponse(
            content_type="text/csv; charset=utf-8"
        )

        response["Content-Disposition"] = (
            f'attachment; filename="registered_students_'
            f'{timezone.now():%Y%m%d_%H%M%S}.csv"'
        )

        # Helps Excel recognize UTF-8 correctly.
        response.write("\ufeff")

        writer = csv.writer(response)

        writer.writerow([
            "Full Name",
            "Index Number",
            "Group",
            "Registration Date",
        ])

        previous_group = None

        for student in students:
            if (
                previous_group is not None
                and previous_group != student.group.number
            ):
                writer.writerow([])

            writer.writerow([
                student.full_name,
                student.index_number,
                student.group.number,
                student.registered_at,
            ])

            previous_group = student.group.number

        return response


@admin.register(ReservedIndex)
class ReservedIndexAdmin(admin.ModelAdmin):
    list_display = ("index_number", "group", "created_at")
    search_fields = ("index_number",)
    list_filter = ("group",)
