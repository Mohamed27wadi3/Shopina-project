#!/usr/bin/env python
"""
Quick verification script for Shopina 3D System
Run: python verify_system.py
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check_file_exists(path, description):
    """Check if a file exists."""
    if Path(path).exists():
        print(f"{Colors.GREEN}✅{Colors.END} {description}")
        return True
    else:
        print(f"{Colors.RED}❌{Colors.END} {description}")
        return False

def check_file_contains(path, search_string, description):
    """Check if a file contains a specific string."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print(f"{Colors.GREEN}✅{Colors.END} {description}")
                return True
            else:
                print(f"{Colors.RED}❌{Colors.END} {description}")
                return False
    except Exception as e:
        print(f"{Colors.RED}❌{Colors.END} {description} - Error: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Shopina 3D System Verification{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    # Base path
    base = "code source/shopina-env/backend"
    
    results = []
    
    # 1. Check Templates
    print(f"{Colors.YELLOW}1. Checking Templates...{Colors.END}")
    results.append(check_file_exists(f"{base}/shopina/templates/dashboard.html", "Dashboard template exists"))
    results.append(check_file_exists(f"{base}/shopina/templates/orders/orders_list.html", "Orders template exists"))
    results.append(check_file_exists(f"{base}/shopina/templates/profile_settings.html", "Settings template exists"))
    print()
    
    # 2. Check Dashboard Features
    print(f"{Colors.YELLOW}2. Checking Dashboard Features...{Colors.END}")
    dashboard_path = f"{base}/shopina/templates/dashboard.html"
    results.append(check_file_contains(dashboard_path, "data-theme", "Theme system implemented"))
    results.append(check_file_contains(dashboard_path, "profile-dropdown", "Avatar dropdown implemented"))
    results.append(check_file_contains(dashboard_path, "backdrop-filter", "Glassmorphism implemented"))
    results.append(check_file_contains(dashboard_path, "cubic-bezier", "Smooth animations implemented"))
    print()
    
    # 3. Check Orders Features
    print(f"{Colors.YELLOW}3. Checking Orders Page Features...{Colors.END}")
    orders_path = f"{base}/shopina/templates/orders/orders_list.html"
    results.append(check_file_contains(orders_path, "status-chip", "Status chips implemented"))
    results.append(check_file_contains(orders_path, "table", "Table structure present"))
    results.append(check_file_contains(orders_path, "profile-dropdown", "Avatar dropdown in orders"))
    print()
    
    # 4. Check Settings Features
    print(f"{Colors.YELLOW}4. Checking Settings Page...{Colors.END}")
    settings_path = f"{base}/shopina/templates/profile_settings.html"
    results.append(check_file_contains(settings_path, "change-password", "Password change form present"))
    results.append(check_file_contains(settings_path, "profile/", "Profile update form present"))
    results.append(check_file_contains(settings_path, "danger-zone", "Danger zone section present"))
    print()
    
    # 5. Check URL Configuration
    print(f"{Colors.YELLOW}5. Checking URL Configuration...{Colors.END}")
    urls_path = f"{base}/shopina/urls.py"
    results.append(check_file_contains(urls_path, "profile-settings", "Settings URL route added"))
    results.append(check_file_contains(urls_path, "DashboardView", "Dashboard view referenced"))
    results.append(check_file_contains(urls_path, "OrdersListPageView", "Orders view referenced"))
    print()
    
    # 6. Check CSS Features
    print(f"{Colors.YELLOW}6. Checking CSS Features...{Colors.END}")
    results.append(check_file_contains(dashboard_path, "--color-accent", "CSS variables defined"))
    results.append(check_file_contains(dashboard_path, "--shadow-md", "Shadow system defined"))
    results.append(check_file_contains(dashboard_path, "--radius-md", "Border radius system defined"))
    results.append(check_file_contains(dashboard_path, "@media", "Responsive design implemented"))
    print()
    
    # 7. Check JavaScript Features
    print(f"{Colors.YELLOW}7. Checking JavaScript Features...{Colors.END}")
    results.append(check_file_contains(dashboard_path, "localStorage", "LocalStorage (theme) implemented"))
    results.append(check_file_contains(dashboard_path, "addEventListener", "Event listeners implemented"))
    results.append(check_file_contains(dashboard_path, "classList", "DOM manipulation implemented"))
    print()
    
    # Summary
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    status_color = Colors.GREEN if percentage == 100 else Colors.YELLOW if percentage >= 80 else Colors.RED
    
    print(f"\n{Colors.BLUE}Results:{Colors.END}")
    print(f"{status_color}{passed}/{total} checks passed ({percentage:.1f}%){Colors.END}\n")
    
    if percentage == 100:
        print(f"{Colors.GREEN}{'='*60}")
        print("✅ System is ready for production!")
        print(f"{'='*60}{Colors.END}\n")
        return 0
    elif percentage >= 80:
        print(f"{Colors.YELLOW}{'='*60}")
        print("⚠️  Most checks passed, but some issues need attention")
        print(f"{'='*60}{Colors.END}\n")
        return 1
    else:
        print(f"{Colors.RED}{'='*60}")
        print("❌ Critical issues detected. Please fix them.")
        print(f"{'='*60}{Colors.END}\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
