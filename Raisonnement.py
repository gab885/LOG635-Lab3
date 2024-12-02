from aima.logic import *
import nltk

class Crime:

    def __init__(self):
        self.weapons = ["Corde", "Fusil", "Couteau", "Beignet empoisonné", "Saxophone","Tige de Plutonium" ]
        self.rooms = ["Cuisine", "Bureau", "Garage", "Salon", "Bibliothèque", "Observatoire"]
        self.persons = ["Mustard", "Peacock", "Scarlet", "Plum", "White", "Green"]
        
        self.clauses = []        
        
        self.initialize_clauses()
        self.initialize_KB()
        self.inference_rules()
        
        self.crime_kb = FolKB(self.clauses)

    def initialize_clauses(self):
        self.initialize_basic_facts()
        self.initialize_constraints()

    def initialize_basic_facts(self):
        """
        Déclare les faits de base sur les armes, pièces et personnes.
        """
        for weapon in self.weapons:
            self.clauses.append(expr(f"Arme({weapon})"))

        for room in self.rooms:
            self.clauses.append(expr(f"Piece({room})"))

        for person in self.persons:
            self.clauses.append(expr(f"Personne({person})"))

    def initialize_constraints(self):
        """
        Déclare des règles pour gérer les contraintes logiques :
        - Les armes, pièces et personnes sont uniques.
        """
        # Les pièces sont toutes différentes
        for i in range(len(self.rooms)):
            for j in range(i + 1, len(self.rooms)):
                self.clauses.append(expr(f"PieceDifferente({self.rooms[i]}, {self.rooms[j]})"))

        # Les armes sont toutes différentes
        for i in range(len(self.weapons)):
            for j in range(i + 1, len(self.weapons)):
                self.clauses.append(expr(f"ArmeDifferente({self.weapons[i]}, {self.weapons[j]})"))


    def add_fact(self, fact):
        """
        Ajoute un nouveau fait à la base de connaissances.
        """
        self.crime_kb.tell(expr(fact))


    def inference_rules(self):
        """
        Trpuver les règles d'inference
        """


