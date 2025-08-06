import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import csv
from pathlib import Path

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class NLTKPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [self.lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in self.stop_words]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self.preprocess(text) for text in X]


class SemanticMapper(BaseEstimator, TransformerMixin):
    def __init__(self, filepath):
        self.filepath = filepath
        self.semantic_colors = {}

    def fit(self, X=None, y=None):
        path = Path(self.filepath)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.filepath}")

        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                word = row['Original Words'].strip().lower()
                r, g, b = int(row['R']), int(row['G']), int(row['B'])
                self.semantic_colors[word] = [r, g, b]
        return self

    def transform(self, words):
        return [self.semantic_colors.get(word.lower(), [0, 0, 0]) for word in words]


class PhraseAnalyzer:
    def __init__(self, seed_words):
        self.seed_words = seed_words
        self.embedding = self._embed_words()

    def _embed_words(self):
        return np.random.rand(len(self.seed_words), 3)

    def analyze_momentum(self):
        diffs = np.diff(self.embedding, axis=0)
        magnitudes = np.linalg.norm(diffs, axis=1)
        directions = diffs / np.expand_dims(magnitudes + 1e-9, axis=1)
        return magnitudes.tolist(), directions.tolist()
