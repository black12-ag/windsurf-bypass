import json
import base64
from colorama import Fore, Style

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "KEY": "🔑"
}

def get_token_from_cookie(cookie_value, translator=None):
    """Extract user token from cookie value"""
    try:
        # Handle different cookie formats
        if not cookie_value:
            print(f"{Fore.RED}{EMOJI['ERROR']} Empty cookie value{Style.RESET_ALL}")
            return None
        
        # If it's already a token (not JWT), return as is
        if '.' not in cookie_value:
            return cookie_value
        
        # Try to decode as JWT token
        try:
            # JWT tokens have 3 parts separated by dots
            parts = cookie_value.split('.')
            if len(parts) != 3:
                # Not a standard JWT, return as is
                return cookie_value
            
            # Decode the payload (second part)
            payload = parts[1]
            
            # Add padding if needed
            padding = 4 - (len(payload) % 4)
            if padding != 4:
                payload += '=' * padding
            
            # Decode base64
            decoded = base64.b64decode(payload)
            payload_data = json.loads(decoded)
            
            # Look for user ID or token in payload
            user_id = payload_data.get('sub') or payload_data.get('user_id') or payload_data.get('userId')
            if user_id:
                return user_id
                
        except Exception as decode_error:
            # If decoding fails, return the original cookie value
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Could not decode JWT token: {decode_error}{Style.RESET_ALL}")
        
        # Return original cookie value as fallback
        return cookie_value
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error extracting token from cookie: {e}{Style.RESET_ALL}")
        return None

def validate_token(token):
    """Validate if token looks like a proper token"""
    if not token:
        return False
    
    # Check if it's a valid string
    if not isinstance(token, str):
        return False
    
    # Basic validation - should not be empty and should have reasonable length
    if len(token) < 10:
        return False
    
    # Should not contain spaces or newlines
    if ' ' in token or '\n' in token or '\r' in token:
        return False
    
    return True

def main():
    """Test function"""
    # Example usage
    test_cookie = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    token = get_token_from_cookie(test_cookie)
    print(f"Extracted token: {token}")

if __name__ == "__main__":
    main()