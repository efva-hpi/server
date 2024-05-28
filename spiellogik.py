from dataclasses import dataclass
import re
from time import time
import copy
from types import NoneType
from typing import Optional

class Spieler:
    def __init__(self, nickname: str, id: int) -> None:
        self.nickname: str = nickname
        self.id: int = id

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

@dataclass 
class Question:
    question: str
    answers: list[str]
    correct_answer: int

@dataclass
class Answer:
    player: Spieler
    answer: int
    time_stamp: int

class Game:
    def __init__(self, players: list[Spieler], id: int, game_settings: GameSettings) -> None:
        self.id: int = id
        self.player_list: list[Spieler] = players

        self.game_settings: GameSettings = game_settings

        self.questions: list[Question] = self.get_questions()
        self.current_question = 0
        #self.answers: list[dict[int, int]] = [{} for i in range(len(self.questions))]
        self.answers: list[list[Answer]] = [[] for i in range(len(self.questions))]

    def get_questions(self) -> list[Question]:
        # TODO: Implement
        time.sleep(0.2)
        return [Question("Wie spät?", ["Dumm1", "Dumm2", "Schlau", "Dumm3"], 2),
                Question("Noch ne Frage!", ["Antwort1", "Antwort2", "Antwort3", "Richtig"], 3),
                Question("???", ["Yes", "Nope1", "Nope2", "Nope3"], 0)]
    
    def all_answered(self) -> bool:
        """
        Checks whether all players have given an answer to the current question
        """
        answers = self.answers[self.current_question]
        for player in self.player_list:
            for a in answers:
                if player.id != a.player: return False
        return True

    def answer(self, player:Spieler, answer:int) -> bool:
        if (player in self.player_list):
            a: Answer = Answer(player, answer, time.time_ns())
            if not (a in self.answers[self.current_question]):
                self.answers[self.current_question].append(a)
                return True
        return False
    
    def next_question(self) -> bool:
        if self.all_answered(): 
            if self.current_question < len(self.questions)-1:
                self.current_question += 1
                return True
        return False

    def get_current_question(self) -> Question:
        return self.questions[self.current_question]
    



class Lobby:
    def __init__(self, id: int, code: str, game_settings: GameSettings = GameSettings()) -> None:
        self.id: int = id
        self._player_list: list[Spieler] = []

        self.game_settings: GameSettings = game_settings
        self.code = code

    def add_player(self, player: Spieler) -> bool:
        if not (player in self._player_list):   
            self._player_list.append(player)
            return True
        return False
    
    def remove_player(self, player: Spieler) -> bool:
        if (player in self._player_list):
            self._player_list.remove(player)
            return True
        return False
    
    def get_players(self) -> list[Spieler]:
        return self._player_list
    
    def get_player_list(self) -> list[str]:
        return [s.nickname for s in self._player_list]
    
    def get_player_ids(self) -> list[int]:
        return [s.id for s in self._player_list]
    
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
    
    def start_game(self) -> Game:
        """
        Starts a game and returns the game object
        """
        game: Game = Game(self._player_list, self.id, copy.deepcopy(self.game_settings))
        return game
    


class GameState:
    def __init__(self) -> None:
        self.id_counter = 0
        self.lobbies: list[Lobby] = []
        self.games: list[Game] = []
    
    def create_lobby(self, code: str, gameSettings: GameSettings) -> bool:
        for l in self.lobbies:
            if l.code == code: return False
        
        self.lobbies.append(Lobby(self.id_counter, code, gameSettings))
        self.id_counter += 1
        return True

    def get_code(self, id: int) -> Optional[str]:
        for l in self.lobbies:
            if (l.id == id): return l.code
        return None
    
    def get_id(self, code: str) -> Optional[int]:
        for l in self.lobbies:
            if (l.code == code): return l.id
        return None
    
    def get_lobby_by_id(self, id: int) -> Optional[Lobby]:
        for l in self.lobbies:
            if (l.id == id): return l
        return None

    def get_lobby_by_code(self, code: str) -> Optional[Lobby]:
        for l in self.lobbies:
            if (l.code == code): return l
        return None
        #raise Exception("Lobby not found")
    
    def start_game(self, id: int) -> bool:
        """
        Starts a game for a given lobby id
        """
        lobby = self.get_lobby_by_id(id)
        if lobby:
            self.games.append(lobby.start_game())
            return True
        else: return False
    
    def get_game_by_id(self, id: int) -> Optional[Game]:
        for g in self.games:
            if (g.id == id):
                return g
        return None
    
