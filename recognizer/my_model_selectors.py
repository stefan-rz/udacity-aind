import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose


    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score
    
    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """
    def get_bic_score(self, n_component):
        model = self.base_model(n_component)
        logL = model.score(self.X, self.lengths)
        logN = np.log(len(self.X))
        d = model.n_features
        # p = = n^2 + 2*d*n - 1
        p = n_component ** 2 + 2 * d * n_component - 1
        bic_score = -2.0 * logL + p * logN
        return model, bic_score
    
    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        
        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best_score = float("-Inf") 
        best_model = None
        try:
            for n_component in range(self.min_n_components, self.max_n_components + 1):
                model, bic_score = self.get_bic_score(n_component)
                if bic_score > best_score:
                    best_model, best_score = model, bic_score
            return best_model
        except Exception as e:
            pass
        return self.base_model(self.n_constant)
        
class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion
    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''
    def get_dic_score(self, n_component):
        model = self.base_model(n_component)
        right_part_scores = []
        for w, (X, lengths) in self.hwords.items():
            if w != self.this_word:
                right_part_scores.append(model.score(X, lengths))
        dic_score = model.score(self.X, self.lengths) - np.mean(right_part_scores)
        return model, dic_score

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best_score = float("-Inf") 
        best_model = None
        try:
            for n_component in range(self.min_n_components, self.max_n_components + 1):
                model, dic_score = self.get_dic_score(n_component)
                if dic_score > best_score:
                    best_model, best_score = model, dic_score
            return best_model
        except Exception as e:
            pass
        return self.base_model(self.n_constant)


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''
    def get_logL(self, num_hidden_states, split_method):
        model = self.base_model(num_hidden_states)  
        
        for train_idx, test_idx in split_method.split(self.sequences):
            # Get test sequences
            test_X, test_lengths = combine_sequences(test_idx, self.sequences)
            logL = model.score(test_X, test_lengths)
        return model, np.mean(logL)

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best_score = float("-Inf")
        best_model = None
        split_method = KFold()
        try:
            for n_component in range(self.min_n_components, self.max_n_components + 1):
                model, mean_logL = self.get_logL(n_component, split_method)
                if mean_logL > best_score:
                    best_score = mean_logL
                    best_model = model
            return best_model
        except Exception as e:
            pass
        return self.base_model(self.n_constant)
  


