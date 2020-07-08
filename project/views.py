import datetime

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError

from . import models, serializers


def clean_text(text):
    """
    Trim the string for whitespaces
    :param text: string
    :return: string
    """
    return str(text).lower().strip()


def update_project_status_details(request):
    """
    Update the project schedule details except name
     and description
    :param request: request object
    :return: Boolean
    """
    project_name = request.data['project_name']
    project_description = request.data['project_description']
    update = request.data['update']
    filter_project_name = models.ProjectScheduleDetail.\
                          objects.filter(project_name=project_name)
    for data in update:
        project_instance = \
            filter_project_name.filter(date=data['date']).first()
        project_instance.analysis = bool(data['analysis'])
        project_instance.cut = bool(data['cut'])
        project_instance.code_merge = bool(data['code_merge'])
        project_instance.ST = bool(data['ST'])
        project_instance.UAT = bool(data['UAT'])
        project_instance.implementation = bool(data['implementation'])
        project_instance.PIS = bool(data['PIS'])

        project_instance.analysis_text = bool(data['analysis_text'])
        project_instance.cut_text = bool(data['cut_text'])
        project_instance.code_merge_text = bool(data['code_merge_text'])
        project_instance.ST_text = bool(data['ST_text'])
        project_instance.UAT_text = bool(data['UAT_text'])
        project_instance.implementation_text = bool(data['implementation_text'])
        project_instance.PIS_text = bool(data['PIS_text'])

        project_instance.save()


def update_project_details(project_obj, project_description):
    """
    Update the name and description of the project
    :param request: request object
    :return: Boolean
    """
    try:
        project_obj.project_description = project_description
        project_obj.save()
        return True

    except:
        return False


def delete_project_details(project_obj):
    """
    Delete project details
    :param project_obj: Project object
    :return:
    """
    queryset = models.ProjectMetaData.objects.get(pk=project_obj.id)

    for project in queryset:
        project.delete()
    else:
        return True

    return False


def populate_new_project_details(project_obj):
    """
    Populates the tables with the new project details
    :param project_obj: project object
    :return: Boolean
    """
    try:
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=365)
        end_date = today + datetime.timedelta(days=2*365)

        while start_date <= end_date:
            project_schedule_object = models.ProjectScheduleDetail()
            project_schedule_object.assoc_project = project_obj
            project_schedule_object.date = start_date
            start_date += datetime.timedelta(days=1)
            project_schedule_object.save()

        return True
    except Exception as e:
        print(e)
        return False


def get_project_names():
    """
    Return a list of project names
    :return: list
    """
    try:
        project_name_list = models.ProjectMetaData.objects.all()
        print(project_name_list)
        res = []
        for project in project_name_list:
            res.append({
                'project_name': project.project_name,
                'project_description': project.project_description
            })
        return res

    except:
        return False

# class ProjectScheduleViewSet(viewsets.ModelViewSet):
#     """
#     Handle crud operations on ProjectScheduleDetail model
#     """
#     serializer_class = serializers.ProjectDetailsSerializer
#     queryset = models.ProjectScheduleDetail.objects.all()


class ProjectScheduleApiSet(APIView):
    """
    Handle crud operations on ProjectScheduleDetail model
    """
    # serializer_class = serializers.ProjectDetailsSerializer

    def get(self, request, format=None):
        if get_project_names():
            res = get_project_names() if not len(get_project_names()) == 0 else {}

            return Response({'response': res},
                            status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """
        Post a new project
        :param request: request
        :param format:
        :return: redirect to list page
        """
        project_name = request.data['project_name']
        project_description = request.data['project_description']

        try:
            new_project_obj = models.ProjectMetaData()
            new_project_obj.project_name = project_name
            new_project_obj.project_description = project_description
            new_project_obj.save()
            populate_new_project_details(new_project_obj)

            res = get_project_names()
            return Response({'response': res}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        Update project details
        :param request: request object
        :param format:
        :return: Response object
        """
        try:
            project_name = request.data['project_name']
            project_description = request.data['project_description']
            project_obj = models.ProjectMetaData.objects.filter(project_name=project_name).first()
            project_obj.project_description = project_description
            project_obj.save()

            res = get_project_names()

            return Response({'response': res}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete a project
        :param request: request object
        :param format:
        :return: Response object
        """
        try:
            project_name = request.data['project_name']
            project_obj = models.ProjectMetaData.objects.filter(project_name=project_name).first()
            project_obj.delete()

            return Response({'response': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ManageProjectDetailsView(APIView):
    """
    Handles the details of a project
    """

    def post(self, request, format=None):
        try:
            start_date = request.data['start_date']
            end_date = request.data['end_date']
            project_name = request.data['project_name']

            queryset = []

            filter_project = models.ProjectScheduleDetail.objects.all()
            project_obj = models.ProjectMetaData.objects.filter(project_name=project_name).first()
            filter_project = filter_project.filter(assoc_project=project_obj)
            filter_project = filter_project.filter(date__range=[start_date, end_date]
                                                    ).order_by('date')

            for project in filter_project:
                queryset.append(
                    {
                        'date': project.date,

                        'analysis': project.analysis,
                        'analysis_text': project.analysis_text,

                        'cut': project.cut,
                        'cut_text': project.cut_text,

                        'code_merge': project.code_merge,
                        'code_merge_text': project.code_merge_text,

                        'ST': project.ST,
                        'ST_text': project.ST_text,

                        'UAT': project.UAT,
                        'UAT_text': project.UAT_text,

                        'implementation': project.implementation,
                        'implementation_text': project.implementation_text,

                        'PIS': project.PIS,
                        'PIS_text': project.PIS_text
                    }
                )
            else:
                return Response({'response': queryset}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        Change information about a project in the database
        :param request: Request object
        :param format:
        :return: Response object
        """
        try:
            req = request.data['request']
            project_name = request.data['project_name']
            project_meta = models.ProjectMetaData.objects.filter(project_name=project_name).first()

            for each in req:
                project_obj = models.ProjectScheduleDetail.objects.filter(assoc_project=project_meta)
                date = each['date']

                project_obj = project_obj.filter(date=date).first()

                project_obj.analysis = (each['analysis'])
                project_obj.analysis_text = each['analysis_text']

                project_obj.cut = (each['cut'])
                project_obj.cut_text = each['cut_text']

                project_obj.code_merge = bool(each['code_merge'])
                project_obj.code_merge_text = each['code_merge_text']

                project_obj.ST = bool(each['ST'])
                project_obj.ST_text = each['ST_text']

                project_obj.UAT = bool(each['UAT'])
                project_obj.UAT_text = each['UAT_text']

                project_obj.implementation = bool(each['implementation'])
                project_obj.implementation_text = each['implementation_text']

                project_obj.PIS = bool(each['PIS'])
                project_obj.PIS_text = each['PIS_text']

                project_obj.save()

            return Response({'response': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)
