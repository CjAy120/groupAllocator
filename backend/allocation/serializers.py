
from rest_framework import serializers

from .models import Student, Group


class StudentRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        max_length=150,
        trim_whitespace=True
    )

    index_number = serializers.CharField(
        max_length=50,
        trim_whitespace=True
    )

    def validate_full_name(self, value):
        value = " ".join(value.split())

        if not value:
            raise serializers.ValidationError(
                "Full name is required."
            )

        return value

    def validate_index_number(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Index number is required."
            )

        return value


class StudentSerializer(serializers.ModelSerializer):
    group_number = serializers.IntegerField(
        source="group.number",
        read_only=True
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "index_number",
            "group_number",
            "registered_at",
        ]


class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    student_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "number",
            "capacity",
            "student_count",
            "is_full",
            "students",
        ]


class GroupSummarySerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    reserved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = [
            "number",
            "capacity",
            "student_count",
            "reserved_count",
            "is_full",
        ]
