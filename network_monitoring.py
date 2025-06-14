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
