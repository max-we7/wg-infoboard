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


def create_bahn_start_keyboard(self):
    try:
        fav1 = list(self.cookies['bahn']['fav1'].keys())[0]
    except (KeyError, IndexError):
        fav1 = "Favorit 1"
    try:
        fav2 = list(self.cookies['bahn']['fav2'].keys())[0]
    except (KeyError, IndexError):
        fav2 = "Favorit 2"
    try:
        fav3 = list(self.cookies['bahn']['fav3'].keys())[0]
    except (KeyError, IndexError):
        fav3 = "Favorit 3"
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=fav1)
        ],
        [
            KeyboardButton(text=fav2)
        ],
        [
            KeyboardButton(text=fav3)
        ],
        [
            KeyboardButton(text="Suche"), KeyboardButton(text="Favoriten bearbeiten")
        ]
    ])
    return keyboard


def create_bahn_destination_keyboard(self):
    try:
        fav1 = list(self.cookies['bahn']['fav1'].keys())[0]
    except (KeyError, IndexError):
        fav1 = "Favorit 1"
    try:
        fav2 = list(self.cookies['bahn']['fav2'].keys())[0]
    except (KeyError, IndexError):
        fav2 = "Favorit 2"
    try:
        fav3 = list(self.cookies['bahn']['fav3'].keys())[0]
    except (KeyError, IndexError):
        fav3 = "Favorit 3"
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=fav1)
        ],
        [
            KeyboardButton(text=fav2)
        ],
        [
            KeyboardButton(text=fav3)
        ],
        [
            KeyboardButton(text="Suche")
        ]
    ])
    return keyboard


def create_bahn_searchresult_keyboard(self, search_results):
    kbs = []
    for x in search_results.keys():
        kbs = kbs + [KeyboardButton(text=x)]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [x] for x in kbs
    ])
    return keyboard


kb_favoriten_bearbeiten = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Favorit 1")
        ],
        [
            KeyboardButton(text="Favorit 2")
        ],
        [
            KeyboardButton(text="Favorit 3")
        ],
        [
            KeyboardButton(text="Abbrechen")
        ]
    ])
