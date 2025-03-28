class Ec2Instance:
    def __init__(self, instance_id, name, autoscaling_group, public_ip, private_ip, launch_time, tags):
        self.instance_id = instance_id
        self.name = name
        self.autoscaling_group = autoscaling_group
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.launch_time = launch_time
        self.tags = tags

    def format_field(self, value, length):
        if len(value) > length:
            return value[:length - 3] + "..."
        return value.ljust(length)

    def __str__(self):
        return f"{self.format_field(self.name, 15)} - {self.format_field(self.autoscaling_group, 20)} - {self.format_field(self.public_ip, 15)} - {self.launch_time}"
