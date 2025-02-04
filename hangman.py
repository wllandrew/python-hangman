import random
import os
import json
import time

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
		self.AlreadyTypedChar = []

		self.GameInit()

	def GameInit(self):
		while True:
			self.hangman.ShowState()
			self.ShowWord()
			ch = input("Letra: ")
			try:
				self.ChangeList(ch)
			except Exception as e:
				print(str(e))
				time.sleep(1)
			
			if self.HasWon(): 
				self.FinalMessage("Você ganhou!")
				break
			if self.HasLost():
				self.FinalMessage("Você perdeu.")
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
		return not "_ " in self.SpaceList

	def ShowWord(self) -> None:
		for n in range(0, len(self.hints)):
			print(f"Dica #{n + 1}: {self.hints[n]}")

		print("\nCaracteres já utilizados: " + ' '.join(self.AlreadyTypedChar))

		print("\n" + "".join(self.SpaceList).capitalize())

	def ChangeList(self, char : str) -> None:
		char = char.lower()

		if len(char) > 1:
			raise Exception("Argumento inválido")

		if char in self.AlreadyTypedChar:
			print("Esse caracter já foi utilizado!")
			time.sleep(1)
			return

		if (char not in self.Word) or ((not char.isalpha()) or (len(char) > 1)):
			self.hangman.ChangeState()
		else:
			for n in range(0, len(self.Word)):
				if self.Word[n].lower() == char:
					self.SpaceList[n] = f"{char} "

		self.AlreadyTypedChar.append(char)
			
class Settings:
	def __init__(self):
		self.wordSize = int(input("Tamanho da palavra: "))
		self.difficulty = input("Dificuldade ( facil/medio/dificil ): ")
		os.system("cls")

		with open("words.json", 'r') as file:
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

		if self.difficulty.lower() == "facil":
			return hints
		elif self.difficulty.lower() == "medio":
			return [hints[0]]
		elif self.difficulty.lower() == "dificil":
			return []

		raise Exception("Dificuldade inválida")

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
			
		except Exception as e:
			print(str(e))
			time.sleep(2)

if __name__ == "__main__":
	main()
