from .models import Assignment

#TODO: Add some form of error handling 
class Schedule():
    def __init__(self):
        self.sorting_token = "due_date" #can be priority, course_name, course_code, assignment_type
        self.sorting_order = "asc"
    
    def load_assignments(self):
        if self.sorting_order == "desc":
            return Assignment.objects.order_by(f"-{self.sorting_token}")
        return Assignment.objects.order_by(f"{self.sorting_token}")
    
    def set_sorting_token(self,token):
        self.sorting_token = token
    
    def set_sorting_order(self,order):
        self.sorting_order = order

    """def add_assignment(self, course_name,course_code, assignment_type, description = "", priority = 0, link = ""):
        Assignment.objects.create(course_name,course_code,assignment_type,description,priority,link)"""

    def add_assignment(self, course_name, assignment_type, description="", priority=0, link=""):
        Assignment.objects.create(
            course_name=course_name,
            assignment_type=assignment_type,
            description=description,
            priority=priority,
            link=link
        )

    def count_assignments(self):
        return Assignment.objects.count()

    def delete_assignment_by_name(self, assignment):
        # Find the assignment by name and delete it
        Assignment.objects.filter(course_name=assignment.course_name).delete()

    def delete_all_assignments(self):
        Assignment.objects.all().delete()