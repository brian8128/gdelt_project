from sklearn.decomposition import SparsePCA
import pandas as pd

import numpy as np


class Model(object):

    def __init__(self, company_df, tfidf, vocab, n_components=10):
        """
        We're keeping the company df and the tfidf separate because tfidf is sparse and we want to
        pickle it sparse for massive savings in space and dump/load time.  This means the caller
        is responsible that company_df and tfidf match up
        """
        self.n_components = n_components # 64 bits
        self.company_df = company_df
        self.tfidf = tfidf # Must match up with company df
        self.vocab = vocab
        self.factorization = None # 243K
        self.labels = None

    def fit(self, dif_df):
        factorization = SparsePCA(n_components=self.n_components, alpha=0.03)
        X = dif_df.values[1:]
        self.labels = dif_df.columns.values
        factorization.fit(X)
        self.factorization = factorization

    def transform(self, dif_df):
        '''
        From the fit function we have 'principle components' (vectors) c = [c_0, ..., c_{k-1}]
        which are stored in self.factorization.components_
        Given v, a vector representing one row of the ticker_df, we want to find (scalars) a = [a_0, ..., a_{k-1}]
        such that
                e = sum(a_i * c_i) - v
        is minimized.  The c_i are not orthogonal to each other though, so we can't just use projections.
        Sklearn takes care of the math for us.

        :param dif_df:
        :return: A data frame of the diffs 'projected' onto the 'principle compents'
        '''

        # TODO: Make sure dif_df has the right columns.  Maybe we can be flexible,
        # but be sure to match up columns correctly and perhaps give a warning and fill
        # in zeros if we have missing columns.  If there are extra columns we might be
        # able to ignore that.
        X = dif_df.values

        a = self.factorization.transform(X)

        # We may use the error term later
        # error = np.dot(a, self.factorization.components_) - X

        pc_df = pd.DataFrame(a, index=dif_df.index, columns=["c{}".format(i) for i in range(self.n_components)])

        return pc_df

    def analyze_principle_component(self, component_num, n_companies=15, n_words=20):
        '''
        component: 1d numpy array representing a linear combination of companies

        returns: A dictionary with the following information about the company:
                    'companies_pro': Numpy array of ticker symbols of the top n_companies
                                     companies associated with this component
                    'importances_pro': Numpy array of floats that tell the weight of the
                                       above companies in the principle component
                    'companies_con': Numpy array of ticker symbols of the top n_companies
                                     companies anti-correlated with this component
                    'importances_con': Numpy array of floats that tell the weight of the
                                       above companies in the principle component
                                       (these numbers are positive, measuring the anti-correlation)
                    'words_pro':
                    'word_importances_pro':
        '''

        component = self.factorization.components_[component_num]
        component_labels = self.labels
        company_df = self.company_df
        # We need this here, so do it.  It's not so bad in memory, something about the way we do this
        # doesn't work seem to work well with pickle
        tfidf = map(lambda x: x.flatten(), np.vsplit(self.tfidf.toarray(), self.tfidf.shape[0]))
        company_df['tfidf'] = tfidf

        vocab = self.vocab

        d = {}
        idx_con = np.argsort(component)[:n_companies]
        d['companies_con'] = component_labels[idx_con]
        d['importances_con'] = component[idx_con] * -1.

        idx_pro = np.argsort(component)[::-1][:n_companies]
        d['companies_pro'] = component_labels[idx_pro]
        d['importances_pro'] = component[idx_pro]

        word_importances_con = company_df.ix[d['companies_con'], :]['tfidf'].mean()
        word_idx_con = word_importances_con.argsort()[::-1][:n_words]
        d['words_con'] = np.array(vocab)[word_idx_con]
        d['word_importances_con'] = word_importances_con[word_idx_con]

        word_importances_pro = company_df.ix[d['companies_pro'], :]['tfidf'].mean()
        word_idx_pro = word_importances_pro.argsort()[::-1][:n_words]
        d['words_pro'] = np.array(vocab)[word_idx_pro]
        d['word_importances_pro'] = word_importances_pro[word_idx_pro]

        return d