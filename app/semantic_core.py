import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
import random
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class NLTKPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        filtered = [self.lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in self.stop_words]
        return filtered

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self.preprocess(text) for text in X]

class SemanticMapper:
    def __init__(self, seed_words):
        self.seed_words = seed_words
        self.color_pool = self._generate_color_pool(len(seed_words))

    def _generate_color_pool(self, n):
        return [[random.randint(0, 255) for _ in range(3)] for _ in range(n)]

    def map_to_colors(self):
        return dict(zip(self.seed_words, self.color_pool))

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
