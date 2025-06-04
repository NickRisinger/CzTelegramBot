import re


def parse_chzn_code(code: str):
    gtin = re.search(r'01(\d{14})', code)
    serial = re.search(r'21([^\x1d]+)', code)
    crypto = re.search(r'93([^\x1d]+)', code)
    return {
        'CLEAN': code.split(' ')[0],
        'GTIN': gtin.group(1) if gtin else 'не найден',
        'Серийный номер': serial.group(1) if serial else 'не найден',
        'Криптокод': crypto.group(1) if crypto else 'не найден'
    }
