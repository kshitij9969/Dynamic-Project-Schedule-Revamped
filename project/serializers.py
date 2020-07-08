from rest_framework import serializers

from . import models


def normalize(text):
    return str(text).strip().lower()


class ProjectDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes the ProjectScheduleDetail model
    """

    class Meta:
        model = models.ProjectScheduleDetail
        fields = ('id',
                  'project_name', 'project_description',
                  'date',
                  'analysis', 'analysis_text',
                  'cut', 'cut_text',
                  'code_merge', 'code_merge_text',
                  'ST', 'ST_text',
                  'UAT', 'UAT_text',
                  'implementation', 'implementation_text',
                  'PIS', 'PIS_text'
                  )

    def create(self, validated_data):
        """
        Return the ProjectScheduleDetail model object
        :param validated_data: Validated data from the request
        :return: ProjectScheduleDetail object
        """
        project_name = validated_data.get('project_name')
        project_description = validated_data.get('project_description')

        return models.ProjectScheduleDetail(**self.validated_data)
