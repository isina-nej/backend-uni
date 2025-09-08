# Fault Tolerance Example
# In views, use try-except to handle errors without crashing the system

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loguru import logger

class FaultTolerantView(APIView):
    def get(self, request):
        try:
            # Simulate potential failure
            data = self.process_data()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in FaultTolerantView: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_data(self):
        # Business logic here
        return {'message': 'Data processed successfully'}
