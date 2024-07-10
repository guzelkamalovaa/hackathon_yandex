import string
import random

EXCEPTION_TEXT = "Чтобы получить информацию о том, как работает навык, Вы можете сказать \"Помощь\".\
                    \nЕсли вы хотите узнать о моих возможностях, задайте вопрос \"Что ты умеешь?\""
INIT_TEXT = "ОПИСАНИЕ НАВЫКА. Если готовы начать, скажите \"Да\""
EMERGENCY_TEXT = "Хорошо, тогда я завершу работу навыка.\nОтдохните, и мы сможем пообщаться снова.\
\nЕсли чусвтвуете сильное недомогание - обратитесь к врачу:\
\nТелефон скорой медицинской помощи - 103."
TEXT_INTRODUCE_MELODY = "Хотите проверить свои музыкальные знания? Давайте сыграем в \"Угадай Мелодию\"!\n\
                         Вот какие у неё правила:\n Я проигрываю для Вас отрывок мелодии.\n\
                         У вас есть 3 попытки, чтобы угадать её название и исполнителя.\n\
                         Начнём с выбора музыкального периода:\n\
                         Назовите период от пятидесятых годов до восьмидесятых включительно."
HELP_MELODY = "Вот какие у неё правила:\n Я проигрываю для Вас отрывок мелодии.\n\
               У вас есть 3 попытки, чтобы угадать название и исполнителя каждой из них.\n\
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

SONG_DICT ={
    "80s":{
        "name": "восьмидесятые",
        "song_count": 3,
        "songs":[
            {
                "title": "а знаешь всё ещё будет",
                "performer": ["пугачева"],
                "url": "https://music.yandex.ru/album/3662718/track/30252300",
                "start": 133000
            },
            {
                "title": "команда молодости нашей",
                "performer": ["гурченко"],
                "url": "https://music.yandex.ru/album/26601340/track/19004854",
                "start": 150000
            },
            {
                "title": "этот мир",
                "performer": ["пугачева"],
                "url": "https://music.yandex.ru/album/3662723/track/30252391",
                "start": 87000
            },
            {
                "title": "ветер перемен",
                "performer": ["смеян", "воронина"],
                "url": "https://music.yandex.ru/album/91137/track/6098551",
                "start": 100000
            }
        ]
    },
    "70s":{
        "name": "семидесятые",
        "song_count": 3
    },
    "60s":{
        "name": "шестидесятые",
        "song_count": 1
    },
    "50s":{
        "name": "пятидесятые",
        "song_count": 1
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
        'win': "win"
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
                    'state07', 'win']:
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
    end_state = "false"
    
    if remove_punct(state).lower() == 'что ты умеешь' or remove_punct(state).lower() == 'что вы умеете' or button_state == 'code002':
        text = "Моя цель - помочь вам в преодолении одиночества"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state}
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
        text = "ФУНКЦИИ ПО ПУНКТАМ"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state}

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
    
    elif button_state == 'code000' \
        or (intent.get("YANDEX.CONFIRM") and saved_state.get("home", {}) == "true"):
        text = "Выберите игру:\n1. Угадай мелодию, или\n2. Угадай значение слова"
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

    elif button_state == 'code005' or\
        (saved_state.get("game_root", {}) == "melody"and saved_state.get("win", {}) == "true") or (saved_state.get("home", {}) == "false" and \
        (choice_number == "first" or remove_punct(state).lower() == 'угадай мелодию')) or \
        (saved_state.get("game_root", {}) == "melody" and saved_state.get("help", {}) == "melody"\
        and not saved_state.get("tries", {}) and not button_state == 'code000'):
        text = TEXT_INTRODUCE_MELODY
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': "melody"}
    elif saved_state.get("game_root", {}) == "melody" and intent.get("CUSTOM.ERA") or\
        (saved_state.get("help", {}) == "melody" and saved_state.get("tries", {}) == 3 \
        and not button_state == 'code000' and not saved_state.get("track", {})):
        if intent.get("CUSTOM.ERA"):
            state_5 = intent.get("CUSTOM.ERA", {}).get("slots", {}).get("number", {}).get("value", {})
            era = SONG_DICT.get(state_5)
            rand_song = random.randint(0, era.get("song_count"))
            text = "Хорошо, проигрываю песню из периода "+era.get("name")
            direct = {
                "audio_player": {
                    "action": "Play",
                    "item": {
                        "stream": {
                            "url": era.get("songs")[rand_song].get("url"),
                            "offset_ms": era.get("songs")[rand_song].get("start"),
                            "token": "token"
                        }
                    }
                }
            }
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
            'state03': "melody", 'state04': 3, 'state05': state_5,
            'state07': rand_song, 'direct': direct}
        elif saved_state.get("tries", {}):
            state_5 =saved_state.get("era", {})
            era = SONG_DICT.get(state_5)
            rand_song = saved_state.get("track", {})
            text = "Хорошо, проигрываю песню из периода "+era.get("name")
            direct = {
                "audio_player": {
                    "action": "Play",
                    "item": {
                        "stream": {
                            "url": era.get("songs")[rand_song].get("url"),
                            "offset_ms": era.get("songs")[rand_song].get("start"),
                            "token": "token"
                        }
                    }
                }
            }
            res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
            'state03': "melody", 'state04': saved_state.get("tries", {}), 'direct': direct,
            'state05':saved_state.get("era", {}), 'state07': saved_state.get("track", {})}

    elif button_state == 'code006' or (saved_state.get("game_root", {}) == "word" and saved_state.get("win", {}) == "true") or (saved_state.get("home", {}) == "false" and (choice_number == "second" or remove_punct(state).lower() == 'угадай значение слова')) or (saved_state.get("game_root", {}) == "word" and saved_state.get("help", {}) == "word" и not button_state == 'code000'):
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

    elif saved_state.get("game_root", {}) == "word" and saved_state.get("state05", {}):
        category = saved_state.get("state05", {})
        text = self.guess_the_word.check_answer(remove_punct(state).lower())
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': "word", 'state04': self.guess_the_word.attempts, 'state05': category}

    elif saved_state.get("game_root", {}) == "word":
        text = "Не понимаю что Вы имеете в виду, давайте вернёмся к нашему последнему взаимодействию.\n\
        Скажите любую фразу и я верну Вас обратно в игру"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': saved_state.get("game_root", {}), 'state04': saved_state.get("state04", {}),
        'state05': saved_state.get("state05", {}), 'state06': "word"}

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
