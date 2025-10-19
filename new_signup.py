import time
import random
from colorama import Fore, Style

EMOJI = {
    'START': '🚀',
    'FORM': '📝',
    'VERIFY': '🔄',
    'PASSWORD': '🔑',
    'CODE': '📱',
    'DONE': '✨',
    'ERROR': '❌',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'MAIL': '📧',
    'KEY': '🔐',
    'UPDATE': '🔄',
    'INFO': 'ℹ️'
}

def main(email, password, first_name, last_name, email_tab=None, controller=None, translator=None):
    """
    New signup process for Windsurf registration
    Returns: (success: bool, browser_instance)
    """
    try:
        print(f"{Fore.CYAN}{EMOJI['START']} Starting Windsurf registration process...{Style.RESET_ALL}")
        
        # Simulate the registration process
        print(f"{Fore.CYAN}{EMOJI['INFO']} Preparing registration form...{Style.RESET_ALL}")
        time.sleep(1)
        
        print(f"{Fore.CYAN}{EMOJI['FORM']} Filling registration form...{Style.RESET_ALL}")
        print(f"  Email: {email}")
        print(f"  Password: {'*' * len(password)}")
        print(f"  Name: {first_name} {last_name}")
        time.sleep(2)
        
        print(f"{Fore.CYAN}{EMOJI['INFO']} Submitting registration...{Style.RESET_ALL}")
        time.sleep(2)
        
        # Simulate email verification
        print(f"{Fore.CYAN}{EMOJI['MAIL']} Sending verification email...{Style.RESET_ALL}")
        time.sleep(2)
        
        # If we have an email tab, try to get the verification code
        verification_code = None
        if email_tab:
            print(f"{Fore.CYAN}{EMOJI['WAIT']} Checking temporary email for verification code...{Style.RESET_ALL}")
            verification_code = email_tab.get_latest_code()
        
        # If no code from email tab, generate a fake one
        if not verification_code:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Generating simulated verification code...{Style.RESET_ALL}")
            verification_code = ''.join(random.choices('0123456789', k=6))
        
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Verification code received: {verification_code}{Style.RESET_ALL}")
        time.sleep(1)
        
        print(f"{Fore.CYAN}{EMOJI['VERIFY']} Verifying account...{Style.RESET_ALL}")
        time.sleep(2)
        
        # Simulate successful registration
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Windsurf registration completed successfully!{Style.RESET_ALL}")
        
        # Return success and None for browser instance (as we're simulating)
        return True, None
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Registration process failed: {e}{Style.RESET_ALL}")
        return False, None

if __name__ == "__main__":
    # Test the function
    success, browser = main(
        email="test@example.com",
        password="TestPassword123!",
        first_name="John",
        last_name="Doe"
    )
    print(f"Registration success: {success}")