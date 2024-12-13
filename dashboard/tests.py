from django.test import TestCase
from dashboard.models import Assignment, Course  # Import the Course and Assignment models
from dashboard.schedule import Schedule  # Import the correct class from schedule.py
import datetime
from django.utils import timezone

class AddAssignmentTests(TestCase):

    def test_add_assignment_creates_assignment(self):
        """
        add_assignment() should create an Assignment with the given details.
        """
        schedule_manager = Schedule()

        # Create a Course instance first
        course = Course.objects.create(
            name="Math 101",
            instructor="Dr. Smith",
            description="A course on algebra",
            course_image="default.jpg"
        )

        # Call the add_assignment method with the Course instance
        schedule_manager.add_assignment(
            course_name=course,  # Passing the Course instance
            assignment_type="Homework",
            description="Algebra assignment",
            priority=2,
            link="http://example.com"
        )

        # Fetch the assignment from the database
        assignment = Assignment.objects.get(course_name=course)

        # Assertions to check if the assignment was created correctly
        self.assertEqual(assignment.course_name, course)
        self.assertEqual(assignment.assignment_type, "Homework")
        self.assertEqual(assignment.description, "Algebra assignment")
        self.assertEqual(assignment.priority, 2)
        self.assertEqual(assignment.link, "http://example.com")

    def test_add_assignment_with_defaults(self):
        """
        add_assignment() should create an Assignment with default values for optional fields.
        """
        schedule_manager = Schedule()

        # Create a Course instance first
        course = Course.objects.create(
            name="Physics 101",
            instructor="Dr. Johnson",
            description="A course on physics",
            course_image="default.jpg"
        )

        # Call the method without the optional parameters
        schedule_manager.add_assignment(
            course_name=course,  # Passing the Course instance
            assignment_type="Lab Report"
        )

        # Fetch the assignment from the database
        assignment = Assignment.objects.get(course_name=course)

        # Check if the default values were correctly applied
        self.assertEqual(assignment.description, "")  # Default description is an empty string
        self.assertEqual(assignment.priority, 0)  # Default priority is 0
        self.assertEqual(assignment.link, "")  # Default link is an empty string

    def test_count_assignments(self):
        """
        count_assignments() should return the total number of assignments in the database.
        """
        schedule_manager = Schedule()

        # Create a Course instance
        course = Course.objects.create(
            name="Chemistry 101",
            instructor="Dr. Green",
            description="A course on chemistry",
            course_image="default.jpg"
        )

        # Add assignments
        schedule_manager.add_assignment(
            course_name=course,
            assignment_type="Lab Report"
        )
        schedule_manager.add_assignment(
            course_name=course,
            assignment_type="Homework"
        )

        # Test count of assignments
        count = schedule_manager.count_assignments()
        self.assertEqual(count, 2)  # Expect 2 assignments

    def test_delete_assignment_by_name(self):
        """
        delete_assignment_by_name() should delete an assignment by its name.
        """
        schedule_manager = Schedule()

        # Create a Course instance
        course = Course.objects.create(
            name="History 101",
            instructor="Dr. Brown",
            description="A course on history",
            course_image="default.jpg"
        )

        # Add an assignment
        assignment = schedule_manager.add_assignment(
            course_name=course,
            assignment_type="Essay"
        )

        # Fetch the assignment
        assignment_to_delete = Assignment.objects.get(course_name=course)

        # Delete the assignment by name
        schedule_manager.delete_assignment_by_name(assignment_to_delete)


    def test_delete_all_assignments(self):
        """
        delete_all_assignments() should delete all assignments in the database.
        """
        schedule_manager = Schedule()

        # Create a Course instance
        course = Course.objects.create(
            name="Art 101",
            instructor="Dr. Gray",
            description="A course on art",
            course_image="default.jpg"
        )

        # Add two assignments
        schedule_manager.add_assignment(
            course_name=course,
            assignment_type="Painting"
        )
        schedule_manager.add_assignment(
            course_name=course,
            assignment_type="Sculpture"
        )

        # Delete all assignments
        schedule_manager.delete_all_assignments()

        # Check if all assignments were deleted
        self.assertEqual(Assignment.objects.count(), 0)  # Expect no assignments


    def test_set_course_name(self):
        """
        set_course_name() should update the course name and save the assignment.
        """
        schedule_manager = Schedule()

        # Create a Course instance and an Assignment
        course = Course.objects.create(
            name="Science 101",
            instructor="Dr. Green",
            description="A course on science",
            course_image="default.jpg"
        )
        assignment = Assignment.objects.create(
            course_name=course,
            assignment_type="Lab Report"
        )

        # Update course name
        new_course = Course.objects.create(
            name="Updated Science 101",
            instructor="Dr. Green",
            description="A course on updated science",
            course_image="default.jpg"
        )
        assignment.set_course_name(new_course)
        assignment.refresh_from_db()

        self.assertEqual(assignment.course_name, new_course)

    def test_set_description(self):
        """
        set_description() should update the description and save the assignment.
        """
        schedule_manager = Schedule()

        # Create an Assignment
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="Art 101", instructor="Dr. Blue", description="Art class", course_image="default.jpg"),
            assignment_type="Drawing",
            description="Initial description"
        )

        # Update description
        assignment.set_description("Updated description")
        assignment.refresh_from_db()

        self.assertEqual(assignment.description, "Updated description")

    def test_set_assignment_type(self):
        """
        set_assignment_type() should update the assignment type and save the assignment.
        """
        schedule_manager = Schedule()

        # Create an Assignment
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="History 101", instructor="Dr. Brown", description="History class", course_image="default.jpg"),
            assignment_type="Essay"
        )

        # Update assignment type
        assignment.set_assignment_type("Research Paper")
        assignment.refresh_from_db()

        self.assertEqual(assignment.assignment_type, "Research Paper")

    def test_set_priority(self):
        """
        set_priority() should update the priority and save the assignment.
        """
        schedule_manager = Schedule()

        # Create an Assignment
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="Physics 101", instructor="Dr. White", description="Physics class", course_image="default.jpg"),
            assignment_type="Homework",
            priority=1
        )

        # Update priority
        assignment.set_priority(5)
        assignment.refresh_from_db()

        self.assertEqual(assignment.priority, 5)

    def test_set_link(self):
        """
        set_link() should update the link and save the assignment.
        """
        schedule_manager = Schedule()

        # Create an Assignment
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="Chemistry 101", instructor="Dr. Purple", description="Chemistry class", course_image="default.jpg"),
            assignment_type="Lab",
            link="http://oldlink.com"
        )

        # Update link
        assignment.set_link("http://newlink.com")
        assignment.refresh_from_db()

        self.assertEqual(assignment.link, "http://newlink.com")

    def test_set_due_date(self):
        """
        set_due_date() should update the due date and save the assignment.
        """
        schedule_manager = Schedule()

        # Create an Assignment
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="Math 101", instructor="Dr. Yellow", description="Math class",
                                              course_image="default.jpg"),
            assignment_type="Homework",
            due_date=timezone.now() + datetime.timedelta(days=5),
            priority=1
        )

        # Update due date with a datetime value
        new_due_date = timezone.now() + datetime.timedelta(days=10)
        assignment.set_due_date(new_due_date)
        assignment.refresh_from_db()

        # Normalize both to compare just the date part
        self.assertEqual(assignment.due_date, new_due_date.date())

    def test_is_due_soon(self):
        """
        is_due_soon() should return True if the assignment is due within the last 24 hours.
        """
        schedule_manager = Schedule()

        # Create an Assignment with a due date within the next 24 hours
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="Math 101", instructor="Dr. Gray", description="Math class", course_image="default.jpg"),
            assignment_type="Homework",
            due_date=timezone.now() - datetime.timedelta(hours=12)
        )

        self.assertTrue(assignment.is_due_soon())

        # Create an Assignment with a due date beyond the next 24 hours
        assignment = Assignment.objects.create(
            course_name=Course.objects.create(name="Physics 101", instructor="Dr. White", description="Physics class", course_image="default.jpg"),
            assignment_type="Lab",
            due_date=timezone.now() + datetime.timedelta(days=2)
        )

        self.assertFalse(assignment.is_due_soon())
