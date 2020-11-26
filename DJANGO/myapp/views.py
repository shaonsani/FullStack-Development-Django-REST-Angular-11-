from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Tutorial
from .serializers import TutorialSerializer,MeetingSerializer

@api_view(['GET','POST','DELETE'])
def tutorials(request):
    """ GET POST DELETE """
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)

    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)

        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

        


@api_view(['GET','PUT','DELETE'])
def tutorial_details(request, pk):
    """ GET PUT DELETE"""

    try:
        tutorial = Tutorial.objects.get(pk=pk)

        if request.method == 'GET':
            tutorial_serializer = TutorialSerializer(tutorial)
            return JsonResponse(tutorial_serializer.data)
        elif request.method == 'PUT':
            tutorial_data = JSONParser().parse(request)

            tutorial_serializer = TutorialSerializer(tutorial , data=tutorial_data)
            if tutorial_serializer.is_valid():
                tutorial_serializer.save()
                return JsonResponse(tutorial_serializer.data)
            
            return JsonResponse(tutorial_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            tutorial.delete()
            return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



    except Tutorial.DoesNotExist:
        return JsonResponse({'message':'Tutorial Does Not Exist yet'}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def tutorial_published(request):
    """ Get all published tutorials in list"""
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)

@api_view(['POST','GET'])
def meeting(request):

    if request.method == 'POST':
        meeting_data = JSONParser().parse(request)

        meeting_serializer = MeetingSerializer(data=meeting_data)
        if meeting_serializer.is_valid():
            meeting_serializer.save()
            return JsonResponse(meeting_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(meeting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        return JsonResponse({'res':'ami nai'})


