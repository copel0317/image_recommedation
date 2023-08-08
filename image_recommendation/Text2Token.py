import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import WordNetLemmatizer

def _removeNonAscii(s):
    return "".join(i for i in s if  ord(i)<128)

def make_lower_case(text):
    return text.lower()

def remove_stop_words(text):
    text = text.split()
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops]
    text = " ".join(text)
    return text

def remove_punctuation(text):
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text

def tokenization(text):
    words = WordPunctTokenizer().tokenize(text)
    return words

def lemmatization(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]

def Text2Token(df):
    df['cleaned'] = df['Description'].apply(_removeNonAscii)
    df['cleaned'] = df.cleaned.apply(make_lower_case)
    df['cleaned'] = df.cleaned.apply(remove_stop_words)
    df['cleaned'] = df.cleaned.apply(remove_punctuation)
    df['cleaned'] = df.cleaned.apply(tokenization)
    df['cleaned'] = df.cleaned.apply(lemmatization) 
    return df['cleaned']

def vocab(df):
    vocab = list(set(w for words in df.cleaned for w in words if len(w)>=3))
    vocab.sort()
    return vocab

if __name__ == '__main__':
    nltk.download('wordnet')
    nltk.download('stopwords')