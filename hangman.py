import random
import os
import json
import time

'''
First, create the assets
1. list of words
2. hangman images (follow up: can a abstract them?)

Second, code the input
Third, code the game logic.
'''

# Implementação: Lista de letras já inseridas.

class Hangman:
	def __init__(self):
		self.HangmanStates = [f"_______\n|     |\n|     0\n|    -|-\n|     A\n|    / {chr(92)}\n|\n",
							f"_______\n|     |\n|     0\n|    -|\n|     A\n|    / {chr(92)}\n|\n",
							f"_______\n|     |\n|     0\n|     |\n|     A\n|    / {chr(92)}\n|\n",
							f"_______\n|     |\n|     0\n|     |\n|     A\n|      {chr(92)}\n|\n",
							"_______\n|     |\n|     0\n|     |\n|     A\n|\n|\n",
							"_______\n|     |\n|     0\n|\n|\n|\n|\n",
							"_______\n|     |\n|\n|\n|\n|\n|\n"]
		self.stateIndex = len(self.HangmanStates) - 1
		self.initialState = self.HangmanStates[self.stateIndex] 

	def ShowState(self) -> None:
		print(self.initialState)

	def CheckState(self) -> bool:
		return self.stateIndex == 0

	def ChangeState(self) -> None:
		if self.CheckState:
			self.stateIndex -= 1
			self.initialState = self.HangmanStates[self.stateIndex]

class Game:
	def __init__(self, word : chr, hints: list[str]):
		self.hangman = Hangman()
		self.Word = word.lower()
		self.SpaceList = ["_ "] * len(self.Word)
		self.hints = hints

		while True:
			self.hangman.ShowState()
			self.ShowWord()
			ch = input("Character: ")
			self.ChangeList(ch)
			if self.HasWon(): 
				self.FinalMessage("You have Won")
				break
			if self.HasLost():
				self.FinalMessage("You have Lost")
				break
			os.system('cls')

	def FinalMessage(self, message : str) -> None:
		os.system('cls')
		self.hangman.ShowState()
		self.ShowWord()

		print(f"\n{message}")
		time.sleep(3)
		os.system('cls')

	def HasLost(self):
		return self.hangman.CheckState()

	def HasWon(self):
		if "_ " in self.SpaceList:
			return False
		return True

	def ShowWord(self) -> None:
		for n in range(0, len(self.hints)):
			print(f"Dica #{n + 1}: {self.hints[n]}")
		print()
		print("".join(self.SpaceList).capitalize())

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
		self.wordSize = int(input("Word size: "))
		self.difficulty = input("Difficulty ( easy/medium/hard ): ")
		os.system("cls")

		with open("word.json", 'r') as file:
			self.jsonWords = json.load(file)
		self.JsonOnlyWords = self.jsonWords.keys() 

	def ChooseWordAndHint(self) -> str:
		relation = {}

		for word in self.jsonWords:
			if len(word) in relation:
				relation[len(word)].append(word)
			else:
				relation[len(word)] = [word]
		
		self.possibleWords = relation[self.wordSize]

		r = random.randint(0, len(self.possibleWords) - 1)
		chosenWord = self.possibleWords[r]
		return chosenWord, self.HintType(chosenWord)

	def HintType(self, word : str) -> list[str]:
		hints = self.jsonWords[word]

		if self.difficulty.lower() == "easy":
			return hints
		elif self.difficulty.lower() == "medium":
			return hints[0:1]
		return []

def main():
	while True:
		try: 
			os.system('cls')
			settings = Settings()
			word, hints = settings.ChooseWordAndHint()
			game = Game(word, hints)
			print("Ir novamente(s/n): ")
			inp = input("")
			if inp.lower() == 'n': break
			os.system("cls")
		except ValueError:
			print("Erro! Esse argumento não é um número.")
			time.sleep(2)

if __name__ == "__main__":
	main()