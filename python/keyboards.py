from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

kb_finance_start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='neuer Eintrag', callback_data='billing')
    ],
    [
        InlineKeyboardButton(text='Kontostände', callback_data='balance'),
        InlineKeyboardButton(text='letzen Eintrag löschen', callback_data='delete')
    ],
    [
        InlineKeyboardButton(text='Verlauf', callback_data='history'),
        InlineKeyboardButton(text='Überweisung', callback_data='transaction')
    ]
])

kb_teilnehmer = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Max"), KeyboardButton(text="Nawid")
    ],
    [
        KeyboardButton(text="Noah"), KeyboardButton(text="Seb")
    ],
    [
        KeyboardButton(text="Alle")
    ],
    [
        KeyboardButton(text="Fertig!")
    ]
])

kb_ja_nein = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="JA")
    ],
    [
        KeyboardButton(text="NEIN - ABBRECHEN"),
    ]
])

kb_wg_bewohner = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Max"), KeyboardButton(text="Nawid")
    ],
    [
        KeyboardButton(text="Noah"), KeyboardButton(text="Seb")
    ]
])
