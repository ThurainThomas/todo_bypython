import paramiko
import time
import re

# --- SSH Connection Details ---
HOSTNAME = "localhost"
PORT = 2222
USERNAME = "sshuser"
PASSWORD = "password"  # Dockerfile ထဲမှာ ထည့်ထားတဲ့ password ကို ဒီမှာ ထည့်ပါ။
# ------------------------------


def parse_ifconfig_output(ifconfig_output: str) -> dict:
    """
    ifconfig command ၏ output မှ eth0 ၏ IP, Netmask, Ether (MAC) address များကို dictionary အဖြစ် ထုတ်ယူသည်။

    Args:
        ifconfig_output (str): ifconfig command မှ ရရှိသော raw text output။

    Returns:
        dict: eth0 ၏ အချက်အလက်များကို Dictionary ပုံစံဖြင့် ပြန်ပေးသည်။
              ဥပမာ: {'inet': '172.17.0.2', 'netmask': '255.255.0.0', 'ether': 'AA:BB:CC:DD:EE:FF'}
              eth0 ကို ရှာမတွေ့ပါက empty dictionary ကို ပြန်ပေးသည်။
    """
    eth0_info = {}

    # eth0 block ကို ရှာရန် regular expression
    eth0_block_match = re.search(
        r"^eth0:.*?^\s*(inet\s+\S+).*?netmask\s+(\S+).*?ether\s+(\S+)",
        ifconfig_output,
        re.DOTALL | re.MULTILINE,
    )

    if eth0_block_match:
        # Captured groups များကို ထုတ်ယူပါ။
        inet_str = eth0_block_match.group(1).strip()
        netmask_str = eth0_block_match.group(2).strip()
        ether_str = eth0_block_match.group(3).strip()

        # "inet" keyword ကို ဖယ်ရှားပြီး IP address ကိုသာ ယူပါ။
        ip_address = inet_str.split()[1] if " " in inet_str else inet_str

        eth0_info = {"inet": ip_address, "netmask": netmask_str, "ether": ether_str}
    return eth0_info


def connect_and_run_command(hostname, port, username, password, command):
    """
    SSH server သို့ ချိတ်ဆက်ပြီး command တစ်ခုကို run ပါသည်။
    stdout output ကို ပြန်ပေးသည်။ stderr output များကိုလည်း ဖော်ပြသည်။
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )  # Unknown host key တွေ့ရင် အလိုအလျောက်လက်ခံရန်

    print(f"Connecting to {username}@{hostname}:{port}...")
    output = ""
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
    return output


if __name__ == "__main__":
    # Docker container နှင့် SSH server အပြည့်အဝ တက်လာရန် အနည်းငယ် စောင့်ဆိုင်းခြင်း
    print("Waiting for Docker container's SSH service to be ready (5 seconds)...")
    time.sleep(5)  # လိုအပ်ပါက ဤ delay ကို ပြင်ဆင်နိုင်သည်

    # ifconfig command ကို run ပါ။
    command_to_execute = "ifconfig"
    raw_ifconfig_output = connect_and_run_command(
        HOSTNAME, PORT, USERNAME, PASSWORD, command_to_execute
    )

    # ifconfig output မှ eth0 အချက်အလက်များကို dictionary အဖြစ် ထုတ်ယူပါ။
    ifconfig_data = parse_ifconfig_output(raw_ifconfig_output)

    if ifconfig_data:
        print("\n--- Parsed eth0 Network Details (JSON-like) ---")
        # dictionary ကို JSON-like string အဖြစ် manually ပြောင်းလဲခြင်း
        json_like_output = "{\n"
        for key, value in ifconfig_data.items():
            json_like_output += f'    "{key}": "{value}",\n'
        # နောက်ဆုံး comma ကို ဖယ်ရှားပြီး bracket ပိတ်ပါ။
        json_like_output = json_like_output.rstrip(",\n") + "\n}"
        print(json_like_output)
        print("----------------------------------------------\n")
    else:
        print("\n--- Could not find eth0 network details in ifconfig output ---")
