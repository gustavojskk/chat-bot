# filebot.py
import os
import json
from difflib import get_close_matches
from unidecode import unidecode
import logging

class FileBot:
    def __init__(self, qa_pairs_file='qa_pairs.json'):
        self.qa_pairs_file = qa_pairs_file
        self.qa_pairs = self.load_qa_pairs()

    def preprocess_text(self, text):
        """Pré-processa o texto para facilitar a comparação."""
        return unidecode(text.lower())

    def load_qa_pairs(self):
        """Carrega pares de pergunta e resposta a partir de um arquivo."""
        try:
            if os.path.exists(self.qa_pairs_file):
                with open(self.qa_pairs_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return {}
        except Exception as e:
            logging.error(f"Erro ao carregar pares de pergunta e resposta: {str(e)}")
            return {}

    def save_qa_pairs(self):
        """Salva pares de pergunta e resposta em um arquivo."""
        try:
            with open(self.qa_pairs_file, 'w', encoding='utf-8') as file:
                json.dump(self.qa_pairs, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Erro ao salvar pares de pergunta e resposta: {str(e)}")

    def train_with_text(self, text):
        """Treina o FileBot com um texto contendo pares de pergunta e resposta."""
        try:
            qa_pairs = [line.strip().split(':') for line in text.split('\n') if ':' in line]
            for question, answer in qa_pairs:
                preprocessed_question = self.preprocess_text(question)
                if preprocessed_question in self.qa_pairs:
                    logging.warning(f"A pergunta '{preprocessed_question}' já foi treinada. Substituindo resposta.")
                self.qa_pairs[preprocessed_question] = answer
            self.save_qa_pairs()
        except Exception as e:
            logging.error(f"Erro durante o treinamento: {str(e)}")

    def find_most_similar_question(self, user_question):
        """Encontra a pergunta mais similar nas perguntas treinadas."""
        try:
            user_question_processed = self.preprocess_text(user_question)
            possible_questions = get_close_matches(user_question_processed, self.qa_pairs.keys(), n=1, cutoff=0.6)

            if possible_questions:
                return possible_questions[0]
            else:
                return None
        except Exception as e:
            logging.error(f"Erro ao encontrar pergunta mais similar: {str(e)}")
            return None

    def answer_question(self, user_question):
        """Gera uma resposta para a pergunta."""
        try:
            similar_question = self.find_most_similar_question(user_question)

            if similar_question is not None:
                return self.qa_pairs[similar_question]
            else:
                return "Desculpe, não sei a resposta para essa pergunta."
        except Exception as e:
            logging.error(f"Erro ao gerar resposta: {str(e)}")
            return "Desculpe, ocorreu um erro ao processar a pergunta."
