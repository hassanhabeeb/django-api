from apps.user.models import ErrorLog
import os
import sys
from rest_framework import status


class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
            "status": args.get('status', True),
            "status_code": args.get('status_code', 200),
            "message": args.get('message', ''),
            "data": args.get('data', {}),
            "errors": args.get('errors', {}),
        }

class ErrorLogInfo(object):
    """
    A small helper for building consistent API responses
    and logging exceptions in a single place.
    """
 
    def __init__(self, user_id=None, **args):
        self.response = {
            "status": args.get('status', True),
            "status_code": args.get('status_code', status.HTTP_200_OK),
            "message": args.get('message', ''),
            "data": args.get('data', {}),
            "errors": args.get('errors', {}),
        }
        self.user_id = user_id if user_id else None
 
    def exception(self, e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
 
        error_message = (
            f"exc_type: {exc_type}, "
            f"filename: {filename}, "
            f"line: {exc_tb.tb_lineno}, "
            f"error: {str(e)}"
        )
        
       
        ErrorLog.objects.create(
            error_message=error_message,
            user_id=self.user_id
        )
 
        self.response.update({
            "status": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": error_message,
            "errors": {},
        })
 
        return self.response