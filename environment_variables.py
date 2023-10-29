import os 

# Get all environment variables
all_env_vars = os.environ.get('YAHOO')
for key, value in all_env_vars.items():
    print(f'{key}={value}')