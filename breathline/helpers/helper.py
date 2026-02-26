import datetime, logging, hashlib, json,socket, base64, os, sys
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from uuid import uuid4
from io import BytesIO
from django.core.files import File
from pathlib import Path
from django.contrib.auth.models import update_last_login
from django.utils import timezone
import math
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from apps.user.models import GeneratedAccessToken
from django.conf import settings
from decimal import Decimal



logger = logging.getLogger(__name__)


def get_all_tokens_for_user(user):
    return OutstandingToken.objects.filter(user=user)


def get_all_tokens_for_multiple_users(users):
    return OutstandingToken.objects.filter(user__in=users)


def get_user_access_tokens(user):
    return GeneratedAccessToken.objects.filter(user=user)

def update_last_logout(sender, user, **kwargs):
    """
    A signal receiver which updates the last_logout date for
    the user logging out.
    """
    user.last_logout = timezone.now()
    user.last_active = timezone.now()
    user.is_logged_in = False
    user.save(update_fields=["last_logout","is_logged_in","last_active"])




def get_token_user_or_none(request):
    User = get_user_model()
    try:
        instance = User.objects.get(id=request.user.id)
    except Exception:
        instance = None
    finally:
        return instance


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    
    
def get_value_or_empty(value):
    
    return value if value is not None else ""


    
def get_value_or_dash(value):
    
    return value if value is not None and value !='' else "-"


def handle_index_error(key, content):
    try:
        return content[key]
    except IndexError:
        return ''
    except:
        return ''
    
    
    
def has_decimal(num):
    try:
        _, int_part = math.modf(num)
        return int_part != num
    except:
        return False

def encryptFileContent(file):
    try:
        md5 = hashlib.md5()
        data = file.read()
        md5.update(data)
        decoded_data = data.decode()
        version = handle_index_error(8, handle_index_error(0, handle_index_error(
            1, decoded_data.split('\n', 2)).replace('  ', ' ').split("~")).split("*"))
        is_837 = True if file.name.lower().endswith('.837') else False
        is_835 = True if file.name.lower().endswith('.835') else False
        return {'status': 200, 'md5': md5.hexdigest(), 'version': version, 'is_837': is_837, 'is_835': is_835}
    except Exception as e:

        return {}


def formatDates(date_format, type=None):
    try:
        if date_format == '':
            return date_format
        match type:
            case 3:
                year, month, day, hours, minute = date_format[0:4], date_format[
                    4:6], date_format[6:8],  date_format[8:10], date_format[10:]
                date_time = datetime.datetime(int(year), int(month), int(
                    day), int(hours), int(minute)).strftime("%Y-%m-%d %H:%M")
                return date_time
            case _:
                year, month, day = date_format[0:4], date_format[4:6], date_format[6:8]
                date = datetime.datetime(int(year), int(
                    month), int(day)).strftime("%Y-%m-%d")
                return date

    except ValueError:
        year, month, day = date_format[0:4], date_format[4:5], date_format[5:7]
        date = datetime.datetime(int(year), int(
            month), int(day)).strftime("%Y-%m-%d")
        return date
    except:
        return date_format

def login_authorization(request):
    if request.user.is_authenticated:
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "req_body":json.loads(request.body.decode("utf-8")) if request.body else {},
        }  

        if ('req_body' in log_data):
            if ('password' in log_data['req_body']):
                del log_data['req_body']['password']

        index='unauthorized_login'

        return False   
    else:
        return True





def base64_to_file(value):
    try:
        format, base64_data = value.split(';base64,')
        decoded_data = base64.b64decode(base64_data)
        stream = BytesIO()
        stream.write(decoded_data)
        stream.seek(0)

        return File(stream)
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(exc_type, fname, exc_tb.tb_lineno)
        return None
    

def base64_file_extension(value):
    try:
        format, base64_data = value.split(';base64,')
        media_type = format.split('/')[1]
        base64_extension = media_type.split('+')[0] 
        return base64_extension
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(exc_type, fname, exc_tb.tb_lineno)
        return None
        
        
        
        
        
#create json BytesIO File from the given base64 code data:application/json;base64,dW5kZWZpbmVk in python      


        
def get_file_name_and_extension(file_path):
    return Path(file_path).stem









