import os
import platform
import uuid
import shutil
import json
from colorama import Fore, Style
from config import get_config
from utils import get_user_documents_path

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "FILE": "📄",
    "FOLDER": "📁"
}

class MachineIDResetter:
    def __init__(self, translator=None):
        self.translator = translator
        self.config = get_config(translator)
    
    def _get_machine_id_paths(self):
        """Get all possible machine ID file paths based on the operating system"""
        system = platform.system()
        paths = []
        
        if system == "Windows":
            if self.config and self.config.has_section('WindowsPaths'):
                if self.config.has_option('WindowsPaths', 'machine_id_path'):
                    paths.append(self.config.get('WindowsPaths', 'machine_id_path'))
            
            # Fallback paths
            appdata = os.getenv("APPDATA", "")
            if appdata:
                paths.append(os.path.join(appdata, "Windsurf", "machineId"))
            
        elif system == "Darwin":  # macOS
            if self.config and self.config.has_section('MacPaths'):
                if self.config.has_option('MacPaths', 'machine_id_path'):
                    paths.append(self.config.get('MacPaths', 'machine_id_path'))
            
            # Fallback paths
            paths.append(os.path.expanduser("~/Library/Application Support/Windsurf/machineId"))
            
        elif system == "Linux":
            if self.config and self.config.has_section('LinuxPaths'):
                if self.config.has_option('LinuxPaths', 'machine_id_path'):
                    paths.append(self.config.get('LinuxPaths', 'machine_id_path'))
            
            # Fallback paths
            home = os.path.expanduser("~")
            paths.extend([
                os.path.join(home, ".config", "windsurf", "machineId"),
                os.path.join(home, ".windsurf", "machineId")
            ])
        
        return paths
    
    def _get_storage_paths(self):
        """Get all possible storage file paths"""
        system = platform.system()
        paths = []
        
        if system == "Windows":
            if self.config and self.config.has_section('WindowsPaths'):
                if self.config.has_option('WindowsPaths', 'storage_path'):
                    paths.append(self.config.get('WindowsPaths', 'storage_path'))
            
        elif system == "Darwin":  # macOS
            if self.config and self.config.has_section('MacPaths'):
                if self.config.has_option('MacPaths', 'storage_path'):
                    paths.append(self.config.get('MacPaths', 'storage_path'))
            
        elif system == "Linux":
            if self.config and self.config.has_section('LinuxPaths'):
                if self.config.has_option('LinuxPaths', 'storage_path'):
                    paths.append(self.config.get('LinuxPaths', 'storage_path'))
        
        return paths
    
    def _generate_new_machine_id(self):
        """Generate a new machine ID"""
        return str(uuid.uuid4())
    
    def _reset_machine_id_file(self, file_path):
        """Reset a single machine ID file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Generate new machine ID
            new_id = self._generate_new_machine_id()
            
            # Write new ID to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_id)
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Reset machine ID file: {file_path}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to reset machine ID file {file_path}: {e}{Style.RESET_ALL}")
            return False
    
    def _clear_storage_files(self):
        """Clear storage files that might contain machine identification"""
        try:
            storage_paths = self._get_storage_paths()
            cleared_count = 0
            
            for storage_path in storage_paths:
                if os.path.exists(storage_path):
                    try:
                        # Read the storage file
                        with open(storage_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Remove machine-specific data
                        keys_to_remove = [
                            'machineId',
                            'deviceId',
                            'installationId',
                            'telemetry.machineId',
                            'telemetry.deviceId'
                        ]
                        
                        modified = False
                        for key in keys_to_remove:
                            if key in data:
                                del data[key]
                                modified = True
                            # Also check nested keys
                            parts = key.split('.')
                            if len(parts) > 1 and parts[0] in data and parts[1] in data[parts[0]]:
                                del data[parts[0]][parts[1]]
                                modified = True
                        
                        # Save modified data back
                        if modified:
                            with open(storage_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Cleared machine ID data from: {storage_path}{Style.RESET_ALL}")
                            cleared_count += 1
                            
                    except Exception as e:
                        print(f"{Fore.RED}{EMOJI['ERROR']} Error processing storage file {storage_path}: {e}{Style.RESET_ALL}")
            
            return cleared_count > 0
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error clearing storage files: {e}{Style.RESET_ALL}")
            return False
    
    def _backup_files(self):
        """Create backups of existing machine ID files"""
        try:
            machine_id_paths = self._get_machine_id_paths()
            backup_count = 0
            
            for file_path in machine_id_paths:
                if os.path.exists(file_path):
                    try:
                        # Create backup filename
                        backup_path = file_path + ".backup"
                        
                        # Copy file to backup location
                        shutil.copy2(file_path, backup_path)
                        print(f"{Fore.CYAN}{EMOJI['INFO']} Backed up: {file_path} -> {backup_path}{Style.RESET_ALL}")
                        backup_count += 1
                        
                    except Exception as e:
                        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to backup {file_path}: {e}{Style.RESET_ALL}")
            
            return backup_count > 0
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error during backup: {e}{Style.RESET_ALL}")
            return False
    
    def reset_machine_ids(self):
        """Reset all machine ID files"""
        try:
            print(f"{Fore.CYAN}{EMOJI['RESET']} Starting machine ID reset process...{Style.RESET_ALL}")
            
            # Create backups first
            print(f"{Fore.CYAN}{EMOJI['INFO']} Creating backups...{Style.RESET_ALL}")
            self._backup_files()
            
            # Reset machine ID files
            print(f"{Fore.CYAN}{EMOJI['INFO']} Resetting machine ID files...{Style.RESET_ALL}")
            machine_id_paths = self._get_machine_id_paths()
            reset_count = 0
            
            for file_path in machine_id_paths:
                if self._reset_machine_id_file(file_path):
                    reset_count += 1
            
            # Clear storage files
            print(f"{Fore.CYAN}{EMOJI['INFO']} Clearing storage files...{Style.RESET_ALL}")
            self._clear_storage_files()
            
            if reset_count > 0:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Machine ID reset completed successfully!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} No machine ID files were reset{Style.RESET_ALL}")
                return True  # Not necessarily an error
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error resetting machine IDs: {e}{Style.RESET_ALL}")
            return False

def run(translator=None):
    """Main function to run the machine ID reset"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['RESET']} Windsurf Machine ID Reset Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    resetter = MachineIDResetter(translator)
    success = resetter.reset_machine_ids()
    
    if success:
        print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} Machine ID reset completed!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['INFO']} You can now use Windsurf without machine restrictions.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} Machine ID reset failed!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} Please run the tool as administrator/root and try again.{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} Press Enter to continue...")

if __name__ == "__main__":
    run()