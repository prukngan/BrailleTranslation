# =====================================================================
# BrailleTranslation_EN.py
# ตัวแปลงอักษรเบรลล์ภาษาอังกฤษ (English Braille Translator)
# อ้างอิงจาก English Braille (Grade 1 / Uncontracted)
# =====================================================================
#
# Braille cell layout (6 dots):
#   dot 1 ● ● dot 4
#   dot 2 ● ● dot 5
#   dot 3 ● ● dot 6
#
# ในโค้ดนี้ เราเก็บเป็น list ของ 3 แถว [row1, row2, row3]
# โดย row1 = (dot1, dot4), row2 = (dot2, dot5), row3 = (dot3, dot6)
# ค่า 0 = ไม่นูน, 1 = นูน

def dots_to_cell(dot_string):
    """แปลง dot string เช่น '1245' เป็น cell [row1, row2, row3]
    โดย row = 0 (ไม่มีจุด), 1 (มีจุดซ้ายอย่างเดียว),
         2 (มีจุดขวาอย่างเดียว), 3 (มีจุดทั้งสองฝั่ง)"""
    dots = set(dot_string)
    r1 = (1 if '1' in dots else 0) + (2 if '4' in dots else 0)
    r2 = (1 if '2' in dots else 0) + (2 if '5' in dots else 0)
    r3 = (1 if '3' in dots else 0) + (2 if '6' in dots else 0)
    return [r1, r2, r3]


# === ตาราง mapping ตัวอักษรอังกฤษ -> dot patterns ===
# เก็บเป็น list ของ dot strings (รองรับ multi-cell)

EN_BRAILLE_MAP = {
    # --- ตัวอักษร (Letters) ---
    'a': ['1'],
    'b': ['12'],
    'c': ['14'],
    'd': ['145'],
    'e': ['15'],
    'f': ['124'],
    'g': ['1245'],
    'h': ['125'],
    'i': ['24'],
    'j': ['245'],
    'k': ['13'],
    'l': ['123'],
    'm': ['134'],
    'n': ['1345'],
    'o': ['135'],
    'p': ['1234'],
    'q': ['12345'],
    'r': ['1235'],
    's': ['234'],
    't': ['2345'],
    'u': ['136'],
    'v': ['1236'],
    'w': ['2456'],
    'x': ['1346'],
    'y': ['13456'],
    'z': ['1356'],

    # --- ตัวเลข (Numbers) ---
    # นำหน้าด้วย number indicator ⠼ (dots 3456)
    '0': ['3456', '245'],
    '1': ['3456', '1'],
    '2': ['3456', '12'],
    '3': ['3456', '14'],
    '4': ['3456', '145'],
    '5': ['3456', '15'],
    '6': ['3456', '124'],
    '7': ['3456', '1245'],
    '8': ['3456', '125'],
    '9': ['3456', '24'],

    # --- เครื่องหมายวรรคตอน (Punctuation) ---
    '.': ['256'],
    ',': ['2'],
    ';': ['23'],
    ':': ['25'],
    '!': ['235'],
    '?': ['236'],
    "'": ['3'],
    '-': ['36'],
    '(': ['126'],
    ')': ['345'],
}


def star(a):
    """แปลงค่า cell row เป็น ASCII art
    3 = ทั้งสองจุด, 2 = จุดขวา, 1 = จุดซ้าย, 0 = ว่าง"""
    if a == 3:
        return "**| "
    if a == 2:
        return "*_| "
    if a == 1:
        return "_*| "
    return "__| "


def translate(text):
    """แปลงข้อความภาษาอังกฤษเป็นอักษรเบรลล์ (ASCII art 3 แถว)"""
    lines = ["", "", ""]

    for ch in text:
        if ch == ' ':
            # ช่องว่าง
            lines[0] += star(0)[::-1]
            lines[1] += star(0)[::-1]
            lines[2] += star(0)[::-1]
        elif ch.lower() in EN_BRAILLE_MAP:
            dot_list = EN_BRAILLE_MAP[ch.lower()]
            for dots in dot_list:
                cell = dots_to_cell(dots)
                lines[0] += star(cell[0])[::-1]
                lines[1] += star(cell[1])[::-1]
                lines[2] += star(cell[2])[::-1]
        else:
            # ตัวอักษรที่ไม่รู้จัก -> แสดงเป็นช่องว่าง
            lines[0] += star(0)[::-1]
            lines[1] += star(0)[::-1]
            lines[2] += star(0)[::-1]

    return lines


# === Main ===
if __name__ == "__main__":
    print("=" * 50)
    print("  ตัวแปลงอักษรเบรลล์ภาษาอังกฤษ")
    print("  English Braille Translator")
    print("=" * 50)
    print()

    text = input("กรุณาพิมพ์ข้อความภาษาอังกฤษ: ")
    result = translate(text)

    print()
    print("ผลลัพธ์อักษรเบรลล์:")
    print("-" * (len(result[0])))
    for line in result:
        print(line)
    print("-" * (len(result[0])))
    print()

    print("ผลลัพธ์อักษรเบรลล์: (mirror)")
    print("-" * (len(result[0])))
    for line in result:
        print(line[::-1])
    print("-" * (len(result[0])))