import requests  
from bottle import (  
    run, post, response, request as bottle_request
)
import datetime
import csv
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from ownbot.auth import requires_usergroup, assign_first_to
from ownbot.admincommands import AdminCommands

BOT_URL = 'https://api.telegram.org/bot781502290:AAEBJ1mlYvhykR_7_2VTPZ-x8tiNblUcJ84/' # <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/

date = datetime.date.today()
day = date.day
month = date.month

august_path = '/Users/quahjingwen/Desktop/menu_bot/AugustMenu.csv'
sep_path = '/Users/quahjingwen/Desktop/menu_bot/SeptemberMenu.csv'
oct_path = '/Users/quahjingwen/Desktop/menu_bot/OctoberMenu.csv'
nov_path = '/Users/quahjingwen/Desktop/menu_bot/NovemberMenu.csv'
dec_path = '/Users/quahjingwen/Desktop/menu_bot/DecemberMenu.csv'
veg_path = '/Users/quahjingwen/Desktop/menu_bot/VegetarianMenu.csv'
none = " "

month_path = [veg_path,none,none,none,none,none,none,none,august_path,sep_path,oct_path,nov_path,dec_path,]

MENU, NORMMENU = range(2)

menu_list = []
chat_id = '246769087'

def start(bot, update):
    text = "Would you like to view the Normal or Vegetarian menu?"
    update.message.reply_text(text)
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, text)
    return MENU

def menu(bot, update):
    choice = update.message.from_user
    if choice == 'Normal':
        update.message.reply_text("Would you like to view the Breakfast or Dinner menu?")
        return NORMMENU
    else:
        update.message.reply_text("What menu number would you like to view?")
        return get_veg_menu

def get_chat_id(data):  
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']

    return chat_id

def get_message(data):  
    """
    Method to extract message id from telegram request.
    """
    message_text = data['message']['text']

    return message_text

def send_message(prepared_data):  
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """ 
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib

def change_text_message(text):  
    """
    To enable turning our message inside out
    """
    return text[::-1]

def prepare_data_for_answer(data):  
    answer = get_message(data)

    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }

    return json_data

# get normal menu (not vegetarian)
def get_menu(bot, update):
    choice = update.message.from_user
    correct_row = None
    correct_column = None
    # getting the correct month menu
    month_menu = month_path[month]
    with open(month_menu):
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            for x in range(6):
                # if it is a sat/sun, format is different
                if (row[x][0] == choice[0]):
                    # if it is dinner, only have dinner
                    if (choice[0] == 'D'):
                        #check if it is the correct date
                        if (day>9):
                            if (row[x][8:10] == str(day)):
                                correct_row = row
                        # day is single digit
                        else:
                            if (row[x][8] == str(day)):
                                correct_row = row
                                correct_column = x
                    # if wants breakfast, but dont have breakfast
                    elif (choice[0] == 'B'):
                        return "No breakfast available"
                # if is weekday, check for day first
                else:
                    # check the date; if day is double digit
                    if (day>9):
                        if(row[x][0:2] == str(day)):
                            correct_row = row
                            correct_column = x
                    # day is single digit
                    else:
                        if(row[x][0] == str(day)):
                            correct_row = row
                            correct_column = x
    # after getting the correct row and columns, go to the appropriate breakfast/dinner menu
    if choice == 'Breakfast':
        while correct_row[correct_column] != 'Drinks':
            menu_list.append(correct_row[correct_column])
            correct_row = correct_row.next()
        menu_list.append(correct_row[correct_column])
        menu_list.append(correct_row.next()[correct_column])
    # choice was Dinner instead
    else:
        while correct_row[correct_column] != 'Dinner':
            correct_row = correct_row.next()
        while correct_row[correct_column] != 'Dessert':
            menu_list.append(correct_row[correct_column])
            correct_row = correct_row.next()
        menu_list.append(correct_row[correct_column])
        menu_list.append(correct_row.next()[correct_column])

    return menu_list

def get_veg_menu(bot, update):
    menu_num = update.message.from_user
    correct_row = None
    correct_column = None
    # getting the correct month menu, vegetarian is indexed at 0
    month_menu = month_path[0]
    with open(month_menu):
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            for x in range(6):
                if (row[x][5] == menu_num):
                    correct_row = row
                    correct_column = x
    # add the menu number into the list and skip the blank line
    menu_list.append(correct_row[correct_column])
    correct_row = correct_row.next()
    correct_row = correct_row.next()
    # iterate until the end point
    while correct_row[correct_column][0:4] != 'Menu' or correct_row[correct_column][0:4] != None:
        menu_list.append(correct_row[correct_column])
        correct_row = correct_row.next()

    return menu_list

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye!')

    return ConversationHandler.END

def print_menu(bot, update, menu_list):
    update.message.reply_text("\n".join(menu_list))

@post('/')
def main():  
    updater = Updater('781502290:AAEBJ1mlYvhykR_7_2VTPZ-x8tiNblUcJ84')
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [RegexHandler('^(Normal|Vegetarian)$', menu)],
            NORMMENU: [RegexHandler('^(Lunch|Dinner)$', get_menu)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    data = "\n".join(menu_list)
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, data)

    updater.start_polling()

    return response  # status 200 OK by default

if __name__ == '__main__':  
    run(host='localhost', port=8080, debug=True)