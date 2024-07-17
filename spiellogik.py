from dataclasses import dataclass
from random import randint
from time import time, sleep, time_ns
import copy
from typing import Optional
import requests
import json
import threading

def write_send_log(data):
    file = open("log_send.txt", "a")
    file.write(str(data) + "\n")
    file.close()

def write_answer_log(data):
    file = open("log_answer.txt", "a")
    file.write(str(data) + "\n")
    file.close()


class Player:
    def __init__(self, username: str) -> None:
        self.username: str = username
        self.score: int = 0


@dataclass
class GameSettings:
    """
    n_questions (max 50)
    category (id: int)
    difficulty (easy, medium, hard)
    game_type (multiple choice, true/false)
    """
    n_questions: int = 5
    category: int = 0
    difficulty: str = "easy"
    game_type: str = "multiple choice"
    max_time_question = 15  # in seconds


@dataclass
class Question:
    question: str
    category: int
    answers: list[str]
    correct_answer: int


@dataclass
class Answer:
    player: Player
    answer: int
    time_stamp: int
    timeout: bool


class Game:
    def __init__(self, players: list[Player], id: int, game_settings: GameSettings, on_next_question = None) -> None:
        self.id: int = id
        self.player_list: list[Player] = players

        self.game_settings: GameSettings = game_settings
        self.question_amount = game_settings.n_questions
        self.questions: list[Question] = self.get_questions(game_settings.n_questions)
        self.question_timestamps: list[Optional[int]] = [None for i in range(len(self.questions))]
        self.current_question = 0
        self.on_next_question = on_next_question

        self.answers: list[list[Answer]] = [[] for i in range(len(self.questions))]

        self.start_timer(0) # Start timer for first question
        

    def _calculate_points_time(self, question_time: Optional[int], answer_time: Optional[int],
                               correct_answer: bool) -> int:
        """
        Calculates the points using the answer and time to answer.
        """
        if not (question_time and answer_time): raise Exception("Time is none")
        if question_time > answer_time: raise Exception("Invalid time")

        time_taken_seconds = (answer_time - question_time) / 10e6  # time is measured in ns
        max_time = self.game_settings.max_time_question

        if time_taken_seconds > max_time: return 0  # answer was too late

        points: int = 0
        if correct_answer:
            points += 500  # a correct answer gives you 500 points

            if time_taken_seconds < 10:  # if you answered fast enough, you get more points
                points += round((1.0 - time_taken_seconds / max_time) * 400)  # you can get up to 400 more points

        return points
    
    def _check_question(self, question: Question, answer: Answer) -> bool:
        """
        Checks if an answer for a question is correct.
        """
        return answer in question.answers

    def _calculate_points_question_player(self, question_id: int, player: Player) -> int:
        """
        Calculates the points for a given player for a given question
        """
        if question_id >= len(self.questions): raise Exception("Invalid question")
        timestamp: Optional[int] = self.question_timestamps[question_id]
        if not timestamp: raise Exception("Invalid question time")

        answer: Optional[Answer] = self.get_answer_player(question_id, player)
        if not answer: raise Exception("Player has no answer for the question")
        if (answer.timeout): return 0

        question: Question = self.questions[question_id]
        return self._calculate_points_time(timestamp, answer.time_stamp, self._check_question(question, answer))

    # TODO: callback next question


    def stop_question(self, question: int):
        if (self.current_question == question):
            for p in self.player_list:
                if (self.get_answer_player(question, p) == None):
                    self.answer(p, -1, True)
            self.next_question()
    
    def start_timer(self, question: int):
        t = threading.Timer(30.0, self.stop_question, args=(question))

    def calculate_points_question(self, question: int) -> list[int]:
        """
        Returns the points for the nth question for all players.
        """
        points: list[int] = [self._calculate_points_question_player(question, p) for p in self.player_list]
        return points

    def _add_lists(self, a: list[int], b: list[int]) -> list[int]:
        if len(a) != len(b): raise Exception("Lists are not equal length")
        return [a[i] + b[i] for i in range(len(a))]

    def calculate_total_points(self) -> list[int]:
        """
        Returns the total points for all players and all currently answered questions
        """
        points: list[int] = [0 for p in self.player_list]
        for i in range(self.current_question + 1):
            points = self._add_lists(points, self.calculate_points_question(i))

        return points

    def get_answer_player(self, question_id: int, player: Player) -> Optional[Answer]:
        """
        Returns the answer object for a given player and question id.
        Can be none.
        """
        for a in self.answers[question_id]:
            if a.player == player:
                return a
        return None

    @staticmethod
    def get_questions(amount: int, difficulty: str = "", category: int = 0) -> list[Question]:
        """
        Fetches all questions from the question database.
        """
        url = "https://opentdb.com/api.php"
        params = {"amount": amount, "type": "multiple"}
        if difficulty != "":
            params.update({"difficulty": difficulty})
        if category != 0:
            params.update({"category": category})
        r = requests.get(url, params=params).json()
        if r["response_code"] != 0:
            if r["response_code"] != 5:
                raise Exception("Invalid response code")
            else:
                while r["response_code"] == 5:
                    sleep(2)
                    r = requests.get(url, params=params).json()
        questions = []
        for q in r["results"]:
            pos = randint(0, 3)
            answers = q["incorrect_answers"]
            answers.insert(pos, q["correct_answer"])
            questions.append(Question(q["question"], q["category"], answers, pos))
        return questions

    def all_answered(self) -> bool:
        """
        Checks whether all players have given an answer to the current question.
        Returns true if successful.
        """
        answers = self.answers[self.current_question]
        write_answer_log(answers)
        write_answer_log(self.player_list)
        for player in self.player_list:
            write_answer_log(f"Answer name {[a.player.username for a in answers]}, Player list {[p.username for p in self.player_list]}")
            if not (player.username in [a.player.username for a in answers]): return False
        return True

    def answer(self, player: Player, answer: int, timeout: bool = False) -> bool:
        """
        Submits an answer for a given player object.
        Returns true if successful.
        """
        print(f"Answer {player}, n: {answer}, timeout: {timeout}")
        #write_answer_log(f"Answer {player}, n: {answer}, timeout: {timeout}, player_list: {self.player_list}")
        if player.username in [p.username for p in self.player_list]:
            a: Answer = Answer(player, answer, time_ns(), timeout=timeout)
            #write_answer_log(a.player.username)
            #write_answer_log([a.player.username for a in self.answers[self.current_question]]   )
            if not (player.username in [a.player.username for a in self.answers[self.current_question]]):
                self.answers[self.current_question].append(a)
                #write_answer_log(f"Submitted answer {a}")
                print(f"Submitted answer {a}")
                return True
        return False

    def next_question(self) -> bool:
        """
        Switches to the next question, if all players submitted an answer.
        Returns true if successful.
        """
        if self.all_answered():
            if self.current_question < (len(self.questions) - 1):
                self.current_question += 1
                self.start_timer(self.current_question)
                self.on_next_question(self.questions[self.current_question], self.current_question)
                return True
        return False

    def get_current_question(self) -> Question:
        """
        Returns the current question object.
        """
        return self.questions[self.current_question]


class Lobby:
    def __init__(self, id: int, code: str, game_settings: GameSettings = GameSettings()) -> None:
        self.id: int = id
        self._player_list: list[Player] = []

        self.game_settings: GameSettings = game_settings
        self.code = code

    def add_player(self, player: Player) -> bool:
        """
        Adds an existing player to the lobby.
        Returns true if successful.
        """
        if not (player.username in self.get_player_list()):
            self._player_list.append(player)
            return True
        return False

    def remove_player(self, player: Player) -> bool:
        """
        Removes an player from the lobby.
        Returns true if successful.
        """
        if player in self._player_list:
            self._player_list.remove(player)
            return True
        return False

    def get_players(self) -> list[Player]:
        """
        Returns a list of all player objects.
        """
        return self._player_list

    def get_player_list(self) -> list[str]:
        """
        Returns a list of all usernames.
        """
        return [s.username for s in self._player_list]

    #    def create_invite_code(self) -> str:
    #        """
    #        Generates a 6-digit code using uppercase letters.
    #        """
    #        alph: list[str] = list(string.ascii_uppercase)
    #        number: int = self.id * 3789078567697854 + 456734568709089
    #
    #        code: str = ""
    #        for i in range(6):
    #            code += alph[number % len(alph)]
    #            number //= len(alph)
    #        return code

    def start_game(self, on_next_question) -> Game:
        """
        Starts a game and returns the game object
        """
        game: Game = Game(self._player_list, self.id, copy.deepcopy(self.game_settings), on_next_question=on_next_question)
        return game


class GameState:
    def __init__(self) -> None:
        self.id_counter = 0
        self.lobbies: list[Lobby] = []
        self.games: list[Game] = []
        self.players: list[Player] = []

    def check_nickname(self, nickname: str) -> bool:
        """
        Checks if a given nickname is already in use.
        """
        for p in self.players:
            if p.username == nickname: return True
        return False

    def create_player(self, nickname: str) -> bool:
        """
        Creates a new player
        """
        if self.check_nickname(nickname): return False
        self.players.append(Player(nickname))
        return True

    def create_lobby(self, code: str, gameSettings: GameSettings) -> bool:
        """
        Creates a new lobby with a lobby code and game settings.
        Returns true if successful.
        """
        for l in self.lobbies:
            if l.code == code:
                return False

        self.lobbies.append(Lobby(self.id_counter, code, gameSettings))
        self.id_counter += 1
        return True

    def get_code(self, id: int) -> Optional[str]:
        """
        Returns the lobby code for a given lobby id.
        Can be none!
        """
        for l in self.lobbies:
            if l.id == id: return l.code
        return None

    def get_id(self, code: str) -> Optional[int]:
        """
        Returns the id for a given lobby code.
        Can be none!
        """
        for l in self.lobbies:
            if l.code == code:
                return l.id
        return None

    def get_lobby_by_id(self, id: int) -> Optional[Lobby]:
        """
        Returns the lobby object for a given id.
        Can be none!
        """
        for l in self.lobbies:
            if l.id == id:
                return l
        return None

    def get_lobby_by_code(self, code: str) -> Optional[Lobby]:
        """
        Returns the lobby object for a given code.
        Can be none!
        """
        for l in self.lobbies:
            if l.code == code:
                return l
        return None

    def start_game(self, id: int, on_next_question) -> bool:
        """
        Starts a game for a given lobby id.
        Returns true if successful.
        """
        lobby = self.get_lobby_by_id(id)
        if lobby:
            self.games.append(lobby.start_game(on_next_question))
            return True
        else:
            return False
        
    def get_game_by_code(self, code: str) -> Optional[Game]:
        """
        Returns the game object for a code.
        Can be none.
        """
        id: Optional[int] = self.get_id(code)
        if id == None: return None
        for g in self.games:
            if g.id == id:
                return g
        return None

    def get_game_by_id(self, id: int) -> Optional[Game]:
        """
        Returns the game object for a given id (identical to the corresponding lobby id).
        Can be none.
        """
        for g in self.games:
            if g.id == id:
                return g
        return None
    
    def get_player_by_username(self, username: str) -> Optional[Player]:
        """
        Returns a player object for a given username
        """
        write_send_log("Ahhh: " + str(self.players))
        for p in self.players:
            
            if p.username == username:
                return p
        return None