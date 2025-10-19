import os
import sys
import configparser
from colorama import Fore, Style
from utils import get_user_documents_path, get_linux_windsurf_path, get_default_driver_path, get_default_browser_path
import shutil
import datetime

EMOJI = {
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "SUCCESS": "✅",
    "ADMIN": "🔒",
    "ARROW": "➡️",
    "USER": "👤",
    "KEY": "🔑",
    "SETTINGS": "⚙️"
}

# global config cache
_config_cache = None

def setup_config(translator=None):
    """Setup configuration file and return config object"""
    try:
        # get documents path
        docs_path = get_user_documents_path()
        if not docs_path or not os.path.exists(docs_path):
            # if documents path not found, use current directory
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('config.documents_path_not_found', fallback='Documents path not found, using current directory') if translator else 'Documents path not found, using current directory'}{Style.RESET_ALL}")
            docs_path = os.path.abspath('.')
        
        # normalize path
        config_dir = os.path.normpath(os.path.join(docs_path, ".windsurf-free-vip"))
        config_file = os.path.normpath(os.path.join(config_dir, "config.ini"))
        
        # create config directory, only print message when directory not exists
        dir_exists = os.path.exists(config_dir)
        try:
            os.makedirs(config_dir, exist_ok=True)
            if not dir_exists:  # only print message when directory not exists
                print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('config.config_dir_created', path=config_dir) if translator else f'Config directory created: {config_dir}'}{Style.RESET_ALL}")
        except Exception as e:
            # if cannot create directory, use temporary directory
            import tempfile
            temp_dir = os.path.normpath(os.path.join(tempfile.gettempdir(), ".windsurf-free-vip"))
            temp_exists = os.path.exists(temp_dir)
            config_dir = temp_dir
            config_file = os.path.normpath(os.path.join(config_dir, "config.ini"))
            os.makedirs(config_dir, exist_ok=True)
            if not temp_exists:  # only print message when temporary directory not exists
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('config.using_temp_dir', path=config_dir, error=str(e)) if translator else f'Using temporary directory due to error: {config_dir} (Error: {str(e)})'}{Style.RESET_ALL}")
        
        # create config object
        config = configparser.ConfigParser()
        
        # Default configuration
        default_config = {
            'Browser': {
                'default_browser': 'chrome',
                'chrome_path': get_default_browser_path('chrome'),
                'chrome_driver_path': get_default_driver_path('chrome'),
                'edge_path': get_default_browser_path('edge'),
                'edge_driver_path': get_default_driver_path('edge'),
                'firefox_path': get_default_browser_path('firefox'),
                'firefox_driver_path': get_default_driver_path('firefox'),
                'brave_path': get_default_browser_path('brave'),
                'brave_driver_path': get_default_driver_path('brave'),
                'opera_path': get_default_browser_path('opera'),
                'opera_driver_path': get_default_driver_path('opera'),
                'operagx_path': get_default_browser_path('operagx'),
                'operagx_driver_path': get_default_driver_path('chrome')  # Opera GX 使用 Chrome 驱动
            },
            'Turnstile': {
                'handle_turnstile_time': '2',
                'handle_turnstile_random_time': '1-3'
            },
            'Timing': {
                'min_random_time': '0.1',
                'max_random_time': '0.8',
                'page_load_wait': '0.1-0.8',
                'input_wait': '0.3-0.8',
                'submit_wait': '0.5-1.5',
                'verification_code_input': '0.1-0.3',
                'verification_success_wait': '2-3',
                'verification_retry_wait': '2-3',
                'email_check_initial_wait': '4-6',
                'email_refresh_wait': '2-4',
                'settings_page_load_wait': '1-2',
                'failed_retry_time': '0.5-1',
                'retry_interval': '8-12',
                'max_timeout': '160'
            },
            'Utils': {
                'enabled_update_check': 'True',
                'enabled_force_update': 'False',
                'enabled_account_info': 'True'
            },
            'OAuth': {
                'show_selection_alert': False,  # 默认不显示选择提示弹窗
                'timeout': 120,
                'max_attempts': 3
            },
            'Token': {
                'refresh_server': 'https://token.windsurfpro.com.cn',
                'enable_refresh': True
            },
            'Language': {
                'current_language': '',  # Set by local system detection if empty
                'fallback_language': 'en',
                'auto_update_languages': 'True',
                'language_cache_dir': os.path.join(config_dir, "language_cache")
            }
        }

        # Add system-specific path configuration
        if sys.platform == "win32":
            appdata = os.getenv("APPDATA")
            localappdata = os.getenv("LOCALAPPDATA", "")
            default_config['WindowsPaths'] = {
                'storage_path': os.path.join(appdata, "Windsurf", "User", "globalStorage", "storage.json"),
                'sqlite_path': os.path.join(appdata, "Windsurf", "User", "globalStorage", "state.vscdb"),
                'machine_id_path': os.path.join(appdata, "Windsurf", "machineId"),
                'windsurf_path': os.path.join(localappdata, "Programs", "Windsurf", "resources", "app"),
                'updater_path': os.path.join(localappdata, "windsurf-updater"),
                'update_yml_path': os.path.join(localappdata, "Programs", "Windsurf", "resources", "app-update.yml"),
                'product_json_path': os.path.join(localappdata, "Programs", "Windsurf", "resources", "app", "product.json")
            }
            # Create storage directory
            os.makedirs(os.path.dirname(default_config['WindowsPaths']['storage_path']), exist_ok=True)
            
        elif sys.platform == "darwin":
            default_config['MacPaths'] = {
                'storage_path': os.path.abspath(os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/storage.json")),
                'sqlite_path': os.path.abspath(os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")),
                'machine_id_path': os.path.expanduser("~/Library/Application Support/Windsurf/machineId"),
                'windsurf_path': "/Applications/Windsurf.app/Contents/Resources/app",
                'updater_path': os.path.expanduser("~/Library/Application Support/windsurf-updater"),
                'update_yml_path': "/Applications/Windsurf.app/Contents/Resources/app-update.yml",
                'product_json_path': "/Applications/Windsurf.app/Contents/Resources/app/product.json"
            }
            # Create storage directory
            os.makedirs(os.path.dirname(default_config['MacPaths']['storage_path']), exist_ok=True)
            
        elif sys.platform == "linux":
            # Get the actual user's home directory, handling both sudo and normal cases
            sudo_user = os.environ.get('SUDO_USER')
            current_user = sudo_user if sudo_user else (os.getenv('USER') or os.getenv('USERNAME'))
            
            if not current_user:
                current_user = os.path.expanduser('~').split('/')[-1]
            
            # Handle sudo case
            if sudo_user:
                actual_home = f"/home/{sudo_user}"
                root_home = "/root"
            else:
                actual_home = f"/home/{current_user}"
                root_home = None
            
            if not os.path.exists(actual_home):
                actual_home = os.path.expanduser("~")
            
            # Define base config directory
            config_base = os.path.join(actual_home, ".config")
            
            # Try both "Windsurf" and "windsurf" directory names in both user and root locations
            windsurf_dir = None
            possible_paths = [
                os.path.join(config_base, "Windsurf"),
                os.path.join(config_base, "windsurf"),
                os.path.join(root_home, ".config", "Windsurf") if root_home else None,
                os.path.join(root_home, ".config", "windsurf") if root_home else None
            ]
            
            for path in possible_paths:
                if path and os.path.exists(path):
                    windsurf_dir = path
                    break
            
            if not windsurf_dir:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('config.neither_windsurf_nor_windsurf_directory_found', config_base=config_base) if translator else f'Neither Windsurf nor windsurf directory found in {config_base}'}{Style.RESET_ALL}")
                if root_home:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('config.also_checked', path=f'{root_home}/.config') if translator else f'Also checked {root_home}/.config'}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('config.please_make_sure_windsurf_is_installed_and_has_been_run_at_least_once') if translator else 'Please make sure Windsurf is installed and has been run at least once'}{Style.RESET_ALL}")
            
            # Define Linux paths using the found windsurf directory
            storage_path = os.path.abspath(os.path.join(windsurf_dir, "User/globalStorage/storage.json")) if windsurf_dir else ""
            storage_dir = os.path.dirname(storage_path) if storage_path else ""
            
            # Verify paths and permissions
            try:
                # Check storage directory
                if storage_dir and not os.path.exists(storage_dir):
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('config.storage_directory_not_found', storage_dir=storage_dir) if translator else f'Storage directory not found: {storage_dir}'}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('config.please_make_sure_windsurf_is_installed_and_has_been_run_at_least_once') if translator else 'Please make sure Windsurf is installed and has been run at least once'}{Style.RESET_ALL}")
                
                # Check storage.json with more detailed verification
                if storage_path and os.path.exists(storage_path):
                    # Additional path configuration for Linux
                    default_config['LinuxPaths'] = {
                        'storage_path': storage_path,
                        'sqlite_path': os.path.abspath(os.path.join(windsurf_dir, "User/globalStorage/state.vscdb")) if windsurf_dir else "",
                        'machine_id_path': os.path.expanduser("~/.config/windsurf/machineId"),
                        'windsurf_path': "/usr/share/windsurf/resources/app",
                        'updater_path': os.path.expanduser("~/.config/windsurf-updater"),
                        'update_yml_path': "/usr/share/windsurf/resources/app-update.yml",
                        'product_json_path': "/usr/share/windsurf/resources/app/product.json"
                    }
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.path_verification_failed', error=str(e)) if translator else f'Path verification failed: {str(e)}'}{Style.RESET_ALL}")
        
        # Load existing config or create new one
        if os.path.exists(config_file):
            try:
                config.read(config_file, encoding='utf-8')
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.failed_to_read_config', error=str(e)) if translator else f'Failed to read config file: {str(e)}'}{Style.RESET_ALL}")
                # Use default config if reading fails
                config = configparser.ConfigParser()
        else:
            # Create new config with default values
            config = configparser.ConfigParser()
        
        # Update config with default values if missing
        for section, options in default_config.items():
            if not config.has_section(section):
                config.add_section(section)
            for key, value in options.items():
                if not config.has_option(section, key):
                    config.set(section, key, str(value))
        
        # Save config to file
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.failed_to_save_config', error=str(e)) if translator else f'Failed to save config file: {str(e)}'}{Style.RESET_ALL}")
        
        # Update global cache
        global _config_cache
        _config_cache = config
        
        return config
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.setup_failed', error=str(e)) if translator else f'Configuration setup failed: {str(e)}'}{Style.RESET_ALL}")
        return None

