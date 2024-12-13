from django import forms
from dashboard.models import Assignment, Course
from .models import CourseFile


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','instructor','description']


class AddAssignmentToCourseForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Updated field

    class Meta:
        model = Assignment
        fields = ['description', 'assignment_type', 'due_date', 'priority', 'keywords']


class CourseFileForm(forms.ModelForm):
    class Meta:
        model = CourseFile
        fields = ['file', 'filename', 'content_type', 'keywords', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter the description for this material'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = file.name.split('.')[-1].lower()
            if file_type not in ['txt', 'pdf', 'jpg']:
                raise forms.ValidationError("Unsupported file type.")
        return file


class FilterCourseFiles(forms.ModelForm):
    class Meta:
        model = CourseFile
        fields = ['filename', 'content_type', 'keywords']

    def __init__(self, *args, **kwargs):
        super(FilterCourseFiles, self).__init__(*args, **kwargs)
        self.fields['filename'].required = False
        self.fields['content_type'].required = False
        self.fields['keywords'].required = False
