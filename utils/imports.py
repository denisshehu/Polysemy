import os
import nltk
from nltk.corpus import wordnet, words
import numpy as np
from sklearn.neighbors import KDTree
import math
from xml.etree import ElementTree
from gensim.models import KeyedVectors
import yaml
import pandas as pd
import gensim.downloader
from gensim.models import FastText
from gph import ripser_parallel
import matplotlib.pyplot as plt
import ripser
from skdim.id import DANCo
import joblib
import time
from gudhi.wasserstein.wasserstein import wasserstein_distance
from gudhi.bottleneck import bottleneck_distance
import scienceplots
from sklearn.decomposition import PCA
