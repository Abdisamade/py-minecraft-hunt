class Elem:
    table_name = None
    def __init__(self, id, name, level, isNewFeature):
        self.id = id
        self.name = name
        self.level = level
        self.isNewFeature = isNewFeature


class Item(Elem):
    table_name = "items"
    def __init__(self, name, level, isNewFeature, id=-1):
        super().__init__(id, name, level, isNewFeature)


class Block(Elem):
    table_name = "blocks"
    def __init__(self, name, level, isNewFeature, id=-1):
        super().__init__(id, name, level, isNewFeature)


class Mob(Elem):
    table_name = "mobs"
    def __init__(self, name, level, isNewFeature, id=-1):
        super().__init__(id, name, level, isNewFeature)