def get_config(translator=None):
    """Get configuration object (cached)"""
    global _config_cache
    if _config_cache is None:
        _config_cache = setup_config(translator)
    return _config_cache

def force_update_config(translator=None):
    """Force update configuration file"""
    global _config_cache
    try:
        # Get documents path
        docs_path = get_user_documents_path()
        if not docs_path or not os.path.exists(docs_path):
            docs_path = os.path.abspath('.')
        
        # Normalize path
        config_dir = os.path.normpath(os.path.join(docs_path, ".windsurf-free-vip"))
        config_file = os.path.normpath(os.path.join(config_dir, "config.ini"))
        
        # Ensure directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        # Get current config
        config = get_config(translator)
        if config:
            # Save to file
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)
            print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('config.config_updated') if translator else 'Configuration file updated'}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.config_not_available') if translator else 'Configuration not available'}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.force_update_failed', error=str(e)) if translator else f'Failed to force update config: {str(e)}'}{Style.RESET_ALL}")

def update_config_section(section, options, translator=None):
    """Update a specific section of the configuration"""
    try:
        config = get_config(translator)
        if not config:
            return False
            
        # Add section if it doesn't exist
        if not config.has_section(section):
            config.add_section(section)
        
        # Update options
        for key, value in options.items():
            config.set(section, key, str(value))
        
        # Save config
        force_update_config(translator)
        return True
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('config.section_update_failed', section=section, error=str(e)) if translator else f'Failed to update config section {section}: {str(e)}'}{Style.RESET_ALL}")
        return False