import paramiko
import time

# --- SSH Connection Details ---
HOSTNAME = "localhost"
PORT = 2222
USERNAME = "sshuser"
PASSWORD = "password"  # Dockerfile ထဲမှာ ထည့်ထားတဲ့ password ကို ဒီမှာ ထည့်ပါ။
# ------------------------------


def connect_and_run_command(hostname, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )  # Unknown host key တွေ့ရင် အလိုအလျောက်လက်ခံရန်

    print(f"Connecting to {username}@{hostname}:{port}...")
    try:
        client.connect(hostname, port, username, password)
        print("Successfully connected!")

        print(f"Executing command: '{command}'")
        stdin, stdout, stderr = client.exec_command(command)

        # Read output from stdout
        output = stdout.read().decode().strip()
        if output:
            print("\n--- Command Output (stdout) ---")
            print(output)
            print("-------------------------------\n")

        # Read output from stderr (for errors)
        errors = stderr.read().decode().strip()
        if errors:
            print("\n--- Command Errors (stderr) ---")
            print(errors)
            print("-------------------------------\n")

    except paramiko.AuthenticationException:
        print("Authentication failed. Check your username and password.")
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if client:
            client.close()
            print("SSH connection closed.")


if __name__ == "__main__":
    # Wait a bit to ensure Docker container and SSH server are fully up
    # This might be needed if you run the script immediately after 'docker run'
    print("Waiting for Docker container's SSH service to be ready (5 seconds)...")
    time.sleep(5)  # You can adjust this delay

    # Run the ifconfig command
    command_to_execute = "ifconfig"
    connect_and_run_command(HOSTNAME, PORT, USERNAME, PASSWORD, command_to_execute)

    # Example of another command
    # connect_and_run_command(HOSTNAME, PORT, USERNAME, PASSWORD, "ls -l /=")
