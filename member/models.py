# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Member(models.Model):

    # Chief #
    CEO = "대표이사"

    # Executives #
    MANAGING_DIRECTOR = "상무"
    EXECUTIVE_DIRECTOR = "이사"

    # Staff #
    GENERAL_MANAGER = "부장"
    DEPUTY_GENERAL_MANAGER = "차장"
    MANAGER = "과장"
    ASSISTANT_MANAGER = "대리"
    SENIOR_STAFF = "주임"
    CLERK = "사원"

    # Research Institute #
    CTO = "연구소장"
    SENIOR_RESEARCH_ENGINEER = "책임연구원"
    ASSOCIATE_RESEARCH_ENGINEER = "전임연구원"

    ACTIVE = "Active"
    PASSIVE = "Passive"

    position = (
        ('이사/임원', (
            (CEO, '대표이사'),
            (MANAGING_DIRECTOR, '상무'),
            (EXECUTIVE_DIRECTOR, '이사'),
        )
        ),
        (
            '직원', (
                (GENERAL_MANAGER, "부장"),
                (DEPUTY_GENERAL_MANAGER, "차장"),
                (MANAGER, "과장"),
                (ASSISTANT_MANAGER, "대리"),
                (SENIOR_STAFF, "주임"),
                (CLERK, "사원"),
            )
        ),
        (
            '연구소', (
                (CTO, "연구소장"),
                (SENIOR_RESEARCH_ENGINEER, "책임 연구원"),
                (ASSOCIATE_RESEARCH_ENGINEER, "전임 연구원"),
            )
        ),
    )

    status = (
        (ACTIVE, "Active"),
        (PASSIVE, "Passive")
    )

    member_id = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=10, null=True)
    dept = models.CharField(max_length=10, null=True)
    status = models.CharField(
        max_length=10,
        choices=status,
        default=ACTIVE
    )
    rank = models.CharField(
        max_length=20,
        choices=position,
        default=CEO
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
