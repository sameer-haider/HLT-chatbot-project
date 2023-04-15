from typing import Dict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy

NER = spacy.load("en_core_web_md")
threshold = 0.3


def best_match(message, patterns) -> str:
    # Tokenize, lemmatize and remove stopwords from the user input and patterns
    wordnet_lemmatizer = WordNetLemmatizer()
    user_input_tokens = [
        wordnet_lemmatizer.lemmatize(word.lower())
        for word in word_tokenize(message)
        if word.isalnum()
    ]
    pattern_tokens = [
        [
            wordnet_lemmatizer.lemmatize(word.lower())
            for word in word_tokenize(pattern)
            if word.isalnum()
        ]
        for pattern in patterns
    ]

    # Calculate the TF-vectors for the user input and patterns
    all_tokens = user_input_tokens + [
        token for pattern in pattern_tokens for token in pattern
    ]
    all_tokens = sorted(list(set(all_tokens)))
    user_input_vector = np.zeros(len(all_tokens))
    pattern_vectors = np.zeros((len(pattern_tokens), len(all_tokens)))
    for i, token in enumerate(all_tokens):
        if token in user_input_tokens:
            user_input_vector[i] = 1.0 / len(user_input_tokens)
        for j, pattern_token in enumerate(pattern_tokens):
            if token in pattern_token:
                pattern_vectors[j, i] = 1.0 / len(pattern_token)

    # Calculate the cosine similarities between the user input and the patterns
    similarity_scores = cosine_similarity([user_input_vector], pattern_vectors)[0]
    if max(similarity_scores) < threshold:
        return "NO MATCH"

    # Find the index of the highest similarity score
    closest_match_index = np.argmax(similarity_scores)

    # Return the closest match as a string
    closest_match = patterns[closest_match_index]
    return closest_match


def named_entity_recognition(message) -> Dict[str, str]:
    # Process message with spacy
    doc = NER(message)
    named_entities = {}
    for entity in doc.ents:
        named_entities[entity.text] = entity.label_
    return named_entities


def extract_person(named_entities):
    # Find the entity labeled as "PERSON" and return its text
    for entity in named_entities:
        if named_entities[entity] == "PERSON":
            return entity

    # If no "PERSON" entity was found, return None
    return ""
