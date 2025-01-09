import random
import os

'''
First, create the assets
1. list of words
2. hangman images (follow up: can a abstract them?)

Second, code the input
Third, code the game logic.
'''

# Problema: A logica de perder está errada.
# Implementação: Lista de letras já inseridas.

HangmanStates = [f"_______\n|     |\n|     0\n|    -|-\n|     A\n|    / {chr(92)}\n|\n",
				f"_______\n|     |\n|     0\n|    -|\n|     A\n|    / {chr(92)}\n|\n",
				f"_______\n|     |\n|     0\n|     |\n|     A\n|    / {chr(92)}\n|\n",
				f"_______\n|     |\n|     0\n|     |\n|     A\n|      {chr(92)}\n|\n",
				"_______\n|     |\n|     0\n|     |\n|     A\n|\n|\n",
				"_______\n|     |\n|     0\n|\n|\n|\n|\n",
				"_______\n|     |\n|\n|\n|\n|\n|\n"]

class Hangman:
	def __init__(self):
		self.initialState = HangmanStates[0]
		self.stateIndex = 0

	def ShowState(self) -> None:
		print(self.initialState)

	def CheckState(self) -> bool:
		if self.stateIndex == len(HangmanStates):
			return False
		return True

	def ChangeState(self) -> None:
		self.stateIndex += 1
		if self.CheckState:
			self.initialState = HangmanStates[self.stateIndex]

class Game:
	def __init__(self, word : chr):
		self.hangman = Hangman()
		self.Word = word.lower()
		self.SpaceList = ["_ "] * len(self.Word)

		while self.Endgame:
			self.hangman.ShowState()
			self.ShowWord()
			ch = input("Character: ")
			self.ChangeList(ch)
			if self.HasWon(): break
			os.system('cls')

		print("You have won!")

	def HasWon(self):
		if "_ " in self.SpaceList:
			return False
		return True

	def ShowWord(self) -> None:
		print("".join(self.SpaceList).capitalize())

	def Endgame(self) -> bool:
		return not self.hangman.CheckState()

	def ChangeList(self, char : str) -> None:
		char = char.lower()

		if (char not in self.Word) or ((not char.isalpha()) or (len(char) > 1)):
			self.hangman.ChangeState()
		else:
			for n in range(0, len(self.Word)):
				if self.Word[n].lower() == char:
					self.SpaceList[n] = f"{char} "
			
class Settings:
	def __init__(self):
		diff = int(input("Word size: "))
		os.system("cls")

		with open("words.txt", 'r') as wordsText:
			relation = {}
			for line in wordsText.read().split("\n"):
				if len(line) in relation:
					relation[len(line)].append(line)
				else:
					relation[len(line)] = [line]

		self.possibleWords = relation[diff]

	def ChooseWord(self) -> str:
		r = random.randint(0, len(self.possibleWords) - 1)
		return self.possibleWords[r]

def main():
	while True:
		os.system('cls')
		settings = Settings()
		game = Game(settings.ChooseWord())
		print("Ir novamente: ")
		inp = input("")
		if inp.lower() == 'n': break
		os.system("cls")

if __name__ == "__main__":
	main()