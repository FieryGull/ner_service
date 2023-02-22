from typing import Dict, List

import spacy
from spacy.tokens.doc import Doc

NLP = spacy.load("en_core_web_sm")


def get_entities_statistic(doc: Doc) -> Dict[str, List[str]]:
    """
    Generate json statistic of texts entities
    :param doc: spacy doc container with marked text
    :return: json-statistic
    """
    doc_ner_labels = (ent.label_ for ent in doc.ents)
    stat_dict = {}
    for ent_label in doc_ner_labels:
        stat_dict[ent_label] = [ent.text for ent in doc.ents if ent.label_ == ent_label]

    return stat_dict
