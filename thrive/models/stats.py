from thrive.models.graph import (
    User,
    Group,
    Student,
    LegalGuardian,
    Course,
    Grade,
    Period
)


def count_total_students():
    # "MATCH(s:Student) RETURN COUNT(s)"
    count = len(Student.nodes.all())
    return count


def count_total_active_students():
    # "MATCH(s:Student) RETURN COUNT(s)"
    count = len(Student.nodes.filter(active=True))
    return count


def count_total_users():
    return len(User.nodes.all())


def count_total_teachers():
    # "MATCH(s:Student) RETURN COUNT(s)"
    teachers_group = Group.nodes.get_or_none(name='TEACHERS')
    if teachers_group is not None:
        return len(teachers_group.members.all())
    else:
        return 0