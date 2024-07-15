import string
import random
import re

EXCEPTION_TEXT = "Чтобы получить информацию о том, как работает навык, Вы можете сказать \"Помощь\".\
                    \nЕсли вы хотите узнать о моих возможностях, задайте вопрос \"Что ты умеешь?\""
INIT_TEXT = "Добро пожаловать в навык с играми-переходниками между поколениями!\n Я предлагаю Вам две игры, в которые можно играть как одному, так и в компании:\n\
            🎶 Знакомая нескольким поколениям игра \"Угадай мелодию\". Распознайте фрагмент классической музыкы и узнайте интересный факт о том, как она связана с современной культурой.\n \
            📚 \"Угадай значение слова\" - игра, расширяющая вашу лексику. В ней вы сможете обменятся знаниями о словах, которые шире использовались в прошлом и активно появляются в настоящем.\n\
            Если готовы начать, скажите \"Да\""
EMERGENCY_TEXT = "Хорошо, тогда я завершу работу навыка.\nОтдохните, и мы сможем пообщаться снова.\
                    \nЕсли чусвтвуете сильное недомогание - обратитесь к врачу:\
                    \nТелефон скорой медицинской помощи - 103."
TEXT_INTRODUCE_MELODY = "Хотите проверить свои музыкальные знания? Давайте сыграем в \"Угадай Мелодию\"!\n\
                         Вот какие у неё правила:\n Я проигрываю для Вас отрывок мелодии классической музыки.\n\
                         У вас есть 3 попытки, чтобы угадать её название и композитора.\n\
                         Начнём с выбора места происхождения композитора:\n\
                         🎹1. Русские композиторы.\n\
                         🎻2. Зарубежные композиторы."
HELP_MELODY = "Вот какие у неё правила:\n Я проигрываю для Вас отрывок мелодии классической мелодии.\n\
               У вас есть 3 попытки, чтобы угадать название и композитора каждой из них.\n\
               Если хотите продолжить с того же места - скажите \"Да\",\n\
               Или скажите \"Нет\" и мы вернёмся к выбору игр"
TEXT_INTRODUCE_GUESS_WORD = "Давайте сыграем в \"Угадай слово\"! \nВ этой игре мы предлагаем угадать значения слов, которые использует \
                            молодежь и люди старшего поколения. В каждом раунде будет 5 слов. Ваша цель - угадать их значения.\
                            \nКакие слова хотите угадывать?"
HELP_GUESS_WORD = ""  # TODO

class GuessTheWord:
    def __init__(self):
        self.words = {
            "старшее поколение": {
                "басче": "лучше",
                "кулема": "уменьшительно ласкательное прозвище",
                "губнушка": "губная помада",
                "гутарить": "болтать, беседовать",
                "умаяться": "устать",
                "дивиться": "поражаться чему-либо",
                "валандаться": "слишком медленно или долго делать что-либо",
                "ухайдокаться": "устать"
            },
            "молодежные": {
                "кринж": "чувство неловкости или стыда за чужие действия",
                "жиза": "жизненная ситуация, случай",
                "пруф": "доказательство"
            }
        }
        self.current_word = None
        self.attempts = 0
        self.max_attempts = 3
        self.round_words = []
        self.correct_answers = 0
        self.round_size = 5

    def start_game(self, category):
        if category not in self.words:
            return "Кажется, я вас не расслышала."
        self.round_words = random.sample(list(self.words[category].keys()), self.round_size)
        self.current_word = self.round_words.pop(0)
        self.attempts = 0
        self.correct_answers = 0
        return f"Вот первое слово: {self.current_word}. Что это значит?"

    def check_answer(self, answer):
        if self.current_word is None:
            return "Игра не начата. Выберите категорию и начните игру."
        
        correct_answer = self.words["старшее поколение" if self.current_word in self.words["старшее поколение"] else "молодежные"][self.current_word]
        if answer.lower() == correct_answer.lower():
            self.correct_answers += 1
            result = f"Правильно! {self.current_word} означает {correct_answer}."
        else:
            self.attempts += 1
            if self.attempts < self.max_attempts:
                return f"Не совсем верно. Попробуйте ещё раз! У вас осталось {self.max_attempts - self.attempts} попыток."
            else:
                result = f"К сожалению, вы не угадали. {self.current_word} означает {correct_answer}."

        if self.round_words:
            self.current_word = self.round_words.pop(0)
            self.attempts = 0
            return f"{result} Следующее слово: {self.current_word}. Что это значит?"
        else:
            self.current_word = None
            return f"{result} Вы отгадали {self.correct_answers}/{self.round_size} слов! Хотите сыграть ещё раз?"

class Skill:
    def __init__(self):
        self.guess_the_word = GuessTheWord()
        self.state = "INIT"
        self.category = None

    def handle_input(self, user_input):
        if self.state == "INIT":
            if user_input.lower() == "да":
                self.state = "CHOOSE_GAME"
                return "Выберите игру: Угадай значение слова или Угадай мелодию"
            else:
                return INIT_TEXT

        elif self.state == "CHOOSE_GAME":
            if "угадай значение слова" in user_input.lower():
                self.state = "CHOOSE_CATEGORY"
                return "Отлично! Давайте начнём. В этой игре мы предлагаем угадать значения слов которые использует молодежь и люди старшего поколения. Какие слова хотите угадывать? Молодежные, Слова моего поколения, Все вместе"
            elif "угадай мелодию" in user_input.lower():
                self.state = "MELODY_GAME"
                return TEXT_INTRODUCE_MELODY
            else:
                return "Пожалуйста, выберите 'Угадай значение слова' или 'Угадай мелодию'."

        elif self.state == "CHOOSE_CATEGORY":
            if "молодежные" in user_input.lower():
                self.category = "молодежные"
                self.state = "WORD_GAME"
                return self.guess_the_word.start_game(self.category)
            elif "слова моего поколения" in user_input.lower():
                self.category = "старшее поколение"
                self.state = "WORD_GAME"
                return self.guess_the_word.start_game(self.category)
            elif "все вместе" in user_input.lower():
                self.category = random.choice(["молодежные", "старшее поколение"])
                self.state = "WORD_GAME"
                return self.guess_the_word.start_game(self.category)
            else:
                return "Пожалуйста, выберите 'Молодежные', 'Слова моего поколения' или 'Все вместе'."

        elif self.state == "WORD_GAME":
            if "да" in user_input.lower():
                return self.guess_the_word.start_game(self.category)
            elif "нет" in user_input.lower():
                self.state = "INIT"
                return "Хорошо! Было приятно поиграть с вами! До новых встреч!"
            elif "сдаюсь" in user_input.lower():
                return self.guess_the_word.check_answer("сдаюсь")
            else:
                return self.guess_the_word.check_answer(user_input)

        elif self.state == "MELODY_GAME":
            return HELP_MELODY

        else:
            return EXCEPTION_TEXT


COMPOSER_DICT ={
    "rus_nineteenth":{
        "name": "русского классического композитора XIX века",
        "song_count": 1,
        "songs":[
            {
                "title": r"увертюр",
                "title_pretty": "\"Торжественная увертюра 1812 год\"",
                "performer": ["Пётр Ильич Чайковский", r"чайковск"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/20f0649b-cfbb-4a45-b6c0-b5084dd689e1.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Данная композиция используется в кульминационной сцене фильма 2005ого года \"V - значит Вендетта\".",
                    "Пётр Ильич Чайковский одним из первых использовал звук пушек, не являющихся музыкальным инструментом, в оркестровом произведении. \
                    \nТакой приём часто используется в авангардной музыке или в музыке для фильмов.\nЗвуки внутри мира фильма (их ещё называют диегетическими) \
                    становятся частью музыкальной композиции."
                ]
            },
            {
                "title": r"картин[а-я0-9ё\s]*выставк|избушк[а-я0-9ё\s]*курьих",
                "title_pretty": "\"Картинки с выставки\", часть \"Избушка на курьих ножках\"",
                "performer": ["Модест Петрович Мусоргский", r"модест|мусор[г]*ск"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/ebe3d4d4-48e6-4e69-adb7-8095adf2a30e.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Модест Мусоргский был частью известного кружка \"Могучая кучка\", который принёс в академическую музыку народные мотивы.\
                Развитие современного жанра фолк так же обязано общему продвижению народной музыки в область высокого искусства", 
                "Другое произведение из цикла \"Картинки с выставки\" - Гном, была использована в известном \
                фильме 1998ого года \"Большой Лебовски\", как часть музыкального сопровождения."]
            }
        ]
    },
    "rus_twentieth":{
        "name": "русского классического композитора начала XX века",
        "song_count": 1,
        "songs": [
            {
                "title":r"ромео и джульетт|танец рыцар|рыцарск[а-я]{2,3} тан[ец]{1}",
                "title_pretty": "балет \"Ромео и Джульетта\", \"Танец Рыцарей\"",
                "performer": ["Сергей Сергеевич Прокофьев", r"прокоф"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/1c4a83a3-196d-40da-8222-d237e13f4e6b.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Мелодия из данной композиции стала основой для песни \"Russians\" (1985 год) за автоством Стинга",
                "Мелодия из данного балета легла в основу песни \"Party Like a Russian\" (2016 год) за автоством Робби Уильямса"]
            },
            {  
                "title": r"пол[её]{1}т шмел|сказка о (царе)*салтан",
                "title_pretty": "\"Полёт шмеля\" из оперы \"Сказка о Царе Салтане\"",
                "performer": ["Николай Андреевич Римский-Корсаков", r"римск|корсаков"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/3f2faff3-7471-45c0-9f7e-e6da945e3674.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Этот эпизод оперы - пример звукоподражания в музыке. Полёт шмеля стал одним из основных звуковых эффектов\
                используемых в культуре для обозначения присутсвия в кадре летающих насекомых.",
                "Полёт шмеля - пример переноса звука природы в музыкальное произведение. Например, согласно легенде, Бетховен вдохновился \
                голосом птицы овсянки для создания Пятой Симфонии (мелодию птичьей песни можно услышать в начальном \"та да да дам\")\
                \nЭто приём, которым широко пользуются и сейчас."] 
            }          
        ]
    },
    "for_early":{
        "name": "раннего зарубежного композитора-классика",
        "song_count": 1,
        "songs": [
            {
                "title": r"скерцо|сюит|ре[-\w]минор|шутк|badinerie|scherzo",
                "title_pretty": "Скерцо(Штука) из \"Сюиты для флейты и струнного оркестра № 2\"",
                "performer": ["Иоганн Себастьян Бах", r"бах"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/6887a895-98c3-4c9d-a4cf-dcc41d31eeb3.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Под общим именем \"Скерцо\" существует много музыкальных произведений разных композиторов. \n\
                Это особый жанр барочной музыки, в котором ощущение от шутки и переливов смеха стараются передать \
                средствами музыкальной композиции. В современной музыке тоже сущетсвуют приёмы для отображения \
                определённых ситуаций и переживаний. Особенно это популярно в сопровождении для кино. Можно обартить внимание\
                на сходства в музыке, которая при просмотре вызывает у Вас схожие эмоции."]
            },
            {
                "title": r"врем[а-я]{1,5} года|зим|четыр[а-z]{1,3} сезона|antonio|quattro|inverno",
                "title_pretty": "Цикл концертов \"Времена года\": Зима",
                "performer": ["Антонио Вивальди", r"антон|в[еи]вальди|antonio|vivaldi"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/de7f50cc-f4e0-4b11-ac42-280c992cfebd.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Отчётливое барочное звучание \"Времён года\" сделало их символом жизни высшего света \
                в исторических фильмах. Часто в современном кино можно услышать композиции из \"Весны\" в сценах богемной жизни \
                не только восемнадцатого века."]
            }

        ]
        
    },
    "for_late":{
        "name": "позднего зарубежного композитора XIX - XX века",
        "song_count": 1,
        "songs": [
            {
                "title": r"лунн[а-я]{2,3} свет|clair de lune|сюит|suite",
                "title_pretty": "\"Лунный свет\" или Бергамасская сюита",
                "performer": ["Клод Дебюсси", r"клод|дебюсси|claude|debussy"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/cce260b1-0d3c-41a8-8eeb-8107c4321ed2.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Клод Дебюсси и другие французские импрессионисты стали вдохновением для музыкального сопровождения\
                популярной творческой игры Майнкрафт. Их отличает мягкое спокойное звучание и использование нестандартных аккордов.\
                \nИмпрессионисты как в изобразительном, так и в музыкальном искусстве старались передать впечатления, эмоции и ощущения.",
                "Импрессионисты, к которым относился Дебюсси, а так же Эрик Сати, стали вдохновением для музыкального жанра \"эмбиент\", (от английского слова, обозначающего \"обволакивающий\") \
                отличающегося спокойным, текучим звучанием с нестандартными интервалами, которые в классической академической музыке \
                считаются неблагозвучными, но используются композиторами сейчас для создания \"неземного\" звучания."]
            },
            {
                 "title": r"чард[аы]ш|c[sz]rdas",
                "title_pretty": "Чардаш",
                "performer": ["Витторио Монти", r"вик?[т]{1,2}орио|монти|vittorio|monti"],
                "audio_token": "<speaker audio='dialogs-upload/c03dc014-8e23-40d8-a04c-0e5ea7342b91/2bd0d497-333f-430a-994b-6d3ba6a0d4c2.opus'>",
                "hints_title": [],
                "hints_composer": [],
                "facts": ["Фрагмент, выбранный для викторины, используется в проигрыше песни Алехандро (2009 год) исполнительницы\
                 под псевдонимом Леди Гага.",
                 "Монти, как и \"Могучая кучка\" в Российской Империи, вывел народный венгерский танец в разряд академической музыки"]
            }
        ]
    }
}


