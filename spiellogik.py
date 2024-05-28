from dataclasses import dataclass
from time import time
import string
import copy

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
    question: str = "Hallo Welt?"
    answers: list[str] = ["1", "2", "3", "4"]
    correct_answer: int = 0

class Game:
    def __init__(self, players: list[Spieler], id: int, game_settings: GameSettings) -> None:
        self.id: int = id
        self.player_list: list[Spieler] = players

        self.game_settings: GameSettings = game_settings

        self.questions: list[Question] = self.get_questions()
        self.current_question = 0
        self.answers: list[dict[int, int]] = []


    def get_questions(self) -> list[Question]:
        # TODO: Implement
        time.sleep(0.2)
        return [Question("Wie spät?", ["Dumm1", "Dumm2", "Schlau", "Dumm3"], 2),
                Question("Noch ne Frage!", ["Antwort1", "Antwort2", "Antwort3", "Richtig"], 3),
                Question("???", ["Yes", "Nope1", "Nope2", "Nope3"], 0)]
    
    def answer(self, player:Spieler, answer:int):
        pass



class Lobby:
    def __init__(self, id: int, game_settings: GameSettings = GameSettings()) -> None:
        self.id: int = id
        self._player_list: list[Spieler] = []

        self.game_settings: GameSettings = game_settings

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
    
    def create_invite_code(self) -> str:
        """
        Generates a 6-digit code using uppercase letters.
        """
        alph: list[str] = list(string.ascii_uppercase)
        number: int = self.id * 3789078567697854 + 456734568709089
        
        code: str = ""
        for i in range(6):
            code += alph[number % len(alph)]
            number //= len(alph)
        return code
    
    def start_game(self) -> Game:
        """
        Starts a game and returns the game object
        """
        game: Game = Game(self._player_list, self.id, copy.deepcopy(self.game_settings))
        return game     