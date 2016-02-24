__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class IntentionMap:

    INTENTION_MAP = {
        "Agriculture": [
            "Agriculture", "Biofuels", "Food crops", "Livestock", "Non-food agricultural commodities", "Agriunspecified"
        ],
        "Forestry": ["Forestry", "For wood and fibre", "For carbon sequestration/REDD", "Forestunspecified"],
        "Mining": ["Mining",],
        "Tourism": ["Tourism",],
        "Land Speculation": ["Land Speculation",],
        "Industry":["Industry",],
        "Conservation": ["Conservation",],
        "Renewable Energy": ["Renewable Energy",],
        "Other": ["Other (please specify)",],
    }

    @classmethod
    def get_parent(cls, intention):
        for parent, subintentions in cls.INTENTION_MAP.items():
            if intention in subintentions:
                return parent
        return intention

    @classmethod
    def has_subintentions(cls, intention):
        return len(cls.INTENTION_MAP.get(intention, [])) > 1
