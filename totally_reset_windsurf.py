import os
import platform
import shutil
import json
from colorama import Fore, Style
from config import get_config
from utils import get_user_documents_path, kill_windsurf_processes

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "FILE": "📄",
    "FOLDER": "📁",
    "WARNING": "⚠️"
}

class WindsurfResetter:
    def __init__(self, translator=None):
        self.translator = translator
        self.config = get_config(translator)
    
    def _get_windsurf_paths(self):
        """Get all Windsurf-related paths based on the operating system"""
        system = platform.system()
        paths = {
            'config_dirs': [],
            'config_files': [],
            'cache_dirs': [],
            'data_dirs': []
        }
        
        if system == "Windows":
            appdata = os.getenv("APPDATA", "")
            localappdata = os.getenv("LOCALAPPDATA", "")
            
            if appdata:
                paths['config_dirs'].extend([
                    os.path.join(appdata, "Windsurf"),
                    os.path.join(appdata, "Windsurf", "User")
                ])
                paths['config_files'].append(
                    os.path.join(appdata, "Windsurf", "User", "globalStorage", "storage.json")
                )
            
            if localappdata:
                paths['data_dirs'].extend([
                    os.path.join(localappdata, "Windsurf"),
                    os.path.join(localappdata, "Programs", "Windsurf")
                ])
                paths['cache_dirs'].append(
                    os.path.join(localappdata, "Windsurf", "Cache")
                )
            
        elif system == "Darwin":  # macOS
            paths['config_dirs'].extend([
                os.path.expanduser("~/Library/Application Support/Windsurf"),
                os.path.expanduser("~/Library/Application Support/Windsurf/User"),
                os.path.expanduser("~/Library/Preferences/com.windsurf.app.plist"),
                os.path.expanduser("~/Library/Saved Application State/com.windsurf.app.savedState")
            ])
            
            paths['config_files'].extend([
                os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/storage.json"),
                os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            ])
            
            paths['cache_dirs'].extend([
                os.path.expanduser("~/Library/Caches/com.windsurf.app"),
                os.path.expanduser("~/Library/Caches/Windsurf")
            ])
            
            paths['data_dirs'].append("/Applications/Windsurf.app")
            
        elif system == "Linux":
            home = os.path.expanduser("~")
            config_base = os.path.join(home, ".config")
            
            paths['config_dirs'].extend([
                os.path.join(config_base, "Windsurf"),
                os.path.join(config_base, "windsurf"),
                os.path.join(home, ".windsurf")
            ])
            
            paths['config_files'].extend([
                os.path.join(config_base, "Windsurf", "User", "globalStorage", "storage.json"),
                os.path.join(config_base, "Windsurf", "User", "globalStorage", "state.vscdb")
            ])
            
            paths['cache_dirs'].extend([
                os.path.join(home, ".cache", "windsurf"),
                os.path.join(config_base, "windsurf", "Cache")
            ])
            
            # Common installation paths
            paths['data_dirs'].extend([
                "/usr/share/windsurf",
                "/opt/windsurf",
                os.path.join(home, ".local/share/windsurf")
            ])
        
        return paths
    
    def _safe_remove_path(self, path):
        """Safely remove a file or directory"""
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Removed file: {path}{Style.RESET_ALL}")
                return True
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Removed directory: {path}{Style.RESET_ALL}")
                return True
            else:
                # Path doesn't exist, which is fine
                return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to remove {path}: {e}{Style.RESET_ALL}")
            return False
    
    def _backup_important_data(self):
        """Backup important data before deletion"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} Creating backup of important data...{Style.RESET_ALL}")
            
            # Get documents path for backup location
            docs_path = get_user_documents_path()
            backup_dir = os.path.join(docs_path, ".windsurf-backup")
            
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)
            
            # Get paths to backup
            paths = self._get_windsurf_paths()
            
            # Backup configuration files
            backed_up = 0
            for config_file in paths['config_files']:
                if os.path.exists(config_file):
                    try:
                        filename = os.path.basename(config_file)
                        backup_path = os.path.join(backup_dir, filename)
                        
                        # Copy file to backup location
                        shutil.copy2(config_file, backup_path)
                        print(f"{Fore.CYAN}{EMOJI['INFO']} Backed up: {filename}{Style.RESET_ALL}")
                        backed_up += 1
                        
                    except Exception as e:
                        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to backup {config_file}: {e}{Style.RESET_ALL}")
            
            if backed_up > 0:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Backed up {backed_up} files to {backup_dir}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} No configuration files found to backup{Style.RESET_ALL}")
                
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error during backup: {e}{Style.RESET_ALL}")
            return False
    
    def totally_reset_windsurf(self):
        """Perform a complete reset of Windsurf"""
        try:
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} This will completely remove all Windsurf data!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} This action cannot be undone.{Style.RESET_ALL}")
            
            # Confirm with user
            confirm = input(f"\n{Fore.RED}Type 'RESET' to confirm complete reset: {Style.RESET_ALL}").strip()
            if confirm != "RESET":
                print(f"{Fore.CYAN}{EMOJI['INFO']} Reset cancelled.{Style.RESET_ALL}")
                return False
            
            # Kill any running Windsurf processes
            print(f"{Fore.CYAN}{EMOJI['INFO']} Closing Windsurf processes...{Style.RESET_ALL}")
            kill_windsurf_processes()
            
            # Create backup of important data
            self._backup_important_data()
            
            # Get all paths to remove
            paths = self._get_windsurf_paths()
            
            # Remove configuration directories
            print(f"{Fore.CYAN}{EMOJI['INFO']} Removing configuration directories...{Style.RESET_ALL}")
            for config_dir in paths['config_dirs']:
                self._safe_remove_path(config_dir)
            
            # Remove configuration files
            print(f"{Fore.CYAN}{EMOJI['INFO']} Removing configuration files...{Style.RESET_ALL}")
            for config_file in paths['config_files']:
                self._safe_remove_path(config_file)
            
            # Remove cache directories
            print(f"{Fore.CYAN}{EMOJI['INFO']} Removing cache directories...{Style.RESET_ALL}")
            for cache_dir in paths['cache_dirs']:
                self._safe_remove_path(cache_dir)
            
            # Remove data directories (be careful with this)
            print(f"{Fore.CYAN}{EMOJI['INFO']} Removing data directories...{Style.RESET_ALL}")
            for data_dir in paths['data_dirs']:
                # Only remove user data directories, not system installations
                if "Application Support" in data_dir or ".config" in data_dir or ".windsurf" in data_dir:
                    self._safe_remove_path(data_dir)
            
            # Clear any auth data
            docs_path = get_user_documents_path()
            auth_file = os.path.join(docs_path, ".windsurf-free-vip", "auth_storage.json")
            if os.path.exists(auth_file):
                self._safe_remove_path(auth_file)
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Windsurf has been completely reset!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{EMOJI['INFO']} You can now reinstall Windsurf as a fresh installation.{Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error during complete reset: {e}{Style.RESET_ALL}")
            return False

def run(translator=None):
    """Main function to run the complete reset"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['RESET']} Windsurf Complete Reset Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    resetter = WindsurfResetter(translator)
    success = resetter.totally_reset_windsurf()
    
    if success:
        print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} Complete reset finished successfully!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} Complete reset failed!{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} Press Enter to continue...")

if __name__ == "__main__":
    run()