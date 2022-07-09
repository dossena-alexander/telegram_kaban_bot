# Telegram Kaban Bot

![https://img.shields.io/badge/Python-3.9.12-green](https://img.shields.io/badge/Python-3.9.12-green) 
![https://img.shields.io/badge/Telebot-4.4.1-green](https://img.shields.io/badge/Telebot-4.4.0-green) 
![https://img.shields.io/badge/License-GPL-blue](https://img.shields.io/badge/License-GPL-blue)     
Simple telegram bot written on Python 3 using Telebot. 

----
need to update readme)

----
## Contents:
1. [Setup](#setup)
2. [Class Menu](#class-menu)
3. [Keys and Keyboard](#keys-and-keyboard)
4. [Menu](#menu)
----
----
## Setup
Actual versions:    
+ `python`  3.9.12    
+ `telebot`  4.4.0
    
Setup:
```
pip install telebot
```
[:arrow_up:Contents](#contents)

----
----
## Class Menu

Menu is composite of message and keyboard bot send to user. Creating Menu object
```python
menu = Menu()
```
Set message. Method **.setMsg(msg: str)**:
```python
menu.setMsg("Hello there!")
```
Set keyboard. Methods **.setInlineKeyboard(keys: dict)** and **.setReplyKeyboard(keys: dict)**
```python
menu.setInlineKeyboard(keys_dict)
menu.setReplyKeyboard(keys_dict)
```
To get message or keyboard you should use:
```python
menu.getMsg()            # returns str 
menu.getInlineKeyboard() # returns types.InlineKeyboardMarkup
menu.getReplyKeyboard()  # returns types.ReplyKeyboardMarkup(resize_keyboard=True)
```

[:arrow_up:Contents](#contents)

----
----
### Keys and keyboard
 In one row -- two buttons, or if you have three buttons, they will be rowed in two rows: two buttons in line upper, one bottom.
**For example:**
```python
class KEYS():
    USER = {
        0: { "text": "Upload",                    "call": "UPLOAD_MENU_USER"  }, 
        1: { "text": "Message to admin",          "call": "MESSAGE_TO_ADMIN"  },
        2: { "text": "Boar translation telegram", "call": "TRANSLATE"         }, 
    }

adminMenu.setInlineKeyboard(keys)
```
If you do not want to use Menu() you could use composite of Menu() ReplyKeyboard() or InlineKeyboard(). They have methods:    
| ReplyKeyboard            | InlineKeyboard                      |
| :----------------------: | :---------------------------------: |
| get()                    | get()                               |
| set_keyboard(keys: dict) | set_keyboard(keys: dict)            |
| add_button(text: str)    | add_button(text: str, call: str)    |
|                          | add_url_button(text: str, url: str) |

Or use standart types.ReplyKeyboardMarkup()

[:arrow_up:Contents](#contents)

----
----

### Menu
**Instead of:**
```python
def user(message):
    button1 = types.InlineKeyboardButton(text='Upload', callback_data='UPLOAD_MENU_USER')
    button2 = types.InlineKeyboardButton(text='Message to admin', callback_data='MESSAGE_TO_ADMIN')
    button3 = types.InlineKeyboardButton(text='Boar translation telegram', callback_data='TRANSLATE')
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button2)
    markup.row(button3)
    bot.send_message(message.chat.id, 'msg', reply_markup=markup)
```
**I use:**
```python
class KEYS():
    USER = {
        0: { "text": "Upload",                    "call": "UPLOAD_MENU_USER"  }, 
        1: { "text": "Message to admin",          "call": "MESSAGE_TO_ADMIN"  },
        2: { "text": "Boar translation telegram", "call": "TRANSLATE"         }, 
    }
msg = "Hello!"
userMenu.setMsg(msg)
userMenu.setInlineKeyboard(KEYS.USER)

def user(message):
    bot.send_message(message.chat.id, userMenu.getMsg(), reply_markup=userMenu.getInlineKeyboard())
```
[:arrow_up:Contents](#contents)

----
----

