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
        KeyboardButton(text="Max"), KeyboardButton(text="x")
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
        KeyboardButton(text="Max"), KeyboardButton(text="x")
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


def create_bahn_searchresult_keyboard(search_results):
    kbs = []
    for x in search_results.keys():
        kbs = kbs + [KeyboardButton(text=x)]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [x] for x in kbs
    ])
    return keyboard


kb_bahn_favoriten_bearbeiten = ReplyKeyboardMarkup(keyboard=[
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


kb_canteen_favoriten_bearbeiten = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Favorit 1")
        ],
        [
            KeyboardButton(text="Favorit 2")
        ],
        [
            KeyboardButton(text="Abbrechen")
        ]
    ])


def create_canteen_start_keyboard(self):
    try:
        fav1 = list(self.cookies['mensa']['fav1'].keys())[0]
    except (KeyError, IndexError):
        fav1 = "Favorit 1"
    try:
        fav2 = list(self.cookies['mensa']['fav2'].keys())[0]
    except (KeyError, IndexError):
        fav2 = "Favorit 2"

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=fav1)
        ],
        [
            KeyboardButton(text=fav2)
        ],
        [
            KeyboardButton(text="Suche"), KeyboardButton(text="Favoriten bearbeiten")
        ]
    ])
    return keyboard


def create_canteen_searchresult_keyboard(search_results):
    kbs = []
    for x in search_results.keys():
        kbs = kbs + [KeyboardButton(text=x)]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [x] for x in kbs
    ])
    return keyboard


def create_weather_start_keyboard(self):
    try:
        fav1 = list(self.cookies['wetter']['fav1'].keys())[0]
    except (KeyError, IndexError):
        fav1 = "Favorit 1"
    try:
        fav2 = list(self.cookies['wetter']['fav2'].keys())[0]
    except (KeyError, IndexError):
        fav2 = "Favorit 2"

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=fav1)
        ],
        [
            KeyboardButton(text=fav2)
        ],
        [
            KeyboardButton(text="Suche"), KeyboardButton(text="Favoriten bearbeiten")
        ]
    ])
    return keyboard


def create_weather_searchresult_keyboard(search_results):
    kbs = []
    for x in search_results.keys():
        kbs = kbs + [KeyboardButton(text=x)]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [x] for x in kbs
    ])
    return keyboard


kb_wetter_favoriten_bearbeiten = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Favorit 1")
        ],
        [
            KeyboardButton(text="Favorit 2")
        ],
        [
            KeyboardButton(text="Abbrechen")
        ]
    ])


def create_eingekauft_keyboard(items_available):
    kbs = ["Alle"]
    for x in items_available:
        kbs = kbs + [KeyboardButton(text=x)]
    kbs = kbs + [KeyboardButton(text="Abbrechen")]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [x] for x in kbs
    ])
    return keyboard


kb_muell_due = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Ich mach das', callback_data='garbage_take_responsibility')
    ],
    [
        InlineKeyboardButton(text='Ist schon draußen', callback_data='garbage_already_done'),
        InlineKeyboardButton(text='Muss nicht raus', callback_data='garbage_not_full')
    ]
])