def convert_to_single_date_format(date_str):
    if date_str is None or date_str == '':
        return None
    # Define a list of possible input date formats
    input_formats = ['%m/%d/%y', '%m-%d-%y', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']

    # Try each input format until one succeeds
    for fmt in input_formats:
        try:
            # Parse the date string using the current format
            date_obj = datetime.datetime.strptime(date_str, fmt)

            # Format the date object using the desired format
            formatted_date_str = date_obj.strftime('%Y-%m-%d')

            # Return the formatted date string
            return formatted_date_str

        except ValueError:
            # If the current format fails, continue to the next format
            continue

    # If no formats succeed, raise an error
    print('Unrecognized date format: {}'.format(date_str))
    return None
    
    


















def convert_to_datetime_format(input_string):
    format_string = ''
    format_codes = {'M': '%m', 'D': '%d', 'Y': '%Y'}
    separators = set('-/')
    processed_letters = []
    
    for char in input_string:
        if char in format_codes and char not in processed_letters:
            format_string += format_codes[char]
            processed_letters.append(char)
        elif char in separators:
            format_string += char
    
    return format_string








import datetime, logging, hashlib, json,socket, base64, os, sys
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.core.files.base import ContentFile
from uuid import uuid4
from io import BytesIO
from django.core.files import File
from pathlib import Path
from django.contrib.auth.models import update_last_login
from django.utils import timezone
import math
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from apps.user.models import GeneratedAccessToken
from django.conf import settings



logger = logging.getLogger(__name__)


def get_all_tokens_for_user(user):
    return OutstandingToken.objects.filter(user=user)


def get_all_tokens_for_multiple_users(users):
    return OutstandingToken.objects.filter(user__in=users)


def get_user_access_tokens(user):
    return GeneratedAccessToken.objects.filter(user=user)

def update_last_logout(sender, user, **kwargs):
    """
    A signal receiver which updates the last_logout date for
    the user logging out.
    """
    user.last_logout = timezone.now()
    user.last_active = timezone.now()
    user.is_logged_in = False
    user.save(update_fields=["last_logout","is_logged_in","last_active"])




def get_token_user_or_none(request):
    User = get_user_model()
    try:
        instance = User.objects.get(id=request.user.id)
    except Exception:
        instance = None
    finally:
        return instance


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    
    
def get_value_or_empty(value):
    
    return value if value is not None else ""


    
def get_value_or_dash(value):
    
    return value if value is not None and value !='' else "-"


def handle_index_error(key, content):
    try:
        return content[key]
    except IndexError:
        return ''
    except:
        return ''
    
    
    
def has_decimal(num):
    try:
        _, int_part = math.modf(num)
        return int_part != num
    except:
        return False

def encryptFileContent(file):
    try:
        md5 = hashlib.md5()
        data = file.read()
        md5.update(data)
        decoded_data = data.decode()
        version = handle_index_error(8, handle_index_error(0, handle_index_error(
            1, decoded_data.split('\n', 2)).replace('  ', ' ').split("~")).split("*"))
        is_837 = True if file.name.lower().endswith('.837') else False
        is_835 = True if file.name.lower().endswith('.835') else False
        return {'status': 200, 'md5': md5.hexdigest(), 'version': version, 'is_837': is_837, 'is_835': is_835}
    except Exception as e:

        return {}


def formatDates(date_format, type=None):
    try:
        if date_format == '':
            return date_format
        match type:
            case 3:
                year, month, day, hours, minute = date_format[0:4], date_format[
                    4:6], date_format[6:8],  date_format[8:10], date_format[10:]
                date_time = datetime.datetime(int(year), int(month), int(
                    day), int(hours), int(minute)).strftime("%Y-%m-%d %H:%M")
                return date_time
            case _:
                year, month, day = date_format[0:4], date_format[4:6], date_format[6:8]
                date = datetime.datetime(int(year), int(
                    month), int(day)).strftime("%Y-%m-%d")
                return date

    except ValueError:
        year, month, day = date_format[0:4], date_format[4:5], date_format[5:7]
        date = datetime.datetime(int(year), int(
            month), int(day)).strftime("%Y-%m-%d")
        return date
    except:
        return date_format

def login_authorization(request):
    if request.user.is_authenticated:
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "req_body":json.loads(request.body.decode("utf-8")) if request.body else {},
        }  

        if ('req_body' in log_data):
            if ('password' in log_data['req_body']):
                del log_data['req_body']['password']

        index='unauthorized_login'

        return False   
    else:
        return True





def base64_to_file(value):
    try:
        format, base64_data = value.split(';base64,')
        decoded_data = base64.b64decode(base64_data)
        stream = BytesIO()
        stream.write(decoded_data)
        stream.seek(0)

        return File(stream)
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(exc_type, fname, exc_tb.tb_lineno)
        return None
    

