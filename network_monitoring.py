from io import StringIO


class Component:
    def __init__(self, name, info):
        self.name = name
        self.info = info
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_me(self, prefix, is_last, output):
        connector = '\\-' if is_last else '+-'
        output.write(f"{prefix}{connector}{self.name}, {self.info}\n")
        new_prefix = prefix + ("  " if is_last else "| ")
        for i, child in enumerate(self.children):
            child.print_me(new_prefix, i == len(self.children) - 1, output)

    def clone(self):
        cloned = Component(self.name, self.info)
        cloned.children = [child.clone() for child in self.children]
        return cloned


class CPU(Component):
    def init(self, cores, frequency):
        super().init('CPU', f"{cores} cores @ {frequency}MHz")

    def clone(self):
        return CPU(int(self.info.split()[0]),
                   int(self.info.split('@ ')[1][:-4]))


class Memory(Component):
    def init(self, size):
        super().init('Memory', f"{size} MiB")

    def clone(self):
        return Memory(int(self.info.split()[0]))


class Partition(Component):
    def init(self, size, label):
        super().init(f"[{label}]", f"{size} GiB")

    def clone(self):
        return Partition(int(self.info.split()[0]), self.name.strip('[]'))


class HDD(Component):
    def init(self, size):
        super().init('HDD', f"{size} GiB")

    def add_partition(self, partition):
        self.add_child(partition)

    def clone(self):
        cloned = HDD(int(self.info.split()[0]))
        cloned.children = [child.clone() for child in self.children]
        return cloned


class Host:
    def init(self, name, ip_list, components=None):
        self.name = name
        self.ip_list = ip_list
        self.components = components or []

    def add_component(self, component):
        self.components.append(component)

    def print_me(self, prefix, is_last, output):
        connector = '\\-' if is_last else '+-'
        output.write(f"{prefix}{connector}Host: {self.name}\n")
        new_prefix = prefix + ("  " if is_last else "| ")
        for ip in self.ip_list:
            output.write(f"{new_prefix}+-{ip}\n")
        for i, comp in enumerate(self.components):
            comp.print_me(new_prefix, i == len(self.components) - 1, output)

    def clone(self):
        return Host(
            self.name,
            self.ip_list[:],
            [comp.clone() for comp in self.components]
        )


class Network:
    def __init__(self, name):
        self.name = name
        self.hosts = []

    def add_host(self, host):
        self.hosts.append(host)

    def print_me(self, output=None):
        output = output or StringIO()
        output.write(f"Network: {self.name}\n")
        for i, host in enumerate(self.hosts):
            host.print_me("", i == len(self.hosts) - 1, output)
        if output is None:
            print(output.getvalue())
        return output.getvalue()

    def clone(self):
        cloned = Network(self.name)
        cloned.hosts = [host.clone() for host in self.hosts]
        return cloned

    def find_host(self, name):
        for host in self.hosts:
            if host.name == name:
                return host
        return None
