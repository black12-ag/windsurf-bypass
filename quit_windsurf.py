import os
import platform
import psutil
import time
from colorama import Fore, Style

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "SETTINGS": "⚙️"
}

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

def quit_windsurf(translator=None):
    """Quit Windsurf application"""
    try:
        print(f"{Fore.CYAN}{EMOJI['SETTINGS']} Start Quitting Windsurf...{Style.RESET_ALL}")
        
        # Check if Windsurf is running
        if not is_windsurf_running():
            print(f"{Fore.CYAN}{EMOJI['INFO']} No Running Windsurf Process{Style.RESET_ALL}")
            return True
        
        # Get all Windsurf processes
        processes = get_windsurf_processes()
        print(f"{Fore.CYAN}{EMOJI['INFO']} Found {len(processes)} Windsurf process(es){Style.RESET_ALL}")
        
        # Try to terminate processes gracefully first
        terminated_count = 0
        for process_info in processes:
            try:
                pid = process_info['pid']
                process = psutil.Process(pid)
                
                # Try graceful termination first
                process.terminate()
                terminated_count += 1
                print(f"{Fore.CYAN}{EMOJI['INFO']} Terminated process PID {pid}{Style.RESET_ALL}")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} Could not terminate process PID {pid}: {e}{Style.RESET_ALL}")
                # Try force kill
                try:
                    process = psutil.Process(pid)
                    process.kill()
                    print(f"{Fore.CYAN}{EMOJI['INFO']} Force killed process PID {pid}{Style.RESET_ALL}")
                except Exception as kill_error:
                    print(f"{Fore.RED}{EMOJI['ERROR']} Failed to kill process PID {pid}: {kill_error}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} Error terminating process PID {pid}: {e}{Style.RESET_ALL}")
        
        # Wait a moment for processes to terminate
        time.sleep(2)
        
        # Check if any processes are still running
        if is_windsurf_running():
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} Some Windsurf processes are still running{Style.RESET_ALL}")
            # Try force killing any remaining processes
            remaining_processes = get_windsurf_processes()
            for process_info in remaining_processes:
                try:
                    pid = process_info['pid']
                    process = psutil.Process(pid)
                    process.kill()
                    print(f"{Fore.CYAN}{EMOJI['INFO']} Force killed remaining process PID {pid}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} Failed to kill remaining process PID {pid}: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} All Windsurf processes terminated{Style.RESET_ALL}")
        
        return terminated_count > 0
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Error quitting Windsurf: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main function for testing"""
    quit_windsurf()

if __name__ == "__main__":
    main()