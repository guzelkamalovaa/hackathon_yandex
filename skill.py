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
        res = request_text.translate(str.maketrans('','', string.punctuation))
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
    # surname = ["попов"]
    # for item in event.get("request", {}).get("nlu", {}).get("entities", ["0"]):
    #     if item.get("type", {}) == "YANDEX.FIO":
    #         surname.append(item.get("value").get("last_name", ""))
    end_state = "false"
    
    #Obligatory functions
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

    #The melody guessing root:
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
                            # "offset_ms": 0,
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
    # elif saved_state.get("game_root", {}) == "melody" and ((saved_state.get("tries", {}) <= 3 \
    #     and saved_state.get("tries", {}) > 0) or (saved_state.get("help", {}) == "melody"\
    #     and saved_state.get("tries", {}) <= 2 and saved_state.get("tries", {}) > 0 and not button_state == 'code000')):
    #     right_names = SONG_DICT.get(saved_state.get("era", {})).get("songs", {})[saved_state.get("track", {})].get("performer", {})
    #     if len(surname)>1:
    #         for s in surname:
    #             if surname in right_names:
    #                 win = True
    #         if win:
    #             text = "Правильно! Вы настоящий музыкальный эксперт!\n Давайте скажем себе \"Ура\" и выберем новую песню!"
    #             res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
    #                     'state03': "melody", 'win': "true"}
    #         else:
    #             tries = saved_state.get("tries", {}) - 1
    #             text = "Не совсем верно. Попробуйте ещё раз! Количество попыток, которые у Вас ещё остались: " + str(tries)
    #             res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
    #                     'state03': "melody", 'state04': tries, 'direct': direct,
    #                     'state05':saved_state.get("era", {}), 'state07': saved_state.get("track", {})}

    #exception for melody
    elif saved_state.get("game_root", {}) == "melody":
        text = "Не понимаю что Вы имеете в виду, давайте вернёмся к нашему последнему взаимодействию.\n\
        Скажите любую фразу и я верну Вас обратно в игру"
        res = {'ver': event["version"], 'ses': event["session"], 't': text, 'end': end_state,
        'state03': saved_state.get("game_root", {}), 'state04': saved_state.get("tries", {}), 
        'state05': saved_state.get("era", {}), 'state06': "melody", 'state07': saved_state.get("track", {})}

    #First message of the skill
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