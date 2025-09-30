from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification  
from notifications.serializers import NotificationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_count(request):
    try:
        user = request.user
        total_notifications = Notification.objects.filter(user=user).count()

        return Response({
            "status": 200,
            "message": "Retrieved notification successfully",
            "data": {
                "total": total_notifications
            }
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_notification(request, id):
    try:
        user = request.user
        # Ensure the notification belongs to the authenticated user
        notification = Notification.objects.get(id=id, user=user)
        
        serializer = NotificationSerializer(notification)
        return Response({
            "status": 200,
            "message": "Retrieved notification successfully",
            "data": serializer.data
        })

    except Notification.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Notification not found"
        }, status=400)

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def mark_notification(request, id):
    try:
        user = request.user
        notification = Notification.objects.get(id=id, user=user)
        
        is_read = request.data.get("isRead")
        if is_read is None:
            return Response({
                "status": 400,
                "message": "isRead field is required"
            }, status=400)
        
        notification.is_read = is_read
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return Response({
            "status": 201,
            "message": "Notification successfully marked",
            "data": serializer.data
        })
        
    except Notification.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Notification not found"
        }, status=400)
        
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_all_notifications(request):
    try:
        user = request.user
        Notification.objects.filter(user=user).delete()

        return Response({
            "status": 200,
            "message": "Notifications deleted successfully",
            "data": {}
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)