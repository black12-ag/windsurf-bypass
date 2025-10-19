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
    "KEY": "🔑"
}

def auto_logout(translator=None):
    """Automatically logout any existing Windsurf account"""
    try:
        print(f"{Fore.CYAN}{EMOJI['KEY']} Checking for active Windsurf login...{Style.RESET_ALL}")
        
        # Get configuration
        config = get_config(translator)
        if not config:
            print(f"{Fore.RED}{EMOJI['ERROR']} Configuration not loaded{Style.RESET_ALL}")
            return False
        
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
        
        # Fallback if no config path found
        if not storage_file:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} No storage file path found in configuration{Style.RESET_ALL}")
            return True
        
        # Check if storage file exists
        if not os.path.exists(storage_file):
            print(f"{Fore.CYAN}{EMOJI['INFO']} No active login found{Style.RESET_ALL}")
            return True
        
        # Read storage file
        try:
            with open(storage_file, 'r', encoding='utf-8') as f:
                storage_data = json.load(f)
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error reading storage file: {e}{Style.RESET_ALL}")
            return False
        
        # Check for auth data
        auth_found = False
        keys_to_check = [
            'windsurf-auth',
            'windsurf.auth',
            'auth',
            'authentication'
        ]
        
        for key in keys_to_check:
            if key in storage_data:
                auth_found = True
                # Remove auth data
                del storage_data[key]
                print(f"{Fore.CYAN}{EMOJI['INFO']} Removed {key} from storage{Style.RESET_ALL}")
        
        # Also check for any keys containing 'auth' or 'token'
        keys_to_remove = []
        for key in storage_data.keys():
            if 'auth' in key.lower() or 'token' in key.lower() or 'session' in key.lower():
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del storage_data[key]
            print(f"{Fore.CYAN}{EMOJI['INFO']} Removed {key} from storage{Style.RESET_ALL}")
            auth_found = True
        
        # Save modified storage data back to file
        if auth_found:
            try:
                with open(storage_file, 'w', encoding='utf-8') as f:
                    json.dump(storage_data, f, indent=2, ensure_ascii=False)
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Successfully logged out of Windsurf{Style.RESET_ALL}")
                return True
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} Error saving storage file: {e}{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.CYAN}{EMOJI['INFO']} No active login found{Style.RESET_ALL}")
            return True
            
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error during auto logout: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main function for testing"""
    auto_logout()

if __name__ == "__main__":
    main()