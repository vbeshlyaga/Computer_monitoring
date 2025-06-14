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
