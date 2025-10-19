import os
import json
import csv
from datetime import datetime
from colorama import Fore, Style
from utils import get_user_documents_path

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "FILE": "📄",
    "KEY": "🔑"
}

class AccountManager:
    def __init__(self, translator=None):
        self.translator = translator
        self.docs_path = get_user_documents_path()
        self.accounts_dir = os.path.join(self.docs_path, ".windsurf-free-vip", "accounts")
        self.accounts_file = os.path.join(self.accounts_dir, "accounts.json")
        self.csv_file = os.path.join(self.accounts_dir, "accounts.csv")
        
        # Ensure accounts directory exists
        os.makedirs(self.accounts_dir, exist_ok=True)
    
    def _load_accounts(self):
        """Load accounts from file"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error loading accounts: {e}{Style.RESET_ALL}")
            return []
    
    def _save_accounts(self, accounts):
        """Save accounts to file"""
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(accounts, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error saving accounts: {e}{Style.RESET_ALL}")
            return False
    
    def _export_to_csv(self, accounts):
        """Export accounts to CSV file"""
        try:
            if not accounts:
                return True
                
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Email', 'Password', 'Token', 'Usage', 'Created At', 'Status'])
                
                # Write account data
                for account in accounts:
                    writer.writerow([
                        account.get('email', ''),
                        account.get('password', ''),
                        account.get('token', ''),
                        account.get('usage', ''),
                        account.get('created_at', ''),
                        account.get('status', 'active')
                    ])
            
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error exporting to CSV: {e}{Style.RESET_ALL}")
            return False
    
    def save_account_info(self, email, password, token, usage):
        """Save account information to file"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} Saving account information...{Style.RESET_ALL}")
            
            # Load existing accounts
            accounts = self._load_accounts()
            
            # Check if account already exists
            existing_index = None
            for i, account in enumerate(accounts):
                if account.get('email') == email:
                    existing_index = i
                    break
            
            # Create account data
            account_data = {
                'email': email,
                'password': password,
                'token': token,
                'usage': usage,
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            # Update existing or add new
            if existing_index is not None:
                accounts[existing_index] = account_data
                print(f"{Fore.CYAN}{EMOJI['INFO']} Updated existing account: {email}{Style.RESET_ALL}")
            else:
                accounts.append(account_data)
                print(f"{Fore.CYAN}{EMOJI['INFO']} Added new account: {email}{Style.RESET_ALL}")
            
            # Save accounts
            if self._save_accounts(accounts):
                # Export to CSV as well
                self._export_to_csv(accounts)
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Account information saved successfully{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} Failed to save account information{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error saving account info: {e}{Style.RESET_ALL}")
            return False
    
    def get_accounts(self):
        """Get all accounts"""
        return self._load_accounts()
    
    def get_account_by_email(self, email):
        """Get specific account by email"""
        accounts = self._load_accounts()
        for account in accounts:
            if account.get('email') == email:
                return account
        return None
    
    def remove_account(self, email):
        """Remove account by email"""
        try:
            accounts = self._load_accounts()
            filtered_accounts = [acc for acc in accounts if acc.get('email') != email]
            
            if len(filtered_accounts) < len(accounts):
                if self._save_accounts(filtered_accounts):
                    self._export_to_csv(filtered_accounts)
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Account removed: {email}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} Failed to save updated accounts{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} Account not found: {email}{Style.RESET_ALL}")
                return True
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error removing account: {e}{Style.RESET_ALL}")
            return False
    
    def update_account_status(self, email, status):
        """Update account status"""
        try:
            accounts = self._load_accounts()
            updated = False
            
            for account in accounts:
                if account.get('email') == email:
                    account['status'] = status
                    account['updated_at'] = datetime.now().isoformat()
                    updated = True
                    break
            
            if updated:
                if self._save_accounts(accounts):
                    self._export_to_csv(accounts)
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Account status updated: {email} -> {status}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} Failed to save updated accounts{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} Account not found: {email}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error updating account status: {e}{Style.RESET_ALL}")
            return False

def main():
    """Test function"""
    manager = AccountManager()
    
    # Example usage
    print("Testing AccountManager...")
    manager.save_account_info(
        email="test@example.com",
        password="test_password",
        token="test_token",
        usage="100/1000"
    )
    
    accounts = manager.get_accounts()
    print(f"Accounts: {accounts}")

if __name__ == "__main__":
    main()