import random
import string
import time
import requests
from colorama import Fore, Style

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "MAIL": "📧",
    "WAIT": "⏳"
}

class SimpleTempMail:
    def __init__(self, translator=None):
        self.translator = translator
        self.email_address = None
        self.session = requests.Session()
    
    def generate_email(self):
        """Generate a temporary email address"""
        try:
            # Generate random username
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            # Common temporary email domains
            domains = [
                "tempmail.example.com",
                "10minutemail.com",
                "guerrillamail.com",
                "mailinator.com",
                "temp-mail.org"
            ]
            
            # Select random domain
            domain = random.choice(domains)
            
            # Create email address
            self.email_address = f"{username}@{domain}"
            
            print(f"{Fore.CYAN}{EMOJI['MAIL']} Generated temporary email: {self.email_address}{Style.RESET_ALL}")
            return self.email_address
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error generating temporary email: {e}{Style.RESET_ALL}")
            return None
    
    def get_verification_code(self, max_attempts=30, interval=2):
        """Get verification code from email (simulated)"""
        try:
            if not self.email_address:
                print(f"{Fore.RED}{EMOJI['ERROR']} No email address generated{Style.RESET_ALL}")
                return None
            
            print(f"{Fore.CYAN}{EMOJI['WAIT']} Waiting for verification code...{Style.RESET_ALL}")
            
            # Simulate waiting for email
            attempts = 0
            while attempts < max_attempts:
                # Simulate checking for email
                time.sleep(interval)
                attempts += 1
                
                # Simulate random chance of receiving code
                if random.random() < 0.15:  # 15% chance per check
                    # Generate 6-digit verification code
                    code = ''.join(random.choices(string.digits, k=6))
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Verification code received!{Style.RESET_ALL}")
                    return code
                
                print(f"{Fore.YELLOW}{EMOJI['WAIT']} Waiting for email... (attempt {attempts}/{max_attempts}){Style.RESET_ALL}")
            
            print(f"{Fore.RED}{EMOJI['ERROR']} Verification code not received within time limit{Style.RESET_ALL}")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error getting verification code: {e}{Style.RESET_ALL}")
            return None
    
    def get_emails(self):
        """Get list of emails (simulated)"""
        # This is a placeholder for actual email checking implementation
        return []

def main():
    """Test function"""
    temp_mail = SimpleTempMail()
    email = temp_mail.generate_email()
    print(f"Generated email: {email}")
    
    if email:
        code = temp_mail.get_verification_code(max_attempts=5, interval=1)
        print(f"Verification code: {code}")

if __name__ == "__main__":
    main()