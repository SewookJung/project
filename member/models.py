from django.db import models

# Create your models here.


class Member(models.Model):
    # Chief #
    CEO = '대표이사',

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
    )

    status = (
        (ACTIVE, "Active"),
        (PASSIVE, "Passive")
    )

    member_id = models.CharField(max_length=20)
    member_pw = models.CharField(max_length=20)
    member_name = models.CharField(null=True, max_length=10)
    member_dept = models.CharField(null=True, max_length=10)
    member_status = models.CharField(
        max_length=10,
        choices=status,
        default=ACTIVE
    )
    member_rank = models.CharField(
        max_length=20,
        choices=position,
        default=CEO
    )

    def __str__(self):
        return self.member_id