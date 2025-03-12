import requests
import os
import sys

def validate_html():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Looking for HTML files in: {current_dir}")

    # List of HTML files to validate
    html_files = ['home.html', 'about.html', 'services.html', 
                  'portfolio.html', 'contact.html', 'blog.html']
    
    # Check if files exist and are readable
    found_files = []
    for file in html_files:
        full_path = os.path.join(current_dir, file)
        if os.path.isfile(full_path):
            found_files.append(file)
        else:
            print(f"Warning: {file} not found at {full_path}")
    
    if not found_files:
        print("Error: No HTML files found!")
        sys.exit(1)
    
    print(f"\nFound {len(found_files)} HTML files to validate")
    
    for file in found_files:
        try:
            full_path = os.path.join(current_dir, file)
            with open(full_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            print(f"\nValidating {file}...")
            
            headers = {
                'Content-Type': 'text/html; charset=utf-8',
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.post(
                'https://validator.w3.org/nu/?out=json',
                headers=headers,
                data=html_content.encode('utf-8')
            )
            
            results = response.json()
            if len(results['messages']) == 0:
                print(f"✓ {file} is valid!")
            else:
                print(f"Found {len(results['messages'])} issues:")
                for message in results['messages']:
                    print(f"- Line {message.get('lastLine', '?')}: {message['message']}")
        
        except FileNotFoundError:
            print(f"Error: Could not open {file}")
        except Exception as e:
            print(f"Error validating {file}: {str(e)}")

if __name__ == "__main__":
    validate_html()