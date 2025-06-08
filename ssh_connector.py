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

        # sudo command ကို -S option နဲ့ ခေါ်ပြီး password ကို stdin ကနေ ပို့မယ်။
        # command_to_run_as_sudo ကို quotes '...' နဲ့ ပတ်ပေးရပါမယ်၊ ဒါမှ sudo က command တစ်ခုတည်းလို့ သိမှာပါ။
        full_command = f"sudo -S {command_to_run_as_sudo}"
        print(f"Executing command: '{full_command}'")

        stdin, stdout, stderr = client.exec_command(full_command)

        # sudo password ကို stdin ထဲကို ရိုက်ထည့်လိုက်
        stdin.write(sudo_password + "\n")
        stdin.flush()  # Data ကို ချက်ချင်း ပို့အောင်လုပ်

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
    print("Waiting for Docker container's SSH service to be ready (5 seconds)...")
    time.sleep(5)  # Docker container ရဲ့ SSH service တက်လာဖို့ စောင့်

    # ဥပမာ: root အနေနဲ့ 'whoami' ကို run ကြည့်မယ်
    command_to_execute_whoami = "whoami"
    connect_and_run_sudo_command(
        HOSTNAME, PORT, USERNAME, PASSWORD, PASSWORD, command_to_execute_whoami
    )

    # ဥပမာ: root အနေနဲ့ package တစ်ခု install လုပ်မယ် (sudo apt update && sudo apt install -y something)
    # command_to_execute_install = "apt update && apt install -y nano"
    # connect_and_run_sudo_command(HOSTNAME, PORT, USERNAME, PASSWORD, PASSWORD, command_to_execute_install)
