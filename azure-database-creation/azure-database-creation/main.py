import random
import string
import subprocess
import json
import sys
import requests


def azure_login():
    """Login to Azure."""
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "login"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error logging in:")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)
    return result


def generate_server_name(base_name="db-verklegt-namskeid-ii-eu"):
    """Generate a unique server name with a random suffix."""
    suffix = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=6))
    return f"{base_name}-{suffix}"


def generate_password(length=12):
    """Generate a random alphanumeric password"""
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(length))
    return password


def create_resource_group(rg_name, location="northeurope"):
    """Create Azure Resource Group."""
    print(f"Creating Resource Group: {rg_name}")
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "group", "create",
        "--name", rg_name,
        "--location", location
    ]

    result = subprocess.run(
        command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error creating resource group:")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)
    return result


def register_postgresql_provider():
    """Register the PostgreSQL provider in Azure."""
    print("Registering PostgreSQL provider...")
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "provider", "register",
        "--namespace", "Microsoft.DBforPostgreSQL"
    ]

    result = subprocess.run(
        command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error registering PostgreSQL provider:")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)
    return result


def create_postgresql_server(server_name, rg_name, admin_user, admin_password):
    """Create PostgreSQL Flexible Server in Azure."""
    password = generate_password(24)
    print(f"Creating PostgreSQL server: {server_name}")
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "postgres", "flexible-server", "create",
        "--resource-group", rg_name,
        "--name", server_name,
        "--location", "northeurope",
        "--admin-user", admin_user,
        "--admin-password", admin_password,
        "--sku-name", "Standard_B1ms",
        "--tier", "Burstable",
        "--storage-size", "32",
        "--version", "16",
        "--yes"
    ]

    result = subprocess.run(
        command, capture_output=True, text=True)
    return result


def create_database(server_name, rg_name, db_name="verklegt_namskeid_db"):
    """Create a new database in the PostgreSQL server."""
    print(f"Creating database: {db_name}")
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "postgres", "flexible-server", "db", "create",
        "--resource-group", rg_name,
        "--server-name", server_name,
        "--database-name", db_name
    ]

    result = subprocess.run(
        command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error creating database:")
        print(result.stderr)
        sys.exit(1)
    return result, db_name


def get_server_details(server_name, rg_name):
    """Get server connection details."""
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "postgres", "flexible-server", "show",
        "--resource-group", rg_name,
        "--name", server_name
    ]

    result = subprocess.run(
        command, capture_output=True, text=True)
    return json.loads(result.stdout)


def format_django_settings(server_details, db_name, admin_user, admin_password):
    """Format Django database settings."""
    host = server_details.get('fullyQualifiedDomainName')

    django_settings = f"""
# PostgreSQL
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{db_name}',
        'USER': '{admin_user}',
        'PASSWORD': '{admin_password}',
        'HOST': '{host}',
        'PORT': '5432'
    }}
}}
"""
    return django_settings


def get_public_ip():
    """Get public IP address using an IP service."""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        try:
            response = requests.get('https://api64.ipify.org')
            return response.text
        except Exception as e:
            print(f"Error getting IP address: {str(e)}")
            return None


def whitelist_your_public_ip(server_name, rg_name):
    """Create firewall rule for your public IP."""
    try:
        public_ip = get_public_ip()
        print(f"Whitelisting IP address: {public_ip}")
        command = [
            r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", "postgres", "flexible-server", "firewall-rule", "create",
            "--resource-group", rg_name,
            "--name", server_name,
            "--rule-name", "allow-my-ip",
            "--start-ip-address", public_ip,
            "--end-ip-address", public_ip
        ]

        result = subprocess.run(
            command, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error creating firewall rule:")
            print(result.stderr)
            return False
        print(result.stdout)
        return True

    except Exception as e:
        print(f"Error setting up firewall rule: {str(e)}")
        return False


def main():
    rg_name = "rg-verklegt-namskeid-ii-eu"
    admin_user = "verklegt_db_user"
    admin_password = generate_password(24)

    azure_login()

    register_postgresql_provider()

    create_resource_group(rg_name)

    server_name = generate_server_name()

    result = create_postgresql_server(
        server_name, rg_name, admin_user, admin_password)
    if result.returncode != 0:
        print("Error creating server:")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)

    whitelist_your_public_ip(server_name, rg_name)

    db_result, db_name = create_database(server_name, rg_name)

    server_details = get_server_details(server_name, rg_name)

    django_settings = format_django_settings(
        server_details, db_name, admin_user, admin_password)

    print("\nServer and database created successfully!")
    print("\nAdd this to your Django settings.py:")
    print(django_settings)

    print("Additional Information:")
    print(f"Server Name: {server_name}")
    print(f"Database Name: {db_name}")
    print(f"Resource Group: {rg_name}")
    print(f"Admin Username: {admin_user}")
    print(f"Admin Password: {admin_password}")

    print("IP whitelisting:")
    print(
        f"   az postgres flexible-server firewall-rule create --resource-group {rg_name} --name {server_name} --rule-name allow-my-ip --start-ip-address <ip-address> --end-ip-address <ip-address>")
    print("Fill in <your-ip> with your group member IP. You will need to run the command for each group member excluding yourself as your IP has been whitelisted.")


if __name__ == "__main__":
    main()
