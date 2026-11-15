
from django.contrib import admin

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
    ordering = ("full_name",)


@admin.register(ReservedIndex)
class ReservedIndexAdmin(admin.ModelAdmin):
    list_display = ("index_number", "group", "created_at")
    search_fields = ("index_number",)
    list_filter = ("group",)
