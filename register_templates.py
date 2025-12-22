import os

settings_path = r'd:\Shopina Project\code source\shopina-env\backend\shopina\settings.py'
with open(settings_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_installed_apps = False
inserted = False
for line in lines:
    if 'INSTALLED_APPS = [' in line or 'INSTALLED_APPS = (' in line:
        in_installed_apps = True
    
    if in_installed_apps and (']' in line or ')' in line) and not inserted:
        new_lines.append("    'templates',\n")
        inserted = True
        in_installed_apps = False
    
    if 'templates' in line and in_installed_apps:
        inserted = True
        
    new_lines.append(line)

with open(settings_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

urls_path = r'd:\Shopina Project\code source\shopina-env\backend\shopina\urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
inserted_url = False

for line in lines:
    if 'from django.urls import' in line and 'include' not in line:
        line = line.replace('import path', 'import path, include')
    
    if 'api/templates/' in line:
        inserted_url = True
    
    new_lines.append(line)
    
    if 'urlpatterns = [' in line and not inserted_url:
        new_lines.append("    path('api/templates/', include('templates.urls')),\n")
        inserted_url = True

with open(urls_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Done')
