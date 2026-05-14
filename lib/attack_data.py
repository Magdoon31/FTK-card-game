class AttackData:
    attacks = {}

    @classmethod
    def register(cls, attack):
        cls.attacks[attack.name] = attack

    @classmethod
    def get(cls, name):
        return cls.attacks.get(name)

    @classmethod
    def get_all(cls):
        return cls.attacks
