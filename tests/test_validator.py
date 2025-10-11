"""
Unit tests for IT Request Compliance Validator

Tests demonstrate Test-Driven Development (TDD) approach.
"""

import pytest
import json
from app.validator import ComplianceValidator, ComplianceStatus, lambda_handler


class TestComplianceValidator:
    """Test cases for ComplianceValidator class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = ComplianceValidator()
        self.valid_request = {
            "title": "Install new software",
            "description": "Need to install Python development tools",
            "priority": "medium",
            "category": "software_request",
            "requester_email": "user@company.com"
        }
    
    def test_valid_request_returns_compliant(self):
        """Test that a valid request returns COMPLIANT status"""
        result = self.validator.validate_request(self.valid_request)
        
        assert result.status == ComplianceStatus.COMPLIANT
        assert "meets all compliance requirements" in result.message
        assert result.missing_fields is None
        assert result.violations is None
    
    def test_missing_required_fields_returns_missing_data(self):
        """Test that missing required fields returns MISSING_DATA status"""
        incomplete_request = {
            "title": "Install software",
            # Missing description, priority, category, requester_email
        }
        
        result = self.validator.validate_request(incomplete_request)
        
        assert result.status == ComplianceStatus.MISSING_DATA
        assert "Missing required fields" in result.message
        assert "description" in result.missing_fields
        assert "priority" in result.missing_fields
        assert "category" in result.missing_fields
        assert "requester_email" in result.missing_fields
    
    def test_blocked_keywords_return_non_compliant(self):
        """Test that blocked keywords return NON_COMPLIANT status"""
        malicious_request = self.valid_request.copy()
        malicious_request["description"] = "Need to hack the system"
        
        result = self.validator.validate_request(malicious_request)
        
        assert result.status == ComplianceStatus.NON_COMPLIANT
        assert "Compliance violations found" in result.message
        assert any("hack" in violation for violation in result.violations)
    
    def test_invalid_category_returns_non_compliant(self):
        """Test that invalid category returns NON_COMPLIANT status"""
        invalid_request = self.valid_request.copy()
        invalid_request["category"] = "invalid_category"
        
        result = self.validator.validate_request(invalid_request)
        
        assert result.status == ComplianceStatus.NON_COMPLIANT
        assert any("Invalid category" in violation for violation in result.violations)
    
    def test_invalid_priority_returns_non_compliant(self):
        """Test that invalid priority returns NON_COMPLIANT status"""
        invalid_request = self.valid_request.copy()
        invalid_request["priority"] = "super_urgent"
        
        result = self.validator.validate_request(invalid_request)
        
        assert result.status == ComplianceStatus.NON_COMPLIANT
        assert any("Invalid priority" in violation for violation in result.violations)
    
    def test_invalid_email_returns_non_compliant(self):
        """Test that invalid email format returns NON_COMPLIANT status"""
        invalid_request = self.valid_request.copy()
        invalid_request["requester_email"] = "not-an-email"
        
        result = self.validator.validate_request(invalid_request)
        
        assert result.status == ComplianceStatus.NON_COMPLIANT
        assert any("Invalid email format" in violation for violation in result.violations)
    
    def test_multiple_violations_all_reported(self):
        """Test that multiple violations are all reported"""
        bad_request = {
            "title": "hack the system",
            "description": "bypass security",
            "priority": "invalid",
            "category": "bad_category",
            "requester_email": "bad-email"
        }
        
        result = self.validator.validate_request(bad_request)
        
        assert result.status == ComplianceStatus.NON_COMPLIANT
        assert len(result.violations) >= 4  # Should have multiple violations


class TestLambdaHandler:
    """Test cases for lambda_handler function"""
    
    def test_lambda_handler_direct_invocation(self):
        """Test lambda handler with direct invocation"""
        event = {
            "title": "Install software",
            "description": "Install Python tools",
            "priority": "medium",
            "category": "software_request",
            "requester_email": "user@company.com"
        }
        
        result = lambda_handler(event)
        
        assert result["statusCode"] == 200
        assert result["body"]["status"] == "COMPLIANT"
    
    def test_lambda_handler_sqs_format(self):
        """Test lambda handler with SQS message format"""
        request_data = {
            "title": "Install software",
            "description": "Install Python tools", 
            "priority": "medium",
            "category": "software_request",
            "requester_email": "user@company.com"
        }
        
        event = {
            "Records": [
                {
                    "body": json.dumps(request_data)
                }
            ]
        }
        
        result = lambda_handler(event)
        
        assert result["statusCode"] == 200
        assert result["body"]["status"] == "COMPLIANT"
    
    def test_lambda_handler_error_handling(self):
        """Test lambda handler error handling"""
        invalid_event = {
            "Records": [
                {
                    "body": "invalid json"
                }
            ]
        }
        
        result = lambda_handler(invalid_event)
        
        assert result["statusCode"] == 500
        assert result["body"]["status"] == "ERROR"


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
