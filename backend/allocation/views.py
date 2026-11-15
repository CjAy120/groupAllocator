
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Student, Group
from .serializers import (
    StudentRegistrationSerializer,
    StudentSerializer,
    GroupSerializer,
    GroupSummarySerializer,
)
from .services import (
    register_student,
    AllocationError,
    DuplicateIndexError,
)


class StudentRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            student = register_student(
                full_name=serializer.validated_data["full_name"],
                index_number=serializer.validated_data["index_number"],
            )

        except DuplicateIndexError as error:
            return Response(
                {"message": str(error), "code": "duplicate_index"},
                status=status.HTTP_409_CONFLICT,
            )

        except AllocationError as error:
            return Response(
                {"message": str(error), "code": "allocation_error"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Registration successful.",
                "student": StudentSerializer(student).data,
            },
            status=status.HTTP_201_CREATED,
        )


class StudentLookupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, index_number):
        normalized_index = index_number.strip().upper()

        student = (
            Student.objects
            .select_related("group")
            .filter(index_number=normalized_index)
            .first()
        )

        if not student:
            return Response(
                {
                    "found": False,
                    "message": "No group assignment was found for this index number.",
                    "code": "student_not_found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        group_members = (
            Student.objects
            .filter(group=student.group)
            .order_by("full_name")
        )

        return Response(
            {
                "found": True,
                "student": StudentSerializer(student).data,
                "group": {
                    "number": student.group.number,
                    "capacity": student.group.capacity,
                    "student_count": group_members.count(),
                    "members": StudentSerializer(
                        group_members,
                        many=True
                    ).data,
                },
            },
            status=status.HTTP_200_OK,
        )


class GroupListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        groups = (
            Group.objects
            .annotate(actual_student_count=Count("students"))
            .order_by("number")
        )

        return Response(
            GroupSummarySerializer(groups, many=True).data,
            status=status.HTTP_200_OK,
        )


class GroupDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, number):
        group = get_object_or_404(
            Group.objects.prefetch_related("students"),
            number=number,
        )

        return Response(
            GroupSerializer(group).data,
            status=status.HTTP_200_OK,
        )


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_students = Student.objects.count()
        total_groups = Group.objects.count()
        total_capacity = sum(
            Group.objects.values_list("capacity", flat=True)
        )

        groups = Group.objects.annotate(
            actual_student_count=Count("students")
        ).order_by("number")

        full_groups = sum(
            1 for group in groups
            if group.actual_student_count >= group.capacity
        )

        return Response({
            "total_students": total_students,
            "total_groups": total_groups,
            "total_capacity": total_capacity,
            "remaining_places": total_capacity - total_students,
            "full_groups": full_groups,
            "available_groups": total_groups - full_groups,
            "registration_open": total_students < total_capacity,
        })
