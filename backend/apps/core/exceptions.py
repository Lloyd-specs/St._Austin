from rest_framework.exceptions import APIException


class ConflictError(APIException):
    status_code = 409
    default_detail = 'A conflict occurred during synchronization.'
    default_code = 'conflict'


class BusinessRuleViolation(APIException):
    status_code = 422
    default_detail = 'Business rule violation.'
    default_code = 'business_rule_violation'
