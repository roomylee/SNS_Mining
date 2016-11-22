from konlpy.tag import *
from konlpy.utils import pprint
import mysql.connector as msc
import pandas as pd


class NLP_Engine:
    def __init__(self):
        self.engines = [Kkma(), Hannanum(), Mecab(), Twitter()]

    def ExtractNoun(self, sentence, eng):
        noun = self.engines[eng].nouns(sentence)
        return noun

    def ExtractPOS(self, sentence, eng):
        POS = self.engines[eng].pos(sentence)
        return POS



