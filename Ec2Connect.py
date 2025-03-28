import os
import shutil

import boto3
import questionary
import yaml
from questionary import Choice

from models.Ec2Instance import Ec2Instance


def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def list_ec2_instances(profile):
    session = boto3.Session(profile_name=profile["name"])
    ec2 = session.client("ec2")
    response = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            name_ec2 = "Sin nombre"
            name_ag = "Sin grupo"
            for tags in instance.get("Tags", []):
                if tags.get("Key") == "Name":
                    name_ec2 = tags["Value"]
                if tags.get("Key") == "aws:autoscaling:groupName":
                    name_ag = tags["Value"]
            instances.append(
                Ec2Instance(instance.get("InstanceId"), name_ec2, name_ag, instance.get("PublicIpAddress", "N/A"),
                            instance.get("PrivateIpAddress"), instance.get("LaunchTime"), instance.get("Tags", [])))
    instances = sorted(instances, key=lambda x: x.launch_time)
    return instances


def open_ssh_tabs(instancia, key_path, user, terminal, autorun):
    ip = instancia.public_ip
    if ip == "N/A":
        print(f"Skipping {instancia.instance_id} (No Public IP)")
        return
    optional = ""
    if autorun:
        optional = " -t"
    if terminal == "gnome-terminal":
        comando = f"gnome-terminal --tab -- ssh -oStrictHostKeyChecking=accept-new {optional} -i {key_path} {user}@{ip}"
    elif terminal == "konsole":
        comando = f"konsole --new-tab -e ssh -oStrictHostKeyChecking=accept-new {optional} -i {key_path} {user}@{ip}"
    elif terminal == "xterm":
        comando = f"xterm -e 'ssh -oStrictHostKeyChecking=accept-new {optional} -i {key_path} {user}@{ip}'"
    else:
        return

    # ToDo: Multiples valores de un tag separados por espacios
    if autorun:
        for tag in instancia.tags:
            autorun = autorun.replace("{" + tag.get("Key") + "}", tag.get("Value"))
        comando += f" \"{autorun}; bash\""

    os.system(f"{comando}")


# 🟢 Detectar qué terminal está disponible
def detectar_terminal():
    if shutil.which("gnome-terminal"):
        return "gnome-terminal"
    elif shutil.which("konsole"):
        return "konsole"
    elif shutil.which("xterm"):
        return "xterm"
    else:
        return None


def select_instances(selected_profile, instances):
    while True:
        try:
            choices_ec2 = []
            for instance in instances:
                choices_ec2.append(Choice(f"{instance}", value=instance))

            selected_instances = questionary.checkbox(
                "Seleccione instancias:",
                choices=choices_ec2).ask()
        except KeyboardInterrupt:  # Captura Ctrl+C (por si acaso)
            print("\nOperación cancelada (Ctrl+C). Volviendo...")
            break
        except questionary.exceptions.Aborted:
            # El usuario presionó Esc
            print("\nOperación cancelada. Volviendo al menú anterior...")
            break

        if not selected_instances or "Volver" in selected_instances:
            return

        user = selected_profile["ssh"]["user"]
        key_path = os.path.expandvars(selected_profile["ssh"]["credentials-file"])  # Reemplaza $HOME
        command = selected_profile["ssh"]["autorun"]
        terminal = detectar_terminal()
        for ec2 in selected_instances:
            print(f"Selected: {ec2}")
            open_ssh_tabs(ec2, key_path, user, terminal, command)


def main():
    while True:
        config = load_config("application.yml")
        profiles = config["aws"]["profiles"]

        choices_profile = []
        for p in profiles:
            choices_profile.append(Choice(p["description"], value=p))
        choices_profile.append(Choice("Cancelar", value=None, shortcut_key="c"))
        selected_profile = questionary.select("Seleccione un perfil:", choices=choices_profile,
                                              use_shortcuts=True).ask()
        if not selected_profile or selected_profile == "Cancelar":
            return

        instances = list_ec2_instances(selected_profile)
        if not instances:
            print("No hay instancias en ejecución.")
            continue

        select_instances(selected_profile, instances)


if __name__ == "__main__":
    main()
