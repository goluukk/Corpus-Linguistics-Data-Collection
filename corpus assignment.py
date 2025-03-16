import glob
import nltk
from nltk import word_tokenize
from nltk.text import ConcordanceIndex
nltk.download('punkt')
nltk.download('punkt_tab')
import re

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
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                    # Get the text ID (from filename)
                    # To do this, replace the '.txt' part of the file name with nothing
                    text_id = filename.replace('.txt', '')

                    # Extract metadata using regex
                    # For this, use re.search(). It's like findall(), but only returns the first match.
                    # Save the information we want in a capturing group
                    # Then output the capturing group by adding .group(1) at the end of the
                    id = re.search(r'<id>(.*?)</id>', text).group(1)
                    title = re.search(r'<title>(.*?)</title>', text).group(1)
                    year = re.search(r'<date of text>(.*?)</date of text>', text).group(1)
                    author = re.search(r'<author>(.*?)</author>', text).group(1)
                    gender = re.search(r"<author's gender>(.*?)</author's gender>", text).group(1)
                    genre = re.search(r'<genre>(.*?)</genre>', text).group(1)

                    # Store in metadata dictionary
                    self.CLMET_metadata[text_id] = {
                        'ID': id,
                        'Title': title,
                        'Year': year,
                        'Author': author,
                        'Gender': gender,
                        'Genre': genre,
                        'Mode': 'Written',
                        'Variety': 'BrE',
                        'Corpus': 'CLMET-3'
                    }

            elif filename.startswith('18'):
            # Create dictionary for metadata
                text_metadata = {}
                lines = text.split("\n")  # Split text by lines
                metadata = {
                        'text_title': 'Unknown',
                        'year': 'Unknown',
                        'author_name': 'Unknown',
                        'author_gender': 'Unknown',
                        'genre': 'Fiction',
                        'mode': 'Written',
                        'variety': 'BrE',
                        'corpus': 'HUM19UK'
                    }

            # Example: Assume metadata is in the first few lines in format "Key: Value"
                for line in lines[:10]:  # Read only first 10 lines (adjust if needed)
                    line = line.replace(">", "").strip()  # 🚀 Remove ">" if it exists
                    if "Title:" in line:
                        metadata['text_title'] = line.split("Title:")[-1].strip()
                    elif "Author:" in line:
                        metadata['author_name'] = line.split("Author:")[-1].strip()
                    elif "Publication date:" in line:
                        metadata['year'] = line.split(":")[-1].strip()
                    elif "Gender:" in line:
                        metadata['author_gender'] = line.split("Gender:")[-1].strip()
                    elif "Genre:" in line:
                        metadata['genre'] = line.split("Genre:")[-1].strip()
                    elif "Mode:" in line:
                        metadata['mode'] = line.split("Mode:")[-1].strip()
                    elif "Variety:" in line:
                        metadata['variety'] = line.split("Variety:")[-1].strip()

                return metadata


                # Read each file and extract metadata
                for filename in filenames:
                    with open(filename, 'r', encoding='ISO-8859-1') as text:
                        content = text.read()
                        metadata = extract_metadata(content)  # Extract metadata from text

                        text_metadata[filename] = {
                            'conc_index': concordance_indices.get(filename, None),  # Avoid KeyError
                            **metadata  # Merge extracted metadata into dictionary
                        }

                    # Debugging: Print metadata to check extraction
                    print(f"Metadata for {filename}: {text_metadata[filename]}")
                    
                        
                            
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