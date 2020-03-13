import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

OPER_TYPE, COMPANY_NAME, TRUCKS, TRAILERS, COMPANY_WHEELS, WHEELS_NEW, WHEELS_RETREAD, CHOOSING, TYPING_REPLY, TYPING_CHOICE, TYRE_FITMENT, ALIGNMENT, FLEET_SURVEY, FULL_SERVICE, CASING, VISIT, CONTACT_PERSON, PHONE_NUMBER, LOCATION, FEEDBACK = range(20)

size_keyboard = [['295/75 R22.5', '11R22.5','11R24.5'],
                  ['255/70 R22.5', '225/70 R19.5'],
                  ['315/80 R22.5', '385/65 R22.5'],
                  ['Done']]
size = ReplyKeyboardMarkup(size_keyboard, one_time_keyboard=True)

operations_keyboard = [['Contruction', 'Regional', 'National'],
                    ['Waste Removal','Refrigirated Tpt','Fuel Tanker'],
                    ['Livestock','Passenger']]
operation = ReplyKeyboardMarkup(operations_keyboard, one_time_keyboard=True)

survey_keyboard = [['Yes'],
                    ['No']]
survey= ReplyKeyboardMarkup(survey_keyboard, one_time_keyboard=True)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you.'
        'Send /cancel to stop talking to me.\n\n'
        'Pick up Fleet type of operation.',
        reply_markup=operation)

    return OPER_TYPE


def oper_type(update, context):
    user = update.message.from_user
    logger.info("Fleet Type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me Fleet name you visited.')
    
    return COMPANY_NAME


def company_name(update, context):
    user = update.message.from_user
    logger.info("Company name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Gorgeous! Send me number of trucks. For example, 100.')

    return TRUCKS

def trucks_number(update, context):
    user = update.message.from_user
    logger.info("Number of trucks of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Now, send me number of trailers. For example, 100.')

    return TRAILERS


def trailers_number(update, context):
    user = update.message.from_user
    logger.info("Number of trailers of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Gorgeous! Now, send me total number of rolling wheels. For example, 1000.')

    return COMPANY_WHEELS


def company_wheels(update, context):
    user = update.message.from_user
    logger.info("Comapany wheels of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('How many of wheels are new?')

    return WHEELS_NEW

def wheels_new(update, context):
    user = update.message.from_user
    logger.info("Comapany new wheels of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('How many of wheels are retreaded?')

    return WHEELS_RETREAD

def wheels_retreaded(update, context):
    user = update.message.from_user
    logger.info("Company retreaded wheels of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me Fleet size breakdown.\n\n'
                                'Click Done when you are ready to go further.',
                                reply_markup=size)

    return CHOOSING

def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Picked up size is {}. What is the number of tires?'.format(text))

    return TYPING_REPLY


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}You can tell me more, or change provided information.".format(facts_to_str(user_data)),
                              reply_markup=size)

    return CHOOSING


def done(update, context):
    user_data = context.user_data
    user = update.message.from_user
    logger.info("Size breakdown of %s: %s", user.first_name, facts_to_str(user_data))
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "\n\n"
                              "Good work! Does Fleet has on site tire fitment?".format(facts_to_str(user_data)),
                              reply_markup=survey)

    #user_data.clear()
    return TYRE_FITMENT

def tyre_fitment(update, context):
    user = update.message.from_user
    logger.info("Tire fitment of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Does Fleet has alignment?', reply_markup=survey)

    return ALIGNMENT


def alignment(update, context):
    user = update.message.from_user
    logger.info("Alignment of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Does Fleet has survey?', reply_markup=survey)

    return FLEET_SURVEY

def fleet_survey(update, context):
    user = update.message.from_user
    logger.info("Fleet survey of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Does Fleet has 24/7/365 service?', reply_markup=survey)

    return FULL_SERVICE

def full_service(update, context):
    user = update.message.from_user
    logger.info("24/7/365 service of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Does Fleet has casing disposal?', reply_markup=survey)

    return CASING

def casing(update, context):
    user = update.message.from_user
    logger.info("Casing disposal of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Great! When was your visit?\n\n'
                            '(DD/MM/YY)')

    return VISIT

def visit(update, context):
    user = update.message.from_user
    logger.info("Visit date of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me your contact person email address.')

    return CONTACT_PERSON

def contact_person(update, context):
    user = update.message.from_user
    logger.info("Contact person email of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('We are almost done! Send me your contact person phone number.')

    return PHONE_NUMBER

def phone_number(update, context):
    user_data = update.message.from_user
    logger.info("Contact person number of %s: %s", user_data.first_name, update.message.text)
    update.message.reply_text('Now, share with me client location.')

    return LOCATION

def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Tell me the feedback.')

    return FEEDBACK

def feedback(update, context):
    user = update.message.from_user
    logger.info("Feedback of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you for provided information. Have a good day.')

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token="938432929:AAEK4XkoljHNE6ApHtLlZe5o-YaG51kKdCs", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            OPER_TYPE: [MessageHandler(Filters.regex(('^(Contruction|Regional|National|Waste Removal|Refrigirated Tpt|Fuel Tanker|Livestock|Passenger)$')), oper_type)],

            TRUCKS: [MessageHandler(Filters.text, trucks_number)],

            TRAILERS: [MessageHandler(Filters.text, trailers_number)],

            COMPANY_NAME: [MessageHandler(Filters.text, company_name)],

            COMPANY_WHEELS: [MessageHandler(Filters.text, company_wheels)],

            WHEELS_NEW: [MessageHandler(Filters.text, wheels_new)],

            WHEELS_RETREAD: [MessageHandler(Filters.text, wheels_retreaded)],

            CHOOSING: [MessageHandler(Filters.regex('^(295/75 R22.5|11R22.5|11R24.5|255/70 R22.5|225/70 R19.5|315/80 R22.5|385/65 R22.5)$'),
                                      regular_choice),
                       MessageHandler(Filters.regex('^Done$'),
                                      done)
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,regular_choice)],

            TYPING_REPLY: [MessageHandler(Filters.text, received_information)],

            TYRE_FITMENT: [MessageHandler(Filters.regex('^(Yes|No)$'), tyre_fitment)],

            ALIGNMENT: [MessageHandler(Filters.regex('^(Yes|No)$'), alignment)],

            FLEET_SURVEY: [MessageHandler(Filters.regex('^(Yes|No)$'), fleet_survey)],

            FULL_SERVICE: [MessageHandler(Filters.regex('^(Yes|No)$'), full_service)],

            CASING: [MessageHandler(Filters.regex('^(Yes|No)$'), casing)],

            VISIT: [MessageHandler(Filters.text, visit)],

            CONTACT_PERSON: [MessageHandler(Filters.text, contact_person)],

            PHONE_NUMBER: [MessageHandler(Filters.text, phone_number)],

            LOCATION: [MessageHandler(Filters.location, location)],

            FEEDBACK: [MessageHandler(Filters.text, feedback)],

        },

        #fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()