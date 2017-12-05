from thrive.models.graph import (
    User, 
    Group,
    Student, 
    LegalGuardian, 
    Course,
    Grade, 
    Period
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
# LIST STUDENTS BY LEVEL
# ------------------------------------------------------------------------------
def get_students_by_level(education_level, education_level_year):
    try:
        return Student.nodes.filter(education_level=education_level, education_level_year=education_level_year)
    except Exception as x:
        print(x)
        return []


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
        guardian.save()
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
    """
    if student is not None and course is not None:
        if student.education_level_year == course.education_level_year:
            student.courses.connect(course)
            student.save()
            course.students.connect(student)
            course.save()
            return True
    return False


# ------------------------------------------------------------------------------
# ADD GRADE TO STUDENT
# ------------------------------------------------------------------------------
def add_grade_to_student(grade, course_id, student_id, period_year, period_number):
    """
    """
    if grade is not None:
        student = Student.nodes.get_or_none(student_id=student_id)
        period = Period.nodes.get_or_none(year=period_year, number=period_number)
        course = Course.nodes.get_or_none(course_id=course_id)
        if student is not None and period is not None and course is not None:
            
            grade.student.connect(student)
            student.grades.connect(grade)
            
            grade.course.connect(course)
            course.grades.connect(grade)
            
            grade.period.connect(period)
            period.grades.connect(grade)
            
            grade.save()
            period.save()
            course.save()
            
    return False


# ------------------------------------------------------------------------------
# ADD PERIODS FOR YEAR
# ------------------------------------------------------------------------------
def spawn_periods_for_year(year, denominator):
    period = Period.nodes.get_or_none(denominator=denominator, year=year, number=1)
    if period is None:
        for num in range(1, denominator+1):
            period = Period(
                    number=num, 
                    year=year,
                    denominator=denominator
                )
            period.save()
        return True
    return False
    
# ------------------------------------------------------------------------------
# ADD COURSE
# ------------------------------------------------------------------------------
def add_course(student,course):
    try:
        courses = Course.nodes.get_or_none(course_id=course.course_id)
        if courses is not None:
            courses.title = course.title
            courses.description = course.description
            courses.year = course.year
            courses.education_level_year = course.education_level_year
        else:
            courses.save()
            courses.students.connect(student)
            student.courses.connect(courses)
            student.save()
        return True
    except Exception as ex:
        # TODO proper exception handling
        print(ex)
        return False
        
# ------------------------------------------------------------------------------
# ADD TEACHER TO COURSE
# ------------------------------------------------------------------------------        
def add_teacher_to_course(course, user):
    ""
    ""
    if user is not None and course is not None:
        user.courses.connect(course)
        user.save()
        course.taught_by.connect(user)
        course.save()
        return True
    return False
    
# ------------------------------------------------------------------------------
# ADD PERIOD TO COURSE
# ------------------------------------------------------------------------------                
def add_period_to_course(period, course)
    ""
    ""
    if period is not None and course is not Note:
        
        course.period.connect(period)
        course.save()
        period.courses.connect(course)
        period.save()
        return True
    return False
