import os
import sys
import platform
from colorama import Fore, Style
import psutil

EMOJI = {
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "SUCCESS": "✅",
    "FOLDER": "📁",
    "FILE": "📄"
}

def get_user_documents_path():
    """Get the user's Documents folder path"""
    try:
        if platform.system() == "Windows":
            import winreg
            # Try to get the Documents folder from registry
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
                documents_path, _ = winreg.QueryValueEx(key, "Personal")
                winreg.CloseKey(key)
                if os.path.exists(documents_path):
                    return documents_path
            except:
                pass
            
            # Fallback to default path
            return os.path.expanduser("~/Documents")
            
        elif platform.system() == "Darwin":  # macOS
            documents_path = os.path.expanduser("~/Documents")
            if os.path.exists(documents_path):
                return documents_path
            return None
            
        elif platform.system() == "Linux":
            # Try standard locations
            home = os.path.expanduser("~")
            documents_paths = [
                os.path.join(home, "Documents"),
                os.path.join(home, "documents"),
                os.path.join(home, "My Documents")
            ]
            
            for path in documents_paths:
                if os.path.exists(path):
                    return path
            return home
            
        else:
            # Fallback for other systems
            return os.path.expanduser("~/Documents")
            
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to get Documents path: {e}{Style.RESET_ALL}")
        return os.path.expanduser("~/Documents")

def get_default_browser_path(browser_name):
    """Get the default path for a browser"""
    system = platform.system()
    
    if system == "Windows":
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        
        browser_paths = {
            "chrome": [
                os.path.join(program_files, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(program_files_x86, "Google", "Chrome", "Application", "chrome.exe")
            ],
            "edge": [
                os.path.join(program_files, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(program_files_x86, "Microsoft", "Edge", "Application", "msedge.exe")
            ],
            "firefox": [
                os.path.join(program_files, "Mozilla Firefox", "firefox.exe"),
                os.path.join(program_files_x86, "Mozilla Firefox", "firefox.exe")
            ],
            "brave": [
                os.path.join(program_files, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
                os.path.join(program_files_x86, "BraveSoftware", "Brave-Browser", "Application", "brave.exe")
            ]
        }
        
    elif system == "Darwin":  # macOS
        browser_paths = {
            "chrome": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
            "edge": ["/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"],
            "firefox": ["/Applications/Firefox.app/Contents/MacOS/firefox"],
            "brave": ["/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]
        }
        
    elif system == "Linux":
        browser_paths = {
            "chrome": ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"],
            "edge": ["/usr/bin/microsoft-edge"],
            "firefox": ["/usr/bin/firefox"],
            "brave": ["/usr/bin/brave-browser"]
        }
        
    else:
        return ""
    
    # Check if any of the paths exist
    paths = browser_paths.get(browser_name, [])
    for path in paths:
        if os.path.exists(path):
            return path
    
    return ""

def get_default_driver_path(browser_name):
    """Get the default path for a browser driver"""
    # For now, we'll return empty strings as drivers are typically managed by webdriver_manager
    return ""

def get_linux_windsurf_path():
    """Get the Windsurf path on Linux systems"""
    if platform.system() != "Linux":
        return ""
    
    # Common installation paths for Windsurf on Linux
    possible_paths = [
        "/usr/share/windsurf",
        "/opt/windsurf",
        os.path.expanduser("~/.local/share/windsurf"),
        "/snap/windsurf/current",
        "/app/share/windsurf"  # Flatpak
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return ""

def is_windsurf_running():
    """Check if Windsurf is currently running"""
    try:
        for process in psutil.process_iter(['pid', 'name']):
            try:
                # Check for Windsurf processes
                if process.info['name'] and 'windsurf' in process.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error checking if Windsurf is running: {e}{Style.RESET_ALL}")
        return False

def get_windsurf_processes():
    """Get all Windsurf processes"""
    processes = []
    try:
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check for Windsurf processes
                if process.info['name'] and 'windsurf' in process.info['name'].lower():
                    processes.append(process.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error getting Windsurf processes: {e}{Style.RESET_ALL}")
    
    return processes

def kill_windsurf_processes():
    """Kill all Windsurf processes"""
    try:
        killed_count = 0
        for process in psutil.process_iter(['pid', 'name']):
            try:
                # Check for Windsurf processes
                if process.info['name'] and 'windsurf' in process.info['name'].lower():
                    pid = process.info['pid']
                    process = psutil.Process(pid)
                    process.terminate()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if killed_count > 0:
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Killed {killed_count} Windsurf process(es){Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}{EMOJI['INFO']} No Windsurf processes found{Style.RESET_ALL}")
            
        return killed_count > 0
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error killing Windsurf processes: {e}{Style.RESET_ALL}")
        return False