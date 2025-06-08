import paramiko
import time

# --- SSH Connection Details ---
HOSTNAME = "localhost"
PORT = 2222
USERNAME = "sshuser"
PASSWORD = "password"  # Dockerfile ထဲမှာ ထည့်ထားတဲ့ password ကို ဒီမှာ ထည့်ပါ။
# ------------------------------


def connect_and_run_sudo_command(
    hostname, port, username, password, sudo_password, command_to_run_as_sudo
):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )  # Unknown host key တွေ့ရင် အလိုအလျောက်လက်ခံရန်

    print(f"Connecting to {username}@{hostname}:{port}...")
    try:
        client.connect(hostname, port, username, password)
        print("Successfully connected!")

        full_command = f"sudo -S bash -c '{command_to_run_as_sudo}'"
        print(f"Executing command: '{full_command}'")

        # Get the channel object for more control over stdin/stdout/stderr
        channel = client.get_transport().open_session()
        channel.exec_command(full_command)

        # Write sudo password to stdin
        channel.sendall(sudo_password + "\n")  # Use sendall for robustness

        stdout_data = channel.makefile("rb", -1).read().decode().strip()
        stderr_data = channel.makefile_stderr("rb", -1).read().decode().strip()

        # Close the channel after reading all output
        channel.close()

        if stdout_data:
            print("\n--- Command Output (stdout) ---")
            print(stdout_data)
            print("-------------------------------\n")

        is_sudo_password_prompt = stderr_data.lower().startswith("[sudo] password for")

        if stderr_data and not is_sudo_password_prompt:
            print("\n--- Command Errors (stderr) ---")
            print(stderr_data)
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
    print("Waiting for Docker container's SSH service to be ready (5 seconds)...")
    time.sleep(5)

    command_to_execute_as_root = "cd / && pwd"
    connect_and_run_sudo_command(
        HOSTNAME, PORT, USERNAME, PASSWORD, PASSWORD, command_to_execute_as_root
    )