def remove_punct(request_text) -> str:
    if request_text:
        res = request_text.translate(str.maketrans('', '', string.punctuation))
    else:
        res = ''
    return res.strip()

def response_builder(**d):
    key_translate = {
        'ver': "version",
        'ses': "session",
        't': "text",
        'tts': "tts",
        'end': "end_session",
        'direct': "directives",
        'b': "buttons",
        'c': "card_tf",
        'state01': "unwell_trigger",
        'state02': "home",
        'state03': "game_root",
        'state04': "tries",
        'state05': "era",
        'state07': "track",
        'state06': "help",
        'win': "win",
        'title': "first_guess"
    }
    JSON = {}
    response = {}
    session = {}
    for key in d:
        if key in ['ver', 'ses']:
            JSON.update({key_translate[key]: d[key]})
        if key in ['t', 'tts', 'end', 'direct', 'b', 'c']:
            response.update({key_translate[key]: d[key]})
        if key in ['state01', 'state02', 'state03', 
                    'state04','state05','state06', 
                    'state07', 'win', 'title']:
            session.update({key_translate[key]: d[key]})
    JSON.update({"response": response})
    JSON.update({"session_state": session})
    return JSON

def handler(event, context):
    state = event.get("request", {}).get("original_utterance", {})
    button_state = event.get("request", {}).get("payload", {}).get("text", {})
    dialogue_state = event.get("state", {}).get("session", {}).get("unwell_trigger", {})
    saved_state = event.get("state", {}).get("session", {})
    intent = event.get("request", {}).get("nlu", {}).get("intents", {})
    choice_number = intent.get("CUSTOM.MULTIPLE_CHOICE", {}).get("slots", {}).get("number", {}).get("value", {})
    classic_value = intent.get("CUSTOM.CLASSIC", {}).get("slots", {}).get("number", {}).get("value", {})
    surname = []
    for item in event.get("request", {}).get("nlu", {}).get("entities", [{"0": 0}]):
        if item.get("type", {}) == "YANDEX.FIO":
            surname.append(item.get("value", {}).get("last_name", ""))
    tries_pretty = ["одну попытку.", "две попытки.", "три попытки."]
    tokens = event.get("request", {}).get("nlu", {}).get("tokens", [])
    end_state = "false"

    
    #Obligatory functions
    if remove_punct(state).lower() == 'что ты умеешь' or remove_punct(state).lower() == 'что вы умеете' or button_state == 'code002':
        text = "Переходник поколений предлагает Вам весёлые игры, в которые можно играть людям \
        разных возрастов. Викторины 🎶\"Угадай мелодию\" и 📚\"Угадай значение слова\" позволяют вам \
        обменяться опытом и получить новые темы для обсуждения.\nУчиться новому - не страшно, а развлекательно!\n \
        Чтобы продолжить скажите: \"да\"."
        buttons = [
            {
                "title": "Да",
                "payload": {
                    "text": "code000"
                 },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'b': buttons, 'end': end_state, 'state02': "home"}
    elif intent.get("YANDEX.HELP") and saved_state.get("game_root", {}) == "melody":
        text = HELP_MELODY
        buttons = [
            {
                "title": "Да",
                "payload": {
                    "text": "code007"
                 },
                "hide": "true"
            },
            {
                "title": "Нет",
                "payload": {
                    "text": "code000"
                },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': saved_state.get("game_root", {}), 'state04': saved_state.get("tries", {}), 
        'state05': saved_state.get("era", {}), 'state06': "melody", 'state07': saved_state.get("track", {}),
        'b': buttons}
    elif (intent.get("YANDEX.HELP") or button_state == 'code001') \
        and not saved_state.get("game_root", {}) == "melody":
        text = "У этого навыка есть следующие функции:\n\
                🎶Игра \"Угадай мелодию\" - при выборе вариантов просто скажите эту фразу или скажите: \"перввый\"\n \
                📚Игра  \"Угадай значение слова\" - при выборе вариантов просто скажите эту фразу или скажите: \"второй\"\n \
                ❓Команда \"Что ты умеешь?\" - я расскажу Вам об основной идее этого навыка\n \
                🛏️Если почувствуете недомогание можете сказать \"Мне плохо\" или я могу попытаться определить это сама\n \
                Чтобы продолжить скажите: \"да\"."
        buttons = [
            {
                "title": "Да",
                "payload": {
                    "text": "code000"
                 },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'b': buttons, 'end': end_state, 'state02': "home"}

    #Checking user's state
    elif button_state == 'code003' or \
        (dialogue_state == "danger_possibility" and intent.get("YANDEX.CONFIRM")):
        text = EMERGENCY_TEXT
        end_state = "true"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state}
    elif button_state == 'code004' or \
        (dialogue_state == "danger_possibility" and intent.get("YANDEX.REJECT")):
        text = "Хорошо, тогда продолжаем общение. На чём мы остановились?"
        dialogue_state = {}
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state}
    elif intent.get("CUSTOM.UNWELL"):
        text = "Я обратила внимание, что вы можете не очень хорошо себя чувствовать.\
        \nЕсли это так, скажите \"Да\", если хотите продолжить общение - \"Нет\""
        buttons = [
            {
                "title": "Да",
                "payload": {
                    "text": "code003"
                 },
                "hide": "true"
            },
            {
                "title": "Нет",
                "payload": {
                    "text": "code004"
                },
                "hide": "true"
            }
        ]
        dialogue_state = "danger_possibility"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'b': buttons}
    
    #Home question for games
    elif button_state == 'code000' \
        or (intent.get("YANDEX.CONFIRM") and saved_state.get("home", {}) == "true") \
        or (saved_state.get("game_root", {}) == "melody" and saved_state.get("win", {}) \
         and (button_state == "109" or intent.get("YANDEX.REJECT"))):
        text = "Выберите игру:\n1. 🎶\"Угадай мелодию\" \n 2. 📚\"Угадай значение слова\""
        buttons = [
            {
                "title": "Угадай мелодию",
                "payload": {
                    "text": "code005"
                 },
                "hide": "true"
            },
            {
                "title": "Угадай значение слова",
                "payload": {
                    "text": "code006"
                },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'b': buttons, 'state02': "false"}

    #The word guessing root
    elif button_state == 'code006' or (saved_state.get("game_root", {}) == "word" and saved_state.get("win", {}) == "true") or (saved_state.get("home", {}) == "false" and (choice_number == "second" or remove_punct(state).lower() == 'угадай значение слова')) or (saved_state.get("game_root", {}) == "word" and saved_state.get("help", {}) == "word" and not button_state == 'code000'):
        text = TEXT_INTRODUCE_GUESS_WORD
        buttons = [
            {
                "title": "Молодежные",
                "payload": {
                    "text": "code008"
                 },
                "hide": "true"
            },
            {
                "title": "Слова моего поколения",
                "payload": {
                    "text": "code009"
                },
                "hide": "true"
            },
            {
                "title": "Все вместе",
                "payload": {
                    "text": "code010"
                },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': "word", 'b': buttons}
    elif saved_state.get("game_root", {}) == "word" and (button_state == 'code008' or button_state == 'code009' or button_state == 'code010'):
        if button_state == 'code008':
            category = "молодежные"
        elif button_state == 'code009':
            category = "старшее поколение"
        elif button_state == 'code010':
            category = random.choice(["молодежные", "старшее поколение"])
        
        text = self.guess_the_word.start_game(category)
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': "word", 'state04': self.guess_the_word.attempts, 'state05': category}

    elif saved_state.get("game_root", {}) == "word" and saved_state.get("era", {}):
        category = saved_state.get("era", {})
        text = self.guess_the_word.check_answer(remove_punct(state).lower())
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': "word", 'state04': self.guess_the_word.attempts, 'state05': category}

    elif saved_state.get("game_root", {}) == "word":
        text = "Не понимаю что Вы имеете в виду, давайте вернёмся к нашему последнему взаимодействию.\n\
        Скажите любую фразу и я верну Вас обратно в игру"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': saved_state.get("game_root", {}), 'state04': saved_state.get("tries", {}),
        'state05': saved_state.get("era", {}), 'state06': "word"}

    #The melody guessing root:
    elif button_state == 'code005' or (saved_state.get("home", {}) == "false" and \
        (choice_number == "first" or remove_punct(state).lower() == 'угадай мелодию')) or \
        ((saved_state.get("game_root", {}) == "melody" or saved_state.get("game_root", {}) == "melody_composer") and saved_state.get("help", {}) == "melody"\
        and not saved_state.get("tries", {}) and not button_state == 'code000') or \
        (saved_state.get("game_root", {}) == "melody" and saved_state.get("win", {}) \
         and (button_state == "108" or intent.get("YANDEX.CONFIRM"))):
        text = TEXT_INTRODUCE_MELODY
        buttons = [
                    {
                        "title": "🎹Русские композиторы",
                        "payload": {
                        "text": "code109"
                        },
                        "hide": "true"
                    },
                    {
                        "title": "🎻Зарубежные композиторы",
                        "payload": {
                        "text": "code110"
                        },
                        "hide": "true"
                    }
                ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'b': buttons, 'end': end_state,
                'state03': "melody_composer"}
    elif saved_state.get("game_root", {}) == "melody_composer" and (button_state or (intent.get("CUSTOM.CLASSIC", {}) and classic_value in ['rus', 'for']) \
        or (choice_number and choice_number != 'third') or saved_state.get("era", {})):
        composer = intent.get("CUSTOM.CLASSIC", {}).get("slots", {}).get("number", {}).get("value", {}) 
        era = saved_state.get("era", {})
        if button_state == "code109" or choice_number == "first" or composer == 'rus' or era == 'rus':
            text = "А теперь выберите временной период для композитора:\n 🎩 1. XIX век\n ✍2. Начало XX века"
            tts = "А теперь выберите временной период для композитора: Первое XIX век. Второе: начало XX века"
            buttons = [
                {
                        "title": "🎩XIX век",
                        "payload": {
                        "text": "code111"
                        },
                        "hide": "true"
                    },
                    {
                        "title": "✍нач. XX в.",
                        "payload": {
                        "text": "code112"
                        },
                        "hide": "true"
                    }
            ]
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'b': buttons, 'tts': tts, 'end': end_state,
                    'state03': "melody", 'state05': composer}
        if button_state == "code110" or choice_number == "second" or composer == 'for' or era == 'for':
            text = "А теперь выберите временной период для композитора:\n📜1. Ранние композиторы (XVIII в.)\n 🖋️2. Поздние композиторы (XIX - нач. XX вв.)"
            tts = "А теперь выберите временной период для композитора: Первое: Ранние композиторы (восемнадцатый век). Второе:  Поздние композиторы (девятнадцатый - начало двадцатого  в+ека)."
            buttons = [
                {
                        "title": "📜Ранние (XVIII в.)",
                        "payload": {
                        "text": "code111"
                        },
                        "hide": "true"
                    },
                    {
                        "title": "🖋️Поздние(XIX - нач. XX вв.)",
                        "payload": {
                        "text": "code112"
                        },
                        "hide": "true"
                    }
            ]
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'b': buttons, 'tts': tts, 'end': end_state,
                    'state03': "melody", 'state05': composer}
    elif saved_state.get("game_root", {}) == "melody" and (((intent.get("CUSTOM.CLASSIC", {}) and classic_value not in ['rus', 'for'])\
        and not saved_state.get("track", {})) or (button_state in ['code112', 'code111']) or (choice_number and choice_number != 'third') or (saved_state.get("help", {}) == "melody"\
        and saved_state.get("tries", {}) > 0  and not button_state == 'code000')):
        if saved_state.get("era", {}) == 'rus' and (classic_value in ['twentieth', 'nineteenth'] \
            or button_state or choice_number):
            dict_states = {
                "code111": "nineteenth",
                "code112": "twentieth",
                "first": "nineteenth",
                "second": "twentieth"
            }
            pre_era = saved_state.get("era", {})
            if intent.get("CUSTOM.CLASSIC", {}):
                state_5 = pre_era + '_' + classic_value
            elif button_state:
                state_5 = pre_era + '_' + dict_states[button_state]
            elif choice_number:
                state_5 = pre_era + '_' + dict_states[choice_number]
            era = COMPOSER_DICT.get(state_5, {})
            rand_song = random.randint(0, len(era.get("songs")) - 1)
            text = "Проигрываю фрагмент произведения " + era.get("name") + ".\n Назовите, пожалуйста, сначала имя композитора!"
            tts = "Проигрываю фрагмент произведения " + era.get("name") + " " +  era.get("songs", [])[rand_song].get("audio_token", {}) + " . Назовите, пожалуйста, сначала имя композитора!"
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'tts':tts, 'end': end_state,
            'state03': "melody", 'state04': 3, 'state05': state_5, 'state07': rand_song}
        elif saved_state.get("era", {}) == 'for' and (intent.get("CUSTOM.CLASSIC", {}) \
            or button_state or choice_number):
            dict_states = {
                "code111": "early",
                "code112": "late",
                "first": "early",
                "second": "late"
            }
            pre_era = saved_state.get("era", {})
            if classic_value in ['late', 'early']:
                state_5 = pre_era + '_' + classic_value
            elif classic_value in ['twentieth', 'nineteenth']:
                state_5 = pre_era + '_late'
            elif button_state:
                state_5 = pre_era + '_' + dict_states[button_state]
            elif choice_number:
                state_5 = pre_era + '_' + dict_states[choice_number]
            era = COMPOSER_DICT.get(state_5, {})
            rand_song = random.randint(0, len(era.get("songs")) - 1)
            text = "Проигрываю фрагмент произведения " + era.get("name") + ".\n Назовите, пожалуйста, сначала имя композитора!"
            tts = "Проигрываю фрагмент произведения " + era.get("name") + " " +  era.get("songs", [])[rand_song].get("audio_token", {}) + " . Назовите, пожалуйста, сначала имя композитора!"
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'tts':tts, 'end': end_state,
            'state03': "melody", 'state04': 3, 'state05': state_5, 'state07': rand_song}
        elif saved_state.get("help", {}) == "melody":
            state_5 =saved_state.get("era", {})
            era = COMPOSER_DICT.get(state_5)
            rand_song = saved_state.get("track", {})
            text = "Проигрываю фрагмент произведения " + era.get("name") + ".\n Назовите, пожалуйста, сначала имя композитора!"
            tts = "Проигрываю фрагмент произведения " + era.get("name") + " " +  era.get("songs", [])[rand_song].get("audio_token", {}) + " . Назовите, пожалуйста, сначала имя композитора!"
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'tts':tts, 'end': end_state,
            'state03': "melody", 'state04': 3, 'state05': state_5, 'state07': rand_song}
        # else:
        #     text = "Кажется, выбор прошёл не совсем верно.\n Скажите что-нибудь, и мы вернёмся на предыдущий шаг."
        #     res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        #     'state03': "melody_composer", 'state05':saved_state.get("era", {}), 'state07': saved_state.get("track", {})}
    elif saved_state.get("game_root", {}) == "melody" and saved_state.get("track", -1) >= 0 \
        and saved_state.get("tries", -1) > 0:
        song_num = saved_state.get("track", {})
        state_5 = saved_state.get("era", {})
        fact = random.choice(COMPOSER_DICT.get(state_5, {}).get("songs", {})[song_num].get("facts", {}))
        right_names = COMPOSER_DICT.get(state_5, {}).get("songs", {})[song_num].get("performer", {})[1]
        right_name = COMPOSER_DICT.get(state_5, {}).get("songs", {})[song_num].get("performer", {})[0]
        right_title = COMPOSER_DICT.get(state_5, {}).get("songs", {})[song_num].get("title", {})
        title_to_show = COMPOSER_DICT.get(state_5, {}).get("songs", {})[song_num].get("title_pretty", {})
        if saved_state.get("first_guess", {}) == "true":
            win = re.search(right_title, remove_punct(state).lower())
            if win:
                text = "Абсолютно верно! Это произведение " + title_to_show + ", его композитор: " + right_name + "\nИнтересный факт: " + fact + "\n" +  "\n Если хотите угадать ещё одну композицию, скажите \"Да\", если хотите выйти из игры - \"Нет\""
                buttons = [
                    {
                        "title": "Да",
                        "payload": {
                        "text": "code108"
                        },
                        "hide": "true"
                    },
                    {
                        "title": "Нет",
                        "payload": {
                        "text": "code109"
                        },
                        "hide": "true"
                    }
                ]
                res = {'ver': event["version"], 'ses': event["session"], 't': text, 'b':buttons, 'end': end_state,
                        'state03': "melody", 'win': "true"}                
            elif saved_state.get("tries", -1) == 1 and not win:
                text_start = ["Не расстраивайтесь! Бывает, что классики не сразу поддаются угадыванию.\n  Это была композиция ", "Спасибо за участие!  Это произведение ", "Музыка - вещь загадочная! \n Эта мелодия оказалась для Вас непростой. \nЭто было произведение "]
                text_end = ["Хотите сыграть ещё?", "Хотите попробовать угадать другую мелодию?", "Хотите попробовать угадать ещё одну?"]
                text = "К сожалению, у Вас закончились попытки.\n" + random.choice(text_start) + title_to_show + "\nКомпозитор: " + right_name + "\nИнтересный факт: " + fact + "\n" + random.choice(text_end) 
                buttons = [
                    {
                        "title": "Да",
                        "payload": {
                        "text": "code108"
                        },
                        "hide": "true"
                    },
                    {
                        "title": "Нет",
                        "payload": {
                        "text": "code109"
                        },
                        "hide": "true"
                    }

                ]
                res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
                    'state03': "melody", 'state05':saved_state.get("era", {}),
                    'state07': saved_state.get("track", {}), 'b': buttons, 'win': "fail"}
            else:
                tries = saved_state.get("tries", {}) - 1
                text = "Не совсем верное название произведения. Попробуйте ещё раз! Вы можете потратить ещё " + tries_pretty[saved_state.get("tries", {}) - 2]
                tts = "Не совсем верное название произведения. Попробуйте ещё раз! Вы можете потратить ещё " + tries_pretty[saved_state.get("tries", {}) - 2] + " " + COMPOSER_DICT.get(state_5, {}).get("songs", [])[song_num].get("audio_token", {})
                res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
                        'state03': "melody", 'state04': tries, 'state05':saved_state.get("era", {}), 
                        'state07': saved_state.get("track", {}), 'title': "true", 'tts': tts}
        elif saved_state.get("first_guess", {}) != "true":
            if re.search(right_names, remove_punct(state).lower()):
                text = "Правильно! Эту мелодию написал композитор " + right_name + "!\n А теперь назовите, пожалуйста, саму композицию."
                tts = "Правильно! Эту мелодию написал композитор " + right_name + "! А теперь назовите, пожалуйста, саму композицию." + " " + COMPOSER_DICT.get(state_5, {}).get("songs", [])[song_num].get("audio_token", {})
                res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
                        'state03': "melody", 'state04': 3, 'state05':saved_state.get("era", {}), 
                        'state07': saved_state.get("track", {}), 'title': "true", 'tts':tts}
            elif saved_state.get("tries", -1) == 1 and not re.search(right_names, remove_punct(state).lower()):
                right_name = COMPOSER_DICT.get(state_5, {}).get("songs", {})[song_num].get("performer", [])[0]
                text_start = ["Не расстраивайтесь! Бывает, что классики не сразу поддаются угадыванию.\n  Это была композиция ", "Спасибо за участие!  Это произведение ", "Музыка - вещь загадочная! \n Эта мелодия оказалась для Вас непростой. \nЭто было произведение "]
                text_end = ["Хотите сыграть ещё?", "Хотите попробовать угадать другую мелодию?", "Хотите попробовать угадать ещё одну?"]
                text = "К сожалению, у Вас закончились попытки.\n" + random.choice(text_start) + title_to_show + "\nКомпозитор: " + right_name + "\nИнтересный факт: " + fact + "\n" + random.choice(text_end) 
                buttons = [
                    {
                        "title": "Да",
                        "payload": {
                        "text": "code108"
                        },
                        "hide": "true"
                    },
                    {
                        "title": "Нет",
                        "payload": {
                        "text": "code109"
                        },
                        "hide": "true"
                    }

                ]
                res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
                    'state03': "melody", 'state05':saved_state.get("era", {}), 
                    'state07': saved_state.get("track", {}), 'b': buttons, 'win': "fail"}
            else:
                tries = saved_state.get("tries", {}) - 1
                text = "Не совсем верное имя композитора. Попробуйте ещё раз! Вы можете использовать ещё " + tries_pretty[saved_state.get("tries", {}) - 2]
                tts = "Не совсем верное имя композитора. Попробуйте ещё раз! Вы можете потратить ещё " + tries_pretty[saved_state.get("tries", {}) - 2] + " " +  COMPOSER_DICT.get(state_5, {}).get("songs", [])[song_num].get("audio_token", {})
                res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
                        'state03': "melody", 'state04': tries, 'state05':saved_state.get("era", {}),
                        'state07': saved_state.get("track", {}), 'tts': tts}
    
    # exception for melody
    elif saved_state.get("game_root", {}) == "melody" or saved_state.get("game_root", {}) == "melody_composer":
        text = "Не понимаю что Вы имеете в виду, давайте вернёмся к нашему последнему взаимодействию.\n\
        Скажите любую фразу и я верну Вас обратно в игру"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': saved_state.get("game_root", {}), 'state04': saved_state.get("tries", {}), 
        'state05': saved_state.get("era", {}), 'state06': "melody", 'state07': saved_state.get("track", {})}
    
    elif len(state) == 0:
        text = INIT_TEXT
        buttons = [
            {
                 "title": "Да",
                "payload": {
                    "text": "code000"
                 },
                "hide": "true"
            },
            {
                "title": "Помощь",
                "payload": {
                    "text": "code001"
                 },
                "hide": "true"
            },
            {
                "title": "Что ты умеешь?",
                "payload": {
                    "text": "code002"
                },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'b': buttons, 'state02': "true"}
    else:
        text = EXCEPTION_TEXT
        buttons = [
            {
                "title": "Помощь",
                "payload": {
                    "text": "code001"
                 },
                "hide": "true"
            },
            {
                "title": "Что ты умеешь?",
                "payload": {
                    "text": "code002"
                },
                "hide": "true"
            }
        ]
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'b': buttons}
    res.update({'state01': dialogue_state})
    return response_builder(**res)
