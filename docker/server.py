#!/usr/bin/env python3
"""
Simple HTTP server for the IT Request Compliance Validator
Provides health endpoint and validation API for containerized deployment
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os

# Add app directory to path
sys.path.insert(0, '/app')

from app.validator import lambda_handler, ComplianceValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the compliance validator"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/health':
            self.handle_health()
        elif parsed_path.path == '/':
            self.handle_root()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/validate':
            self.handle_validate()
        else:
            self.send_error(404, "Not Found")
    
    def handle_health(self):
        """Health check endpoint"""
        try:
            # Test validator initialization
            validator = ComplianceValidator()
            
            health_data = {
                "status": "healthy",
                "service": "IT Request Compliance Validator",
                "version": "1.0.0",
                "timestamp": "2025-10-11T22:30:00Z"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(health_data, indent=2).encode())
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            self.send_error(500, f"Health check failed: {str(e)}")
    
    def handle_root(self):
        """Root endpoint with service info"""
        info = {
            "service": "IT Request Compliance Validator",
            "version": "1.0.0",
            "endpoints": {
                "health": "GET /health",
                "validate": "POST /validate"
            },
            "description": "Validates IT requests for compliance and data quality"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(info, indent=2).encode())
    
    def handle_validate(self):
        """Validation endpoint"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            request_data = json.loads(post_data.decode())
            
            # Process validation
            result = lambda_handler(request_data)
            
            # Send response
            self.send_response(result.get('statusCode', 200))
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            logger.error(f"Validation error: {e}")
            error_response = {
                "statusCode": 500,
                "body": {
                    "status": "ERROR",
                    "message": f"Validation failed: {str(e)}"
                }
            }
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, indent=2).encode())
    
    def log_message(self, format, *args):
        """Override to use proper logging"""
        logger.info(f"{self.client_address[0]} - {format % args}")


def run_server(port=8080):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ValidatorHandler)
    
    logger.info(f"Starting IT Request Compliance Validator on port {port}")
    logger.info("Available endpoints:")
    logger.info("  GET  /health   - Health check")
    logger.info("  GET  /         - Service info")
    logger.info("  POST /validate - Validate IT request")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run_server(port)
