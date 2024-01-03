import re

be_name="default"
# Default zfs datasets layout
zfs_datasets = "/," \
    "/home(mountpoint=/home)," \
    "/tmp(mountpoint=/tmp|exec=on|setuid=off)," \
    "/usr(mountpoint=/usr|canmount=off)," \
    "/usr/ports(setuid=off)," \
    "/usr/src," \
    "/var(mountpoint=/var|canmount=off)," \
    "/var/audit(exec=off|setuid=off)," \
    "/var/crash(exec=off|setuid=off)," \
    "/var/log(exec=off|setuid=off)," \
    "/var/mail(atime=on)," \
    "/var/tmp(setuid=off)"


# Find if pasword contain only lower case and number
def lowerCase(strg, search=re.compile(r'[^a-z]').search):
    return not bool(search(strg))


# Find if pasword contain only upper case
def upperCase(strg, search=re.compile(r'[^A-Z]').search):
    return not bool(search(strg))


# Find if pasword contain only lower case and number
def lowerandNunber(strg, search=re.compile(r'[^a-z0-9]').search):
    return not bool(search(strg))


# Find if pasword contain only upper case and number
def upperandNunber(strg, search=re.compile(r'[^A-Z0-9]').search):
    return not bool(search(strg))


# Find if pasword contain only lower and upper case and
def lowerUpperCase(strg, search=re.compile(r'[^a-zA-Z]').search):
    return not bool(search(strg))


# Find if pasword contain only lower and upper case and
def lowerUpperNumber(strg, search=re.compile(r'[^a-zA-Z0-9]').search):
    return not bool(search(strg))


# Find if password contain only lowercase, uppercase numbers
# and some special character.
def allCharacter(strg):
    search = re.compile(r'[^a-zA-Z0-9~\!@#\$%\^&\*_\+":;\'\-]').search
    return not bool(search(strg))


def password_strength(password, label3):
    same_character_type = any(
        [
            lowerCase(password),
            upperCase(password),
            password.isdigit()
        ]
    )
    mix_character = any(
        [
            lowerandNunber(password),
            upperandNunber(password),
            lowerUpperCase(password)
        ]
    )
    if ' ' in password or '\t' in password:
        label3.set_text("Space not allowed")
    elif len(password) <= 4:
        label3.set_text("Super Weak")
    elif len(password) <= 8 and same_character_type:
        label3.set_text("Super Weak")
    elif len(password) <= 8 and mix_character:
        label3.set_text("Very Weak")
    elif len(password) <= 8 and lowerUpperNumber(password):
        label3.set_text("Fairly Weak")
    elif len(password) <= 8 and allCharacter(password):
        label3.set_text("Weak")
    elif len(password) <= 12 and same_character_type:
        label3.set_text("Very Weak")
    elif len(password) <= 12 and mix_character:
        label3.set_text("Fairly Weak")
    elif len(password) <= 12 and lowerUpperNumber(password):
        label3.set_text("Weak")
    elif len(password) <= 12 and allCharacter(password):
        label3.set_text("Strong")
    elif len(password) <= 16 and same_character_type:
        label3.set_text("Fairly Weak")
    elif len(password) <= 16 and mix_character:
        label3.set_text("Weak")
    elif len(password) <= 16 and lowerUpperNumber(password):
        label3.set_text("Strong")
    elif len(password) <= 16 and allCharacter(password):
        label3.set_text("Fairly Strong")
    elif len(password) <= 20 and same_character_type:
        label3.set_text("Weak")
    elif len(password) <= 20 and mix_character:
        label3.set_text("Strong")
    elif len(password) <= 20 and lowerUpperNumber(password):
        label3.set_text("Fairly Strong")
    elif len(password) <= 20 and allCharacter(password):
        label3.set_text("Very Strong")
    elif len(password) <= 24 and same_character_type:
        label3.set_text("Strong")
    elif len(password) <= 24 and mix_character:
        label3.set_text("Fairly Strong")
    elif len(password) <= 24 and lowerUpperNumber(password):
        label3.set_text("Very Strong")
    elif len(password) <= 24 and allCharacter(password):
        label3.set_text("Super Strong")
    elif same_character_type:
        label3.set_text("Fairly Strong")
    else:
        label3.set_text("Super Strong")
