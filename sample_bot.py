from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import datetime
import csv
from itertools import islice

date = datetime.date.today()
day = date.day
month = date.month

updater = Updater('781502290:AAEBJ1mlYvhykR_7_2VTPZ-x8tiNblUcJ84')
SETUP, NORMMENU, CHOOSENORMMENU, VEGMENU, CHOOSEVEGMENU, CHOOSEDAY = range(6)

august_path = '/Users/quahjingwen/Desktop/menu_bot/AugustMenu.csv'
sep_path = '/Users/quahjingwen/Desktop/menu_bot/SeptemberMenu.csv'
oct_path = '/Users/quahjingwen/Desktop/menu_bot/OctoberMenu.csv'
nov_path = '/Users/quahjingwen/Desktop/menu_bot/NovemberMenu.csv'
dec_path = '/Users/quahjingwen/Desktop/menu_bot/DecemberMenu.csv'
veg_path = '/Users/quahjingwen/Desktop/menu_bot/VegetarianMenu.csv'
none = " "
month_path = [veg_path,none,none,none,none,none,none,none,august_path,sep_path,oct_path,nov_path,dec_path,]

def start_method(bot, update):
    """ Start Command """

    startList = [["Normal Menu","Vegetarian Menu"]]

    chat_id = update.message.chat_id
    replyText = update.message.text

    text = """Hello and welcome To Eusoff Hall's Menu bot.
This bot lets you view the breakfast and dinner menu for the day.
First, choose the menu type that you wish to view
"""
    bot.sendChatAction(chat_id, "TYPING")
    update.message.reply_text(text, parse_mode="Markdown",reply_markup=ReplyKeyboardMarkup(startList, one_time_keyboard=True))
    return SETUP

def setup(bot, update):
    """Initialize The User Account For The First Time"""
    chat_id = update.message.chat_id

    if update.message.text == "Normal Menu":
        dayList = [["Today", "Another Day"]]
        bot.sendChatAction(chat_id, "TYPING")
        register_text = """Okay.
Choose which day's menu you would like to view.
"""
        update.message.reply_text(register_text, parse_mode="Markdown",
                                  reply_markup=ReplyKeyboardMarkup(dayList, one_time_keyboard=True))
        print("Going For Normal Menu")
        return NORMMENU ## put CHOOSEDAY instead when the choose_day function is settled

    elif update.message.text == "Vegetarian Menu":
        bot.sendChatAction(chat_id, "TYPING")
        register_text = """Okay.
Which menu would you like to view? (Type in a number from 1 - 21)
        """
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        print("Going For Vegetarian Menu")
        return VEGMENU

    else:
        bot.sendChatAction(chat_id, "TYPING")
        update.message.reply_text("Invalid Command!")

def choose_day(bot,update):
    if update.message.text == "Today":
        return NORMMENU
    else:
        register_text = """Okay.
Type in the date and month in dd(space)mm format.
        """
        #if (replyText[0] == 0):
        #    day = replyText[1]
        #else:
        #    day = replyText [0:2]
        #if (replyText[3] == 0):
        #    month = replyText[4]
        #else:
        #    month = replyText[3:]
        return NORMMENU

def norm_menu(bot, update):
    menuList = [["All Day Menu", "Breakfast Menu", "Dinner Menu"]]

    chat_id = update.message.chat_id
    replyText = update.message.text

    text = """Choose the menu that you would like to view
    """
    bot.sendChatAction(chat_id, "TYPING")
    update.message.reply_text(text, parse_mode="Markdown",
                              reply_markup=ReplyKeyboardMarkup(menuList, one_time_keyboard=True))
    print("Choosing relevant menu")
    return CHOOSENORMMENU