def base64_file_extension(value):
    try:
        format, base64_data = value.split(';base64,')
        media_type = format.split('/')[1]
        base64_extension = media_type.split('+')[0] 
        return base64_extension
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(exc_type, fname, exc_tb.tb_lineno)
        return None
        

def encode_email(email_body):
    """
    Encodes a string (email body) into a base64 string.

    Args:
        email_body (str): The email content to be encoded.

    Returns:
        str: The base64-encoded string.
    """
    # The base64.b64encode function expects bytes, so we must
    # first encode the string to bytes (e.g., using UTF-8).
    encoded_bytes = base64.b64encode(email_body.encode('utf-8'))
    # The result is bytes, so we decode it back to a string for display.
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string


def decode_email(base64_string):
    """
    Decodes a base64 string back into a regular string (email body).

    Args:
        base64_string (str): The base64-encoded string.

    Returns:
        str: The decoded email content.
    """
    # The base64.b64decode function expects bytes, so we first encode
    # the string back to bytes.
    decoded_bytes = base64.b64decode(base64_string.encode('utf-8'))
    # The result is bytes, so we decode it back to a string (UTF-8).
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string
        
        
        
        
#create json BytesIO File from the given base64 code data:application/json;base64,dW5kZWZpbmVk in python      


        
def get_file_name_and_extension(file_path):
    return Path(file_path).stem









def convert_to_single_date_format(date_str):
    if date_str is None or date_str == '':
        return None
    # Define a list of possible input date formats
    input_formats = ['%m/%d/%y', '%m-%d-%y', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']

    # Try each input format until one succeeds
    for fmt in input_formats:
        try:
            # Parse the date string using the current format
            date_obj = datetime.datetime.strptime(date_str, fmt)

            # Format the date object using the desired format
            formatted_date_str = date_obj.strftime('%Y-%m-%d')

            # Return the formatted date string
            return formatted_date_str

        except ValueError:
            # If the current format fails, continue to the next format
            continue

    # If no formats succeed, raise an error
    print('Unrecognized date format: {}'.format(date_str))
    return None
    
    


















def convert_to_datetime_format(input_string):
    format_string = ''
    format_codes = {'M': '%m', 'D': '%d', 'Y': '%Y'}
    separators = set('-/')
    processed_letters = []
    
    for char in input_string:
        if char in format_codes and char not in processed_letters:
            format_string += format_codes[char]
            processed_letters.append(char)
        elif char in separators:
            format_string += char
    
    return format_string



def create_employee_code(Classmodel,company):
    first_initials = company.company_name[0].upper()   #first letter of company name
    last_initials  = company.company_name[-1].upper()  # last letter of company name 

    last_employee=Classmodel.objects.filter(branch__company=company).order_by('-id').first()   # Retrieve the last employee created for this company

    if last_employee:                                           # If an employee exists, extract the numeric part of their employee_code and convert it to an integer
        last_id=int(last_employee.employee_code[-4:])
    else:
        last_id=0
        
    last_id+=1

    while (Classmodel.all_objects.filter(employee_code=f"{first_initials}{last_initials}{last_id:04d}").exists()):      # Ensure the new employee_code is unique by checking if it already exists in the database
        last_id+=1


    return f"{first_initials}{last_initials}{last_id:04d}"    



def calculate_salarycomponents_total(basic_salary,house_rent_allowance,travel_allowance,dearness_allowance,medical_allowance,other_allowance,bonuses):         
   
    try:

        total_salary = (basic_salary+house_rent_allowance+travel_allowance+dearness_allowance+medical_allowance+other_allowance+bonuses)
        return total_salary
    except:
        return None         
                      


def calculate_employee_loan(loan_amount,interest,repayment_period_months):
    try:
        loan_amount               = loan_amount or 0
        interest                  = interest  or 0
        repayment_period_months   = repayment_period_months or 0

        if interest > 0 and interest is not None:
           total_interest = (loan_amount * (interest / 100) * (repayment_period_months / Decimal(12)))
           total_amount   = loan_amount + total_interest
           monthly_amount = total_amount/repayment_period_months
        else:
            total_amount = loan_amount
            monthly_amount = loan_amount/repayment_period_months
       
        return monthly_amount,total_amount

    except:
        return None      

def calculate_balance_loan(monthly_deduction,balance):
    try:
        return balance - monthly_deduction

    except:
        return None    




