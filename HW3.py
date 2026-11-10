from math import log

# Код с практики
class CountVectorizer:

    def __init__(self, lowercase=True, ngram_size=1):
        self._vocabulary = {}
        self.lowercase = lowercase
        self.ngram_size = ngram_size

    def add_word(self, word):
        if word not in self.vocabulary:
            self.vocabulary[word] = len(self.vocabulary)
        return self.vocabulary[word]

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        text = text.split()
        answer = []
        for i in range(len(text) - (self.ngram_size - 1)):
            answer.append(" ".join(text[i:i + self.ngram_size]))
        return answer

    def get_feature_names(self):
        v = sorted(self.vocabulary.items(), key=lambda i: i[1])
        return [w for w, i in v]

    def transform(self, corpus):
        if not self.vocabulary:
            raise RuntimeError

        matrix = []
        for t in corpus:
            row = [0] * len(self.vocabulary)
            for token in self.tokenize(t):
                if token in self.vocabulary:
                    row[self.vocabulary[token]] += 1
            matrix.append(row)
        return matrix

    def fit_transform(self, corpus):
        return self.fit(corpus).transform(corpus)

    def fit(self, corpus):        
        temp_voc = {}
        temp_i = 0

        for text in corpus:
            for token in self.tokenize(text):
                if token not in temp_voc:
                    temp_voc[token] = temp_i
                    temp_i += 1

        if not temp_voc:
            raise ValueError("Нет токенов или пустой корпус")

        self.vocabulary = temp_voc
        self.ind = temp_i

        return self

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, value):
        self._vocabulary = value

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}

    @classmethod
    def from_dict(cls, state):
        model = cls(
            lowercase=state.get("lowercase", True), 
            ngram_size=state.get("ngram_size", 1)
        )
        model.vocabulary = state.get("vocabulary", {})
        return model

    def to_dict(self):
        return {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self._vocabulary.copy()
        }


class BinaryVectorizer(CountVectorizer):
    def transform(self, corpus):
        if not self.vocabulary:
            raise RuntimeError

        matrix = []
        for t in corpus:
            row = [0] * len(self.vocabulary)
            for token in self.tokenize(t):
                if token in self.vocabulary:
                    row[self.vocabulary[token]] = 1
            matrix.append(row)
        return matrix


# Начало ДЗ
class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase=True, ngram_size=1, use_idf=True):
        super().__init__(lowercase, ngram_size)
        self._idf = []
        self.use_idf = use_idf

    def fit(self, corpus):        
        temp_voc = {}
        temp_i = 0
        doc_count = {}
        N = len(corpus)

        for text in corpus:
            seen = set()
            for token in self.tokenize(text):
                if token not in temp_voc:
                    temp_voc[token] = temp_i
                    temp_i += 1
                if token not in seen:
                    doc_count[token] = doc_count.get(token, 0) + 1
                    seen.add(token)

        if not temp_voc:
            raise ValueError("Нет токенов или пустой корпус")

        idf = []  
        if self.use_idf:
            len_vocab = len(temp_voc)
            idf = [0] * len_vocab
            for token, ind in temp_voc.items():
                idf[ind] = log((N + 1) / (doc_count[token] + 1)) + 1

        self.vocabulary = temp_voc
        self.ind = temp_i
        self.idf = idf

        return self

    def transform(self, corpus):
        if not self.vocabulary:
            raise RuntimeError

        tf_idf_corpus = []
        for text in corpus:
            tf_idf = [0] * len(self.vocabulary)
            tokenized_text = self.tokenize(text)
            n = 0

            for token in tokenized_text:
                if token in self.vocabulary:
                    n += 1

            for token in tokenized_text:
                if token in self.vocabulary:
                    if self.use_idf:
                        tf_idf[self.vocabulary[token]] += 1 / n * self.idf[self.vocabulary[token]]
                    else:
                        tf_idf[self.vocabulary[token]] += 1 / n

            tf_idf_corpus.append(tf_idf)
        return tf_idf_corpus

    @classmethod
    def from_config(cls, config):
        model = cls(
            lowercase=config.get("lowercase", True),
            use_idf=config.get("use_idf", True),
            ngram_size=config.get("ngram_size", 1)
        )
        model.vocabulary = config.get("vocabulary", {})
        return model

    @property
    def idf(self):
        return self._idf.copy()

    @idf.setter
    def idf(self, value):
        self._idf = value

    @idf.deleter
    def idf(self):
        self._idf = []    


class KeywordExtractor:
    def __init__(self, v, top_n=2):
        self.v = v
        self.top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(
                'Переменная `top_n` должна задаваться '
                'как положительное целое число!')
        self._top_n = value

    def fit(self, corpus):
        self.tf_idf_model = self.v.fit(corpus)
        return self

    def extract(self, corpus, top_n=None):
        if top_n is not None:
            self.top_n = top_n

        tf_idf_corpus = self.tf_idf_model.transform(corpus)
        results = []

        for tf_idf in tf_idf_corpus:
            tf_idf_token = []

            for word, ind in self.tf_idf_model.vocabulary.items():
                if tf_idf[ind] > 0:
                    tf_idf_token.append((word, tf_idf[ind]))

            sorted_tf_idf_token = sorted(
                tf_idf_token,
                key=lambda x: (-x[1], x[0])
            )

            results.append(sorted_tf_idf_token[:self.top_n])

        return results


def demo():
    # Обучающие сообщения
    TRAIN_CORPUS = [
        "Марс сигнал сигнал",
        "Марс пыль",
        "Марс сигнал антенна",
    ]

    # Сообщения для проверки
    CHECK_CORPUS = [
        "СИГНАЛ шум сигнал",
        "антенна пыль",
        "марс марс марс",
        "комета", "",
    ]                

    # 1) Веса TF-IDF
    print('Сценарий 1. Веса TF-IDF')
    tfidf = TfidfVectorizer.from_config({})
    tfidf.fit_transform(TRAIN_CORPUS)
    print(tfidf.get_feature_names())
    print(tfidf.idf)
    print(tfidf.transform(TRAIN_CORPUS))
    print(tfidf.transform(CHECK_CORPUS))
    idf = tfidf.idf
    idf.clear()
    print(tfidf.idf)
    print('-' * 10)

    # Настройки и новый fit()
    print('Сценарий 2. Настройки и новый fit()')
    config = {"lowercase": False,
              "use_idf": False}
   
    tf = TfidfVectorizer.from_config(config)
    tf.fit(["Марс марс", "МАРС сигнал"])
    print(tf.get_feature_names())
    print(tf.idf)
    tfidf.fit(["Венера облака"])
    print(tfidf.idf)
    print(tfidf.transform(["Марс Венера облака"]))
    print('-' * 10)

    # 3) Ключевые слова
    print('Сценарий 3. Ключевые слова')
    e = KeywordExtractor(tfidf, top_n=2)
    e.fit(TRAIN_CORPUS)
    print(e.extract(CHECK_CORPUS))
    print(e.extract(CHECK_CORPUS, top_n=1))

    try:
        e.top_n = 0
        e.extract(CHECK_CORPUS, top_n=0)
        print('Код прошел успешно')
    except ValueError:
        print('Была вызвана ошибка ValueError')

    print('-' * 10)


if __name__ == '__main__':
    demo()
