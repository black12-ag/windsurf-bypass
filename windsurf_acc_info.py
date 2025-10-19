import os
import json
import platform
from colorama import Fore, Style
from config import get_config
from utils import get_user_documents_path

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "USER": "👤",
    "KEY": "🔑"
}

def display_account_info(translator=None):
    """Display current Windsurf account information"""
    try:
        print(f"\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['USER']} Account Information{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        
        # Get configuration
        config = get_config(translator)
        if not config:
            print(f"{Fore.RED}{EMOJI['ERROR']} Configuration not loaded{Style.RESET_ALL}")
            return
        
        # Determine storage file path based on OS
        system = platform.system()
        storage_file = None
        
        if system == "Windows":
            if config.has_section('WindowsPaths') and config.has_option('WindowsPaths', 'storage_path'):
                storage_file = config.get('WindowsPaths', 'storage_path')
        elif system == "Darwin":  # macOS
            if config.has_section('MacPaths') and config.has_option('MacPaths', 'storage_path'):
                storage_file = config.get('MacPaths', 'storage_path')
        elif system == "Linux":
            if config.has_section('LinuxPaths') and config.has_option('LinuxPaths', 'storage_path'):
                storage_file = config.get('LinuxPaths', 'storage_path')
        
        # Check if storage file exists
        if not storage_file or not os.path.exists(storage_file):
            print(f"{Fore.CYAN}{EMOJI['INFO']} No active account found. Please register using option 2.{Style.RESET_ALL}")
            return
        
        # Read storage file
        try:
            with open(storage_file, 'r', encoding='utf-8') as f:
                storage_data = json.load(f)
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error reading storage file: {e}{Style.RESET_ALL}")
            return
        
        # Look for auth data
        auth_data = None
        keys_to_check = [
            'windsurf-auth',
            'windsurf.auth',
            'auth',
            'authentication'
        ]
        
        for key in keys_to_check:
            if key in storage_data:
                auth_data = storage_data[key]
                break
        
        # If no auth data found, check for any keys containing 'auth'
        if not auth_data:
            for key in storage_data.keys():
                if 'auth' in key.lower():
                    auth_data = storage_data[key]
                    break
        
        # Display account information
        if auth_data and isinstance(auth_data, dict):
            email = auth_data.get('email', 'Unknown')
            auth_type = auth_data.get('auth_type', 'Unknown')
            
            print(f"{Fore.GREEN}{EMOJI['USER']} Email: {Fore.CYAN}{email}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['KEY']} Auth Type: {Fore.CYAN}{auth_type}{Style.RESET_ALL}")
            
            # Check for additional info
            if 'updated_at' in auth_data:
                print(f"{Fore.GREEN}{EMOJI['INFO']} Last Updated: {Fore.CYAN}{auth_data['updated_at']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}{EMOJI['INFO']} No active account found. Please register using option 2.{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error displaying account info: {e}{Style.RESET_ALL}")

def main():
    """Main function for testing"""
    display_account_info()

if __name__ == "__main__":
    main()