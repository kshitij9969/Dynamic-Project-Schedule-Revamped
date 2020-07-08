from django.db import models


class ProjectMetaData(models.Model):
    """
    Model for project meta data
    """

    project_name = models.CharField(max_length=255, unique=True, null=False)
    project_description = models.TextField(null=False)

    def __str__(self):
        return f"Project name: {self.project_name}" \
               f"Project description: {self.project_description}."


class ProjectScheduleDetail(models.Model):
    """
    Model for project details
    1. first field is boolean store wheather action
    was taken on a particular date or not. For eg:
    analysis: True means that analysis was done
    for that particular date.

    2. _text is a textfield to store any note for
    that activity

    """

    assoc_project = models.ForeignKey(ProjectMetaData, on_delete=models.CASCADE)

    date = models.DateField()

    analysis = models.BooleanField(default=False)
    analysis_text = models.TextField(default='')

    cut = models.BooleanField(default=False)
    cut_text = models.TextField(default='')

    code_merge = models.BooleanField(default=False)
    code_merge_text = models.TextField(default='')

    ST = models.BooleanField(default=False)
    ST_text = models.TextField(default='')

    UAT = models.BooleanField(default=False)
    UAT_text = models.TextField(default='')

    implementation = models.BooleanField(default=False)
    implementation_text = models.TextField(default='')

    PIS = models.BooleanField(default=False)
    PIS_text = models.TextField(default='')

    def __str__(self):
        """
        String function to return string representation of
        the object.
        :return: String
        """
        return f"Date: {self.date}\n" \
               f"Analysis: {self.analysis}\n" \
               f"CUT: {self.cut}\n" \
               f"Code Merger: {self.code_merge}\n" \
               f"ST: {self.ST}\n" \
               f"UAT: {self.UAT}\n" \
               f"implementation: {self.implementation}\n" \
               f"PIS: {self.PIS}\n"
