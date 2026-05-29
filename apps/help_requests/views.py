from django.shortcuts import render

# Create your views here.
# backend/apps/help_requests/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import HelpRequest, EmergencyAlert
from .serializers import HelpRequestSerializer, EmergencyAlertSerializer
from ..ai_coach.risk_predictor import RiskPredictor

class HelpRequestViewSet(viewsets.ModelViewSet):
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'my_requests']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        risk_predictor = RiskPredictor()
        
        # Analyze request for risk
        risk_analysis = risk_predictor.analyze_chat_message(
            serializer.validated_data.get('description', ''),
            {'user_id': str(self.request.user.id)}
        )
        
        # Save with risk score
        serializer.save(
            user=self.request.user,
            risk_score=risk_analysis['risk_score'],
            risk_level=risk_analysis['risk_level']
        )
        
        # Handle high-risk cases
        if risk_analysis['requires_immediate_action']:
            self._handle_high_risk(serializer.instance, risk_analysis)
    
    @action(detail=False, methods=['post'])
    def emergency_sos(self, request):
        """Handle emergency SOS alerts"""
        serializer = EmergencyAlertSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create emergency alert
            alert = serializer.save(
                user=request.user,
                status='ACTIVE'
            )
            
            # Get user location
            location = request.data.get('location', {})
            
            # Notify emergency contacts
            self._notify_emergency_contacts(alert, location)
            
            # Log to analytics
            self._log_emergency_incident(alert, location)
            
            return Response({
                'emergency_id': alert.id,
                'message': 'Emergency alert sent successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _handle_high_risk(self, help_request, risk_analysis):
        """Handle high-risk help requests"""
        
        # Send email notification to counselors
        send_mail(
            subject=f'URGENT: High Risk Report - {help_request.id}',
            message=f"""
            High risk help request received:
            
            Type: {help_request.get_type_display()}
            Risk Score: {risk_analysis['risk_score']}
            Risk Level: {risk_analysis['risk_level']}
            
            Detected Risks:
            {json.dumps(risk_analysis['detected_risks'], indent=2)}
            
            Suggested Actions: {', '.join(risk_analysis['suggested_actions'])}
            
            Please review immediately in the admin dashboard.
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.COUNSELOR_EMAIL],
            fail_silently=False,
        )
        
        # If emergency, also send SMS
        if risk_analysis['risk_level'] == 'CRITICAL':
            self._send_sms_alert(help_request.user, risk_analysis)
    
    def _notify_emergency_contacts(self, alert, location):
        """Notify emergency contacts about SOS"""
        
        # This would integrate with SMS service (Africa's Talking)
        # For now, we'll log it
        print(f"Emergency alert {alert.id} triggered at location: {location}")
        
        # In production, send SMS to:
        # - Police (112)
        # - Local DOVVSU office
        # - Nearest health facility
        
    def _send_sms_alert(self, user, risk_analysis):
        """Send SMS alert for critical cases"""
        
        # Integrate with Africa's Talking or Hubtel
        # Example SMS content:
        message = f"""
        CRITICAL ALERT: User {user.id} requires immediate attention.
        Risk: {risk_analysis['detected_risks'][0]['type']}
        """
        
        # Send SMS logic here
        pass