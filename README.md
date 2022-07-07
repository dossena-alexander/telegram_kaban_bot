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
2. [Usage](#usage)
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
## Menu

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
menu.getMsg() # returns str 
menu.getInlineKeyboard() # returns types.InlineKeyboardMarkup
menu.getReplyKeyboard() # returns types.ReplyKeyboardMarkup(resize_keyboard=True)
```
----
### Keys and keyboard
Keys below will be rowed as you see. 
 In other words, in one row -- two buttons, or if you have three buttons, they will be rowed in two rows: two buttons up, one bottom.
 Keys is a button text and callback data in the same time. Keys must be rowed.    
**For example:**
```python
keys = [
  'key1', 'key2',
  'key3', 'key4'
]

adminMenu.setInlineKeyboard(keys)
adminMenu.rowInlineKeyboard()
```
If you do not want to use Menu() you could use composite of Menu() ReplyKeyboard() or InlineKeyboard(). They have methods:    
1. get()
2. add(keys: list)
3. autoRow()

Or use standart types.ReplyKeyboardMarkup()

----

### Menu
**Instead of:**
```python
def admin(message):
    button1 = types.InlineKeyboardButton(text='button1', callback_data='call_1')
    button2 = types.InlineKeyboardButton(text='button2', callback_data='call_2')
    button3 = types.InlineKeyboardButton(text='button3', callback_data='call_3')
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button2)
    markup.row(button3)
    bot.send_message(message.chat.id, 'msg', reply_markup=markup)
```
**I use:**
```python
Keys = [
    "Key one", "Key two",
         "Key three"
]
msg = "Hello!"
adminMenu.setMsg(msg)
adminMenu.setInlineKeyboard(Keys)
adminMenu.rowInlineKeyboard()

def admin(message):
    bot.send_message(message.chat.id, adminMenu.getMsg(), reply_markup=adminMenu.getInlineKeyboard())
```
[:arrow_up:Contents](#contents)

----
----

