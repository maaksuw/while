def successful_submission():
    return "Onneksi olkoon, ohjelma toimii oikein!"

def wrong_answer():
    return "Ohjelma antoi väärän vastauksen."

def steplimit_exceeded():
    return "Ohjelma suorittaa liian monta askelta."

def not_WHILEprogram():
    return "Ohjelma ei ole WHILE-ohjelma tai se ei ole annettu oikeassa syntaksissa."

def bracket_missing():
    return "Kaarisulje puuttuu."

def explain_incorrect_answer(input, user_output, correct_output):
    return "Ohjelmasi antoi syötteellä " + input + " tuloksen " + user_output + ".\n" + "Oikea tulos oli " + correct_output + "."

def empty_heading():
    return "Otsikko ei saa olla tyhjä."

def empty_decription():
    return "Tehtävänanto ei saa olla tyhjä."

def invalid_topic():
    return "Aihealue pitää määritellä ja sen pitää olla numero."

def invalid_input_size():
    return "Syötteen koko pitää määritellä ja sen pitää olla numero"