def choose_norm_menu(bot, update):
    """Initialize The User Account For The First Time"""
    print("Choosing norm menu")
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, "TYPING")
    print(day, month)
    day_name = datetime.datetime.now()
    get_dayname = day_name.strftime("%A")
    menu = update.message.text
    print(menu)

    menu_list = []
    correct_row = None
    correct_column = None
    # getting the correct month menu
    month_menu = month_path[month]

    # row index
    i = 0
    with open(month_menu) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            i += 1
            for x in range(6):
                if (row[x] == ''):
                    continue
                # if it is a sat/sun, format is different
                elif (get_dayname == "Saturday" or get_dayname == "Sunday"):
                    if (row[x][0] == menu[0]):
                        # if it is dinner, only have dinner
                        if (menu[0] == 'D'):
                            # check if it is the correct date
                            if (day > 9):
                                if (row[x][8:10] == str(day)):
                                    correct_row = row
                                    correct_column = x
                                    correct_row_index = i
                                    break
                            # day is single digit
                            else:
                                if (row[x][8] == str(day)):
                                    correct_row = row
                                    correct_column = x
                                    correct_row_index = i
                                    break
                        # if wants breakfast, but dont have breakfast
                        elif (menu[0] == 'B'):
                            bot.sendMessage(update.message.chat_id, "No breakfast available")
                            return ConversationHandler.END
                # if is weekday, check for day first
                else:
                    # check the date; if day is double digit
                    if (day > 9):
                        if (row[x][0:2] == str(day)):
                            print("got the correct row and column")
                            correct_row = row
                            correct_column = x
                            correct_row_index = i
                            break
                    # day is single digit
                    else:
                        print("else")
                        if (row[x][0] == str(day)):
                            correct_row = row
                            correct_column = x
                            correct_row_index = i
                            break

    if menu == "Breakfast Menu":
        print("Going For Breakfast Menu")
        print(correct_row)
        print(correct_column)

        with open(month_menu) as file:
            print(correct_row_index)
            sliced_file = islice(file, correct_row_index, None)
            readfile = csv.reader(sliced_file, delimiter=',')
            for row in readfile:
                correct_row_index += 1
                if row[correct_column] == 'Drinks':
                    print(row[correct_column])
                    menu_list.append(row[correct_column])
                    break
                else:
                    print(row[correct_column])
                    menu_list.append(row[correct_column])
        print(correct_row_index)
        with open(month_menu) as last_line:
            slice_last = islice(last_line, correct_row_index, None)
            readfile = csv.reader(slice_last, delimiter=',')
            for row in readfile:
                print(row[correct_column])
                menu_list.append(row[correct_column])
                break
        print(menu_list)

        register_text = ("\n".join(menu_list))
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        bot.sendMessage(update.message.chat_id, "End of Breakfast Menu, bye!")
        return ConversationHandler.END

    elif menu == "All Day Menu":
        print("Going For All Day Menu")
        print(correct_row)
        print(correct_column)

        with open(month_menu) as file:
            print(correct_row_index)
            sliced_file = islice(file, correct_row_index, None)
            readfile = csv.reader(sliced_file, delimiter=',')
            for row in readfile:
                correct_row_index += 1
                if row[correct_column] == 'Dessert':
                    print(row[correct_column])
                    menu_list.append(row[correct_column])
                    break
                else:
                    print(row[correct_column])
                    menu_list.append(row[correct_column])
        print(correct_row_index)
        with open(month_menu) as last_line:
            slice_last = islice(last_line, correct_row_index, None)
            readfile = csv.reader(slice_last, delimiter=',')
            for row in readfile:
                print(row[correct_column])
                menu_list.append(row[correct_column])
                break
        print(menu_list)

        register_text = ("\n".join(menu_list))
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        bot.sendMessage(update.message.chat_id, "End of All Day Menu, bye!")
        return ConversationHandler.END
    # last option is the dinner menu
    else:
        print("Dinner Menu")
        print(correct_row)
        print(correct_column)

        with open(month_menu) as file:
            print(correct_row_index)
            sliced_file = islice(file, correct_row_index, None)
            readfile = csv.reader(sliced_file, delimiter=',')
            for row in readfile:
                correct_row_index += 1
                if row[correct_column] == 'Drinks':
                    break
        correct_row_index +=2
        print(correct_row_index)
        with open(month_menu) as second_part:
            slice_second = islice(second_part, correct_row_index, None)
            readfile = csv.reader(slice_second, delimiter=',')
            for row in readfile:
                correct_row_index +=1
                if row[correct_column] == 'Dessert':
                    print(row[correct_column])
                    menu_list.append(row[correct_column])
                    break
                else:
                    print(row[correct_column])
                    menu_list.append(row[correct_column])
        with open(month_menu) as last_line:
            slice_last = islice(last_line, correct_row_index, None)
            readfile = csv.reader(slice_last, delimiter=',')
            for row in readfile:
                print(row[correct_column])
                menu_list.append(row[correct_column])
                break
        print(menu_list)

        register_text = ("\n".join(menu_list))
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        bot.sendMessage(update.message.chat_id, "End of Dinner Menu, bye!")
        return ConversationHandler.END

def get_veg_menu(bot, update):

    chat_id = update.message.chat_id
    replyText = update.message.text
    chosen_menu = [["Menu " + replyText]]

    text = """Type in the menu that you would like to view
        """
    bot.sendChatAction(chat_id, "TYPING")
    update.message.reply_text(text, parse_mode="Markdown",
                              reply_markup=ReplyKeyboardMarkup(chosen_menu, one_time_keyboard=True))
    return CHOOSEVEGMENU

def choose_veg_menu(bot, update):
    print("Choosing vegetarian menu")
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, "TYPING")
    print(day, month)
    day_name = datetime.datetime.now()
    get_dayname = day_name.strftime("%A")
    menu = update.message.text
    print(menu)

    menu_list = []
    correct_row = None
    correct_column = None

    # row index
    i = 0
    # getting the correct month menu, vegetarian is indexed at 0
    month_menu = month_path[0]
    with open(month_menu) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            i +=1
            for x in range(6):
                if (row[x] == menu):
                    correct_row = row
                    correct_column = x
                    correct_row_index = i
                    break
    menu_list.append(menu)
    with open(month_menu) as second_part:
        slice_second = islice(second_part, correct_row_index+1, correct_row_index+6)
        readfile = csv.reader(slice_second, delimiter=',')
        for row in readfile:
            if row[correct_column][0:4] != "Menu":
                menu_list.append(row[correct_column])
    print(menu_list)
    register_text = ("\n".join(menu_list))
    update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
    bot.sendMessage(update.message.chat_id, "End of Vegetarian Menu, bye!")
    return ConversationHandler.END

def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, "Bye!")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start_method)],

    states = {
        SETUP: [MessageHandler(Filters.text, setup)],
        NORMMENU: [MessageHandler(Filters.text, norm_menu)],
        CHOOSENORMMENU: [MessageHandler(Filters.text, choose_norm_menu)],
        VEGMENU: [MessageHandler(Filters.text, get_veg_menu)],
        CHOOSEVEGMENU: [MessageHandler(Filters.text, choose_veg_menu)],
        CHOOSEDAY: [MessageHandler(Filters.text, choose_day)],

    },

    fallbacks = [CommandHandler('cancel', cancel)]
)
updater.dispatcher.add_handler(conv_handler)

########## Starting Bot ##########
updater.start_polling()
updater.idle()