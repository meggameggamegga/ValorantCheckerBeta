from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('TOKEN_ID')
ADMIN_ID = env.str('ADMIN_ID')
CHAT_ID = env.str('CHAT_ID')
buyer_id = 5200370130
ranks = {
        0: "UNRANKED",
        1: "Unused1",
        2: "Unused2",
        3: "IRON 1",
        4: "IRON 2",
        5: "IRON 3",
        6: "BRONZE 1",
        7: "BRONZE 2",
        8: "BRONZE 3",
        9: "SILVER 1",
        10: "SILVER 2",
        11: "SILVER 3",
        12: "GOLD 1",
        13: "GOLD 2",
        14: "GOLD 3",
        15: "PLATINUM 1",
        16: "PLATINUM 2",
        17: "PLATINUM 3",
        18: "DIAMOND 1",
        19: "DIAMOND 2",
        20: "DIAMOND 3",
        21: "ASCENDANT 1",
        22: "ASCENDANT 2",
        23: "ASCENDANT 3",
        24: "IMMORTAL 1",
        25: "IMMORTAL 2",
        26: "IMMORTAL 3",
        27: "RADIANT",
    }
