"""
IT Request Compliance Validator

Validates IT requests against compliance rules and returns status.
Automates the approval workflow for internal IT requests.
"""

import json
import logging
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status enumeration"""
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    MISSING_DATA = "MISSING_DATA"


@dataclass
class ValidationResult:
    """Result of compliance validation"""
    status: ComplianceStatus
    message: str
    missing_fields: List[str] = None
    violations: List[str] = None


class ComplianceValidator:
    """Main compliance validator class"""
    
    def __init__(self):
        self.required_fields = [
            "title",
            "description", 
            "priority",
            "category",
            "requester_email"
        ]
        
        self.blocked_keywords = [
            "hack",
            "bypass", 
            "disable_security",
            "admin_override"
        ]
        
        self.valid_categories = [
            "software_request",
            "hardware_request", 
            "access_request",
            "change_request"
        ]
        
        self.valid_priorities = ["low", "medium", "high", "critical"]
    
    def validate_request(self, request_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate an IT request for compliance
        
        Args:
            request_data: Dictionary containing request details
            
        Returns:
            ValidationResult with status and details
        """
        logger.info(f"Validating request: {request_data.get('title', 'Unknown')}")
        
        # Check for missing required fields
        missing_fields = self._check_required_fields(request_data)
        if missing_fields:
            return ValidationResult(
                status=ComplianceStatus.MISSING_DATA,
                message=f"Missing required fields: {', '.join(missing_fields)}",
                missing_fields=missing_fields
            )
        
        # Check for violations
        violations = self._check_violations(request_data)
        if violations:
            return ValidationResult(
                status=ComplianceStatus.NON_COMPLIANT,
                message=f"Compliance violations found: {', '.join(violations)}",
                violations=violations
            )
        
        # All checks passed
        logger.info("Request is compliant")
        return ValidationResult(
            status=ComplianceStatus.COMPLIANT,
            message="Request meets all compliance requirements"
        )
    
    def _check_required_fields(self, request_data: Dict[str, Any]) -> List[str]:
        """Check for missing required fields"""
        missing = []
        for field in self.required_fields:
            if field not in request_data or not request_data[field]:
                missing.append(field)
        return missing
    
    def _check_violations(self, request_data: Dict[str, Any]) -> List[str]:
        """Check for compliance violations"""
        violations = []
        
        # Check for blocked keywords in title and description
        title = request_data.get("title", "").lower()
        description = request_data.get("description", "").lower()
        
        for keyword in self.blocked_keywords:
            if keyword in title or keyword in description:
                violations.append(f"Contains blocked keyword: {keyword}")
        
        # Check valid category
        category = request_data.get("category", "").lower()
        if category not in self.valid_categories:
            violations.append(f"Invalid category: {category}")
        
        # Check valid priority
        priority = request_data.get("priority", "").lower()
        if priority not in self.valid_priorities:
            violations.append(f"Invalid priority: {priority}")
        
        # Check email format (basic validation)
        email = request_data.get("requester_email", "")
        if "@" not in email or "." not in email:
            violations.append("Invalid email format")
        
        return violations


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Lambda handler function for processing IT request validations
    
    Args:
        event: Event data containing the request to validate
        context: Lambda context (optional)
        
    Returns:
        Dictionary with validation results
    """
    try:
        validator = ComplianceValidator()
        
        # Extract request data from event
        if "Records" in event:
            # SQS message format
            request_data = json.loads(event["Records"][0]["body"])
        else:
            # Direct invocation format
            request_data = event
        
        # Validate the request
        result = validator.validate_request(request_data)
        
        return {
            "statusCode": 200,
            "body": {
                "status": result.status.value,
                "message": result.message,
                "missing_fields": result.missing_fields or [],
                "violations": result.violations or []
            }
        }
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            "statusCode": 500,
            "body": {
                "status": "ERROR",
                "message": f"Validation failed: {str(e)}"
            }
        }


if __name__ == "__main__":
    # Test the validator
    test_request = {
        "title": "Install new software",
        "description": "Need to install Python development tools",
        "priority": "medium",
        "category": "software_request",
        "requester_email": "user@company.com"
    }
    
    result = lambda_handler(test_request)
    print(json.dumps(result, indent=2))
