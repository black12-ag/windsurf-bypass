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
    "KEY": "🔑",
    "SETTINGS": "⚙️"
}

class WindsurfAuth:
    def __init__(self, translator=None):
        self.translator = translator
        self.config = get_config(translator)
        self.auth_file = self._get_auth_file_path()
    
    def _get_auth_file_path(self):
        """Get the path to the Windsurf authentication file"""
        try:
            # Get the configuration
            if not self.config:
                raise Exception("Configuration not loaded")
            
            # Determine the path based on the operating system
            system = platform.system()
            
            if system == "Windows":
                if self.config.has_section('WindowsPaths') and self.config.has_option('WindowsPaths', 'storage_path'):
                    storage_path = self.config.get('WindowsPaths', 'storage_path')
                    auth_dir = os.path.dirname(storage_path)
                else:
                    appdata = os.getenv("APPDATA", "")
                    auth_dir = os.path.join(appdata, "Windsurf", "User", "globalStorage")
                    
            elif system == "Darwin":  # macOS
                if self.config.has_section('MacPaths') and self.config.has_option('MacPaths', 'storage_path'):
                    storage_path = self.config.get('MacPaths', 'storage_path')
                    auth_dir = os.path.dirname(storage_path)
                else:
                    auth_dir = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage")
                    
            elif system == "Linux":
                if self.config.has_section('LinuxPaths') and self.config.has_option('LinuxPaths', 'storage_path'):
                    storage_path = self.config.get('LinuxPaths', 'storage_path')
                    auth_dir = os.path.dirname(storage_path)
                else:
                    # Try to find the Windsurf config directory
                    home = os.path.expanduser("~")
                    config_base = os.path.join(home, ".config")
                    
                    # Check common locations
                    possible_paths = [
                        os.path.join(config_base, "Windsurf", "User", "globalStorage"),
                        os.path.join(config_base, "windsurf", "User", "globalStorage"),
                        os.path.join(home, ".windsurf", "User", "globalStorage")
                    ]
                    
                    auth_dir = None
                    for path in possible_paths:
                        if os.path.exists(os.path.dirname(path)):
                            auth_dir = path
                            break
                    
                    if not auth_dir:
                        auth_dir = possible_paths[0]  # Default to first option
            else:
                # Fallback for other systems
                auth_dir = os.path.expanduser("~/.windsurf/User/globalStorage")
            
            # Ensure the directory exists
            os.makedirs(auth_dir, exist_ok=True)
            
            # Return the full path to the storage.json file
            return os.path.join(auth_dir, "storage.json")
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error determining auth file path: {e}{Style.RESET_ALL}")
            # Fallback to a default location
            docs_path = get_user_documents_path()
            return os.path.join(docs_path, ".windsurf-free-vip", "auth_storage.json")
    
    def _load_auth_data(self):
        """Load authentication data from file"""
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default structure
                return {}
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error loading auth data: {e}{Style.RESET_ALL}")
            return {}
    
    def _save_auth_data(self, data):
        """Save authentication data to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.auth_file), exist_ok=True)
            
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error saving auth data: {e}{Style.RESET_ALL}")
            return False
    
    def update_auth(self, email=None, access_token=None, refresh_token=None, auth_type="Auth_0"):
        """Update Windsurf authentication information"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} Updating Windsurf authentication...{Style.RESET_ALL}")
            
            # Load existing data
            auth_data = self._load_auth_data()
            
            # Update authentication information
            auth_key = "windsurf-auth"
            if auth_key not in auth_data:
                auth_data[auth_key] = {}
            
            # Update the authentication data
            if email:
                auth_data[auth_key]["email"] = email
            if access_token:
                auth_data[auth_key]["access_token"] = access_token
            if refresh_token:
                auth_data[auth_key]["refresh_token"] = refresh_token
            if auth_type:
                auth_data[auth_key]["auth_type"] = auth_type
            
            # Add timestamp
            import time
            auth_data[auth_key]["updated_at"] = time.time()
            
            # Save the updated data
            if self._save_auth_data(auth_data):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Windsurf authentication updated successfully{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} Failed to save Windsurf authentication data{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error updating Windsurf authentication: {e}{Style.RESET_ALL}")
            return False
    
    def get_auth_info(self):
        """Get current authentication information"""
        try:
            auth_data = self._load_auth_data()
            auth_key = "windsurf-auth"
            
            if auth_key in auth_data:
                return auth_data[auth_key]
            else:
                return None
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error retrieving Windsurf authentication info: {e}{Style.RESET_ALL}")
            return None
    
    def clear_auth(self):
        """Clear all authentication information"""
        try:
            auth_data = self._load_auth_data()
            auth_key = "windsurf-auth"
            
            if auth_key in auth_data:
                del auth_data[auth_key]
                return self._save_auth_data(auth_data)
            else:
                return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error clearing Windsurf authentication: {e}{Style.RESET_ALL}")
            return False

def main():
    """Test function"""
    auth_manager = WindsurfAuth()
    
    # Example usage
    print("Testing WindsurfAuth...")
    auth_manager.update_auth(
        email="test@example.com",
        access_token="test_access_token",
        refresh_token="test_refresh_token",
        auth_type="Auth_0"
    )
    
    auth_info = auth_manager.get_auth_info()
    print(f"Auth info: {auth_info}")

if __name__ == "__main__":
    main()