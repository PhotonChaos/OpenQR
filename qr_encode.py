#
#   OpenQR qr_encode.py
#   By: Carbon
#
#   Handles the encoding of the QRCode data

from enum import Enum


##############################
#   Enums and Constants
#
class EncodingMode(Enum):
    NUMERIC = 0
    ALPHA_NUMERIC = 1
    BYTE = 2
    KANJI = 3

    def __int__(self):
        return self.value


class CorrectionLevel(Enum):
    LOW = 0
    MEDIUM = 1
    QUARTILE = 2
    HIGH = 3


VERSION_TOO_HIGH = 41
ERROR_VERSION = -1

# Turns out there isn't really a formula for calculating the version thresholds.
# So we just hardcode this table. It's not perfect but it works.
#
# Table Guide:
# - Each table corresponds to the thresholds for a given correction mode
# - Rows correspond to version, e.g. low_thresholds[0] corresponds to version 1 (bc 0 indexing)
# - Cols correspond to the character encoding modes: [numeric, alphanumeric, byte, kanji]
#   - e.g. low_thresholds[0][2] corresponds to the threshold for byte encoding for version 1

low_thresholds = [[41, 25, 17, 10], [77, 47, 32, 20], [127, 77, 53, 32], [187, 114, 78, 48], [255, 154, 106, 65],
                  [322, 195, 134, 82], [370, 224, 154, 95], [461, 279, 192, 118], [552, 335, 230, 141],
                  [652, 395, 271, 167], [772, 468, 321, 198], [883, 535, 367, 226], [1022, 619, 425, 262],
                  [1101, 667, 458, 282], [1250, 758, 520, 320], [1408, 854, 586, 361], [1548, 938, 644, 397],
                  [1725, 1046, 718, 442], [1903, 1153, 792, 488], [2061, 1249, 858, 528], [2232, 1352, 929, 572],
                  [2409, 1460, 1003, 618], [2620, 1588, 1091, 672], [2812, 1704, 1171, 721], [3057, 1853, 1273, 784],
                  [3283, 1990, 1367, 842], [3517, 2132, 1465, 902], [3669, 2223, 1528, 940], [3909, 2369, 1628, 1002],
                  [4158, 2520, 1732, 1066], [4417, 2677, 1840, 1132], [4686, 2840, 1952, 1201],
                  [4965, 3009, 2068, 1273], [5253, 3183, 2188, 1347], [5529, 3351, 2303, 1417],
                  [5836, 3537, 2431, 1496], [6153, 3729, 2563, 1577], [6479, 3927, 2699, 1661],
                  [6743, 4087, 2809, 1729], [7089, 4296, 2953, 1817]]

medium_thresholds = [[34, 20, 14, 8], [63, 38, 26, 16], [101, 61, 42, 26], [149, 90, 62, 38], [202, 122, 84, 52],
                     [255, 154, 106, 65], [293, 178, 122, 75], [365, 221, 152, 93], [432, 262, 180, 111],
                     [513, 311, 213, 131], [604, 366, 251, 155], [691, 419, 287, 177], [796, 483, 331, 204],
                     [871, 528, 362, 223], [991, 600, 412, 254], [1082, 656, 450, 277], [1212, 734, 504, 310],
                     [1346, 816, 560, 345], [1500, 909, 624, 384], [1600, 970, 666, 410], [1708, 1035, 711, 438],
                     [1872, 1134, 779, 480], [2059, 1248, 857, 528], [2188, 1326, 911, 561], [2395, 1451, 997, 614],
                     [2544, 1542, 1059, 652], [2701, 1637, 1125, 692], [2857, 1732, 1190, 732], [3035, 1839, 1264, 778],
                     [3289, 1994, 1370, 843], [3486, 2113, 1452, 894], [3693, 2238, 1538, 947],
                     [3909, 2369, 1628, 1002], [4134, 2506, 1722, 1060], [4343, 2632, 1809, 1113],
                     [4588, 2780, 1911, 1176], [4775, 2894, 1989, 1224], [5039, 3054, 2099, 1292],
                     [5313, 3220, 2213, 1362], [5596, 3391, 2331, 1435]]

quartile_thresholds = [[27, 16, 11, 7], [48, 29, 20, 12], [77, 47, 32, 20], [111, 67, 46, 28], [144, 87, 60, 37],
                       [178, 108, 74, 45], [207, 125, 86, 53], [259, 157, 108, 66], [312, 189, 130, 80],
                       [364, 221, 151, 93], [427, 259, 177, 109], [489, 296, 203, 125], [580, 352, 241, 149],
                       [621, 376, 258, 159], [703, 426, 292, 180], [775, 470, 322, 198], [876, 531, 364, 224],
                       [948, 574, 394, 243], [1063, 644, 442, 272], [1159, 702, 482, 297], [1224, 742, 509, 314],
                       [1358, 823, 565, 348], [1468, 890, 611, 376], [1588, 963, 661, 407], [1718, 1041, 715, 440],
                       [1804, 1094, 751, 462], [1933, 1172, 805, 496], [2085, 1263, 868, 534], [2181, 1322, 908, 559],
                       [2358, 1429, 982, 604], [2473, 1499, 1030, 634], [2670, 1618, 1112, 684],
                       [2805, 1700, 1168, 719], [2949, 1787, 1228, 756], [3081, 1867, 1283, 790],
                       [3244, 1966, 1351, 832], [3417, 2071, 1423, 876], [3599, 2181, 1499, 923],
                       [3791, 2298, 1579, 972], [3993, 2420, 1663, 1024]]

high_thresholds = [[17, 10, 7, 4], [34, 20, 14, 8], [58, 35, 24, 15], [82, 50, 34, 21], [106, 64, 44, 27],
                   [139, 84, 58, 36], [154, 93, 64, 39], [202, 122, 84, 52], [235, 143, 98, 60], [288, 174, 119, 74],
                   [331, 200, 137, 85], [374, 227, 155, 96], [427, 259, 177, 109], [468, 283, 194, 120],
                   [530, 321, 220, 136], [602, 365, 250, 154], [674, 408, 280, 173], [746, 452, 310, 191],
                   [813, 493, 338, 208], [919, 557, 382, 235], [969, 587, 403, 248], [1056, 640, 439, 270],
                   [1108, 672, 461, 284], [1228, 744, 511, 315], [1286, 779, 535, 330], [1425, 864, 593, 365],
                   [1501, 910, 625, 385], [1581, 958, 658, 405], [1677, 1016, 698, 430], [1782, 1080, 742, 457],
                   [1897, 1150, 790, 486], [2022, 1226, 842, 518], [2157, 1307, 898, 553], [2301, 1394, 958, 590],
                   [2361, 1431, 983, 605], [2524, 1530, 1051, 647], [2625, 1591, 1093, 673], [2735, 1658, 1139, 701],
                   [2927, 1774, 1219, 750], [3057, 1852, 1273, 784]]


##############################
#   Helper Methods
#

def get_optimal_encoding(message: str) -> EncodingMode:
    """
    Consumes the message as a string, and produces the best encoding mode.
    Kanji isn't supported yet.
    :param message: The message to be encoded
    :return: The optimal encoding mode for message
    """
    optimal_mode = EncodingMode.NUMERIC

    for i in message:
        if not ord("0") <= ord(i) <= ord("9"):
            # We need alphanumeric.
            optimal_mode = EncodingMode.ALPHA_NUMERIC
        if ord("a") <= ord("i") <= ord("z"):
            return EncodingMode.BYTE

    return optimal_mode


def get_optimal_version(message, encoding_mode: EncodingMode, correction_lvl: CorrectionLevel) -> int:
    """
    Produces the smallest version the message can fit in given its encoding mode and error correction level.
    :param message: The message to be encoded
    :param encoding_mode: The mode the message is to be encoded with (numeric, alphanumeric, etc.)
    :param correction_lvl: The level of error correction desired
    :return: The smallest version number which can fit message with the requested settings. -1 if error occured
    """

    version = 0
    correction_map = [[]]

    if correction_lvl == CorrectionLevel.LOW:
        correction_map = low_thresholds
    elif correction_lvl == CorrectionLevel.MEDIUM:
        correction_map = medium_thresholds
    elif correction_lvl == CorrectionLevel.QUARTILE:
        correction_map = quartile_thresholds
    elif correction_lvl == CorrectionLevel.HIGH:
        correction_map = high_thresholds
    else:
        print("[!] Error: Invalid correction level")
        return ERROR_VERSION

    while len(message) > correction_map[version][int(encoding_mode)]:
        version += 1

        if version >= len(correction_map):
            return VERSION_TOO_HIGH

    return version + 1


##############################
#   Main Algorithm
#
def encode_data(message, correction_level) -> list[int]:
    encoding_mode = get_optimal_encoding(message)

    if encoding_mode == EncodingMode.KANJI:
        print("Not supported.")
        return message

    version = get_optimal_version(message, encoding_mode, correction_level)

    # TODO: Encode data

    # TODO: Error correction

    return message
