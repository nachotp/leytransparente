from math import pow
from .conn import DBconnection
from gensim.models import KeyedVectors
from numpy.linalg import norm
from django.conf import settings
from nltk.tag import StanfordPOSTagger
import string
import os
import operator
import numpy as np

