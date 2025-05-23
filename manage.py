import os
import sys
import django
from tasks import views  

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')    
    django.setup()  

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
