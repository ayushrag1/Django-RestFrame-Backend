from enum import Enum


class EnumChoice(Enum):
    @classmethod
    def dict(cls):
        return {i.name.lower(): i.value for i in cls}

    @classmethod
    def name_list(cls):
        return [name.lower() for name in cls.__members__.keys()]

    @classmethod
    def value_list(cls):
        return list(cls.dict().values())

    @classmethod
    def get_member_value(cls, member_name):
        return cls.__members__[member_name.upper()].value

    @classmethod
    def path_list(cls):
        return [name for name in cls.__members__.keys()]


class ContractType(EnumChoice):
    # RPF = "RPF"
    # SOW = "SOW"
    # SAP = "SAP"
    # WARRANTY = "Warranty"
    CUSTOM = "Custom"

    def __str__(self):
        return f'{self.value}'


class HardCodedContract(EnumChoice):
    SAP = "JCI Enterprise SAP COE_Global SAP Application Maintenance & Support RFP.pdf"
    RPF = "JCI Enterprise SAP COE_Global SAP Application Maintenance & Support RFP.pdf"
    SOW = "JCI Enterprise SAP COE_Global SAP Application Maintenance & Support RFP.pdf"
    WARRANTY = "JCI Enterprise SAP COE_Global SAP Application Maintenance & Support RFP.pdf"

    def __str__(self):
        return f'{self.value}'
