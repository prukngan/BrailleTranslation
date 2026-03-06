from BrailleTranslation_TH import translate

def classify(c):
    if c in "เแโใไ":
        return "Vpre"
    if c in "่้๊๋":
        return "Tone"
    if c in "ะาิีึืุูั":
        return "Vmain"
    if c in "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ":
        return "C"
    if c in ["เอ", "เีย", "เือ", "ัว", "เา"]:
        return "Spelling"
    return "OTHER"

def parse_thai(text_temp: str):
    '''
    แยก พญัชนะ สระ วรรณยุกต์ ยังไม่มีการแปลงเป็นสระพื้นฐาน เช่น เ-ิ -> เ-อ
    '''

    text = text_temp
    
    character = []
    spelling = []
    tone = []
    last_c = []

    if classify(text[0]) == "Vpre":
        # ในกรณีที่มีสระอยู่หน้าพยัญชนะ
        for i in range(1, len(text)):
            if classify(text[1]) != "C":
                break
            character.append(text[1])
            # text.remove(text[1])
            text = text[:1] + text[2:]
        
        for c in text:
            if classify(c) == "Tone":
                tone.append(c)
                # print("Tone: ", tone)
                # text.remove(c)
                text = text.replace(c, "", 1)
                # print("Tone: ", text)
                break

        if classify(text) == "Spelling":
            spelling = [text]
        else:
            if classify(text[-1]) == "C":
                # อักษรท้ายเป็นพยัญชนะ
                last_c = [text[-1]]
                text = text[:-1]
                if text in ["เิ"]:
                    spelling = [text] if text else []
                elif classify(text) == "Spelling":
                    spelling = [text] if text else []
                else:
                    for c in text:
                        tone.append(c)
            else:
                for c in text:
                    spelling.append(c)
                # อื่นๆ
                # spelling_tmp = ""
                # for c in text:
                #     spelling_tmp += c
                #     if classify(spelling_tmp) == "Spelling":
                #         spelling = [spelling_tmp]
                #         text = text[len(spelling_tmp):]

                #         if text == "ะ":
                #             if spelling_tmp == "เา":
                #                 spelling = [spelling_tmp + "ะ"]
                #                 break
                #             spelling.append(text)
                #         else:
                #             last_c = [text]
                #         break

    else:
        for c in text:
            if classify(c) != "C":
                break
            character.append(c)
            text = text[1:]

        spelling_tmp = ""
        for c in text:
            spelling_tmp += c
            if classify(spelling_tmp) == "Spelling":
                spelling = [spelling_tmp]
                text = text[len(spelling_tmp):]
                # print(text)
                if text == "ะ":
                    spelling.append(text)
                else:
                    last_c = [text]
                break

    return character, spelling, tone, last_c

def braille_translate(text: str):
    character, spelling, tone, last_c = parse_thai(text)
    print("Character: ", character)
    print("Spelling: ", spelling)
    print("Tone: ", tone)
    print("Last C: ", last_c)
    if not spelling:
        return text
    elif classify(spelling[0]) == "Vpre":
        return spelling + character + tone + last_c
    elif spelling == ['เอ'] and last_c:
        return text
    elif spelling == ['เิ']:
        spelling = ['เอ']
    return character + spelling + tone + last_c

if __name__ == "__main__":
    from pythainlp.tokenize import word_tokenize
    from BrailleTranslation_TH import translate

    while True:
        text = input("Enter text: ")

        if not text.strip():
            break

        # ตัดคำภาษาไทย
        words = word_tokenize(text, engine="newmm")

        all_trans = []

        for word in words:
            trans_list = braille_translate(word)
            trans_text = translate(trans_list)
            all_trans.append(trans_text)

        print()
        print("ผลลัพธ์อักษรเบรลล์:")

        for trans_text in all_trans:
            print("-" * len(trans_text[0]))
            for line in trans_text:
                print(line)
            print("-" * len(trans_text[0]))

        print()