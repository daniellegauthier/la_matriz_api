from sklearn.pipeline import Pipeline
from app.semantic_core import NLTKPreprocessor, SemanticMapper, PhraseAnalyzer
from app.utils import generate_color_sequence, calculate_momentum

def initialize_pipeline():
    pipeline = Pipeline([
        ('preprocessor', NLTKPreprocessor()),
        ('semantic_mapper', SemanticMapper(filepath="data/semantic_rgb_mapping_with_sentiment.csv")),
        )),
    ])
    pipeline.fit(["init"])
    return pipeline

def process_phrase(pipeline, phrase, length=6, momentum='original'):
    tokens = pipeline.named_steps['preprocessor'].transform([phrase])[0]
    mapper = pipeline.named_steps['semantic_mapper']
    analyzer = PhraseAnalyzer(mapper.word_to_rgb_map, mapper.all_semantic_words)
    _, seed_words = analyzer.analyze(tokens)
    rgb_sequence = generate_color_sequence(seed_words, mapper.word_to_rgb_map, mapper.semantic_df, length)
    momentum_data = calculate_momentum(rgb_sequence)
    return {
        'seed_words': seed_words,
        'rgb_sequence': rgb_sequence,
        'momentum': momentum_data
    }
