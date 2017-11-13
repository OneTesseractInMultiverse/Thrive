from thrive.models.graph import (
    User, 
    Group,
    Student, 
    LegalGuardian, 
    Course
)
import uuid

# ==============================================================================
# STUDENT TRANSACTIONS
# ==============================================================================


def find_student_by_personal_id(personal_id):
    """
    """
    return Student.nodes.get_or_none(personal_id=personal_id)

# ------------------------------------------------------------------------------
# ADD LEGAL GUARDIAN
# ------------------------------------------------------------------------------
def add_legal_guardian(student, legal_guardian):
    try:
        guardian = LegalGuardian.nodes.get_or_none(personal_id=legal_guardian.personal_id)
        if guardian is not None:
            guardian.phone_number = legal_guardian.phone_number
            guardian.email = legal_guardian.email
            guardian.address = legal_guardian.address
        else:
            guardian = legal_guardian
        guardian.dependents.connect(student)
        guardian.save()
        student.legal_guardians.connect(guardian)
        student.save()
        return True
    except Exception as ex:
        # TODO proper exception handling
        print(ex)
        return False



# ------------------------------------------------------------------------------
# ADD STUDENT TO COURSE
# ------------------------------------------------------------------------------
def add_student_to_course(course, student):
    """
        Validates if
    """
    if student is not None and course is not None:
        if student.education_level_year == course.education_level_year:
            student.courses.connect(course)
            student.save()
            course.students.connect(student)
            course.save()
            return True
    return False