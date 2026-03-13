from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from utils.logger import lg

lg.info("=============================================================== PREPROCESSING ===============================================================")

stop_words = set(stopwords.words("english"))

def filtering_stop_words(query:str)->str :
    try:
        lg.info("Initializing filtering_stop_words")

        tokens = word_tokenize(query.lower())

        keywords = [w for w in tokens if w.isalnum() and w not in stop_words]

        filter_query = " ".join(keywords)

        lg.info("filtering_stop_words successfully")

        return filter_query

    except Exception as e:
        lg.error(f"filtering_stop_words failed: {str(e)}")
        raise e
