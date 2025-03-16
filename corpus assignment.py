import glob
import nltk
from nltk import word_tokenize
from nltk.text import ConcordanceIndex
nltk.download('punkt')
nltk.download('punkt_tab')

class Help_processing:

    def __init__(self):
        self.CLMET_metadata = {}
        self.TenIndivCorpus_metadata = {}
        self.HUM19UK_metadata = {}
        self.all_text_tokenized = {}
        self.file_names = []
        self.concordance_indices = {}

    def tokenizer(self):
        #assumes all files are in the same repository as the code
        #takes all file names ending with .txt and puts them in a list
        for file in glob.glob("*.txt"):
            self.file_names.append(file)

        #dict that stores name of file as key and text as value
        all_text = {}

        # Read each file
        for filename in self.file_names:
            with open(filename, 'r', encoding='utf8') as text:
                # Use filename as key in dictionary
                all_text[filename] = text.read()

        # Tokenise each text and store with same filename as key
        for filename in all_text: 
            self.all_text_tokenized[filename] = word_tokenize(all_text[filename])


    def generate_metadata(self):
        for filename in self.all_text_tokenized:
            self.concordance_indices[filename] = ConcordanceIndex(self.all_text_tokenized[filename])

        for filename in self.file_names:
            if filename.startswith('CLMET3'):

            elif filename.startswith('18'):

            
            #all files starting with an @ symbol are from the TenIndivCorpus
            #
            elif filename.startswith('@'):
                info = filename.split('@')

                self.TenIndivCorpus_metadata[filename] = {
                'conc_index': self.concordance_indices[filename],
                # for me, info[] is an empty string, so I start at 1
                'author': info[1],
                'birth_year': info[2],
                'title': info[3],
                'pub_year': info[4],
                'place': info[5],
                'latitude': info[6],
                'longitude': info[7],
                'gender': info[8],
                'macro_genre': info[9],
                'micro_genre': info[10],
                'word_count': info[11].replace('.txt', ''),
                'genre': 'fiction',
                'mode': 'written',
                'variety': 'BrE',
                'corpus': 'TenIndivCorpus'
                }
            else: 
                print(filename)
                raise RuntimeError("Filename unaccounted for: not in CLMET3, HUM19UK, or TenIndivCorpus format")