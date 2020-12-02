import re

def invalid_username():
    return "Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä."

def invalid_password():
    return "Salasanassa tulee olla vähintään 8 merkkiä ja siinä saa käyttää suomalaisen aakkoston isoja ja pieniä kirjaimia. Salasanassa pitää olla vähintään yksi numero."

def mismatch_confirm_password():
    return "Salasanan vahvistus ei täsmää salasanaan."

def username_taken():
    return "Käyttäjänimi on jo varattu."

def wrong_credentials():
    return "Käyttäjänimi tai salasana on väärin."

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

def variablename():
    return "[a-zA-Z]([a-zA-Z]|[0-9])*"

def inputvariables():
    return re.compile("input:(" + variablename() + ",)*" + variablename() + ";")

def variable_assignment():
    return re.compile(variablename() + "=" + variablename() + "[+-]([0-9])*;")

def while_command():
    return re.compile("while[(]" + variablename() + "[!][=]0[)][{]")

def endbracket():
    return re.compile("[}]")

def input_formatter():
    return re.compile("([0-9]* )*[0-9]+")

def valid_password():
    return re.compile("([a-zA-Z]|[öäå]|[ÖÄÅ])*[0-9]([a-zA-Z]|[öäå]|[ÖÄÅ]|[0-9])*")
