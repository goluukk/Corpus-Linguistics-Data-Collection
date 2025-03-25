import glob
import nltk
from nltk import word_tokenize
from nltk.text import ConcordanceIndex
nltk.download('punkt')
nltk.download('punkt_tab')
import re
from tqdm import tqdm
import pickle

class Help_processing:

    def __init__(self):
        self.metadata = {}
        self.all_text_tokenized = {}
        self.file_names = []
        self.concordance_indices = {}

    def tokenizer(self):
        #assumes all files are in the same repository as the code
        #takes all file names ending with .txt and puts them in a list
        for file in glob.glob("*.txt"):
            self.file_names.append(file)
        
        print(self.file_names)

        #dict that stores name of file as key and text as value
        all_text = {}

        # Read each file
        for filename in tqdm(self.file_names):
            with open(filename, 'r', encoding='ISO-8859-1') as text:
                # Use filename as key in dictionary
                all_text[filename] = text.read()

        # Tokenise each text and store with same filename as key
        for filename in tqdm(all_text): 
            self.all_text_tokenized[filename] = word_tokenize(all_text[filename])
        
        with open('all_text_tokenized.pickle', 'wb') as handle:
            pickle.dump(self.all_text_tokenized, handle, protocol = pickle.HIGHEST_PROTOCOL)
        

        print(self.all_text_tokenized)

    def load_all_text_tokenized(self):
        with open('all_text_tokenized.pickle', 'rb') as handle:
            self.all_text_tokenized = pickle.load(handle)


    def generate_metadata(self):
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
                    self.metadata[text_id] = {
                        'TextID': id,
                        'TextName': title,
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
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                    text_id = filename.replace('.txt', '')
                
                    lines = text.split("\n")  # Split text by lines
                    self.metadata[text_id] = {
                                                        'TextName': 'Unknown',
                                                        'Year': 'Unknown',
                                                        'Author': 'Unknown',
                                                        'AuthorGender': 'Unknown',
                                                        'Genre': 'Fiction',
                                                        'Mode': 'Written',
                                                        'Variety': 'BrE',
                                                        'Corpus': 'HUM19UK'
                                                    }

                # Example: Assume metadata is in the first few lines in format "Key: Value"
                    for line in lines[:10]:  # Read only first 10 lines (adjust if needed)
                        line = line.replace(">", "").strip()  # Remove ">" if it exists
                        if "Title:" in line:
                            self.metadata['TextTitle'] = line.split("Title:")[-1].strip()
                        elif "Author:" in line:
                            self.metadata['Author'] = line.split("Author:")[-1].strip()
                        elif "Publication date:" in line:
                            self.metadata['Year'] = line.split(":")[-1].strip()
                        elif "Gender:" in line:
                            self.metadata['AuthorGender'] = line.split("Gender:")[-1].strip()


                # # Read each file and extract metadata
                # for filename in filenames:
                #     with open(filename, 'r', encoding='ISO-8859-1') as text:
                #         content = text.read()
                #         metadata = extract_metadata(content)  # Extract metadata from text

                #         text_metadata[filename] = {
                #             'conc_index': concordance_indices.get(filename, None),  # Avoid KeyError
                #             **metadata  # Merge extracted metadata into dictionary
                #         }

                #     # Debugging: Print metadata to check extraction
                #     print(f"Metadata for {filename}: {text_metadata[filename]}")
                    
                        
                            
            
            #all files starting with an @ symbol are from the TenIndivCorpus                
            elif filename.startswith('@'):
                info = filename.split('@')

                self.metadata[filename] = {
                'conc_index': self.concordance_indices[filename],
                # for me, info[] is an empty string, so I start at 1
                'Author': info[1],
                'TextTitle': info[3],
                'Year': info[4],
                'AuthorGender': info[8],
                'Genre': 'fiction',
                'Mode': 'written',
                'Variety': 'BrE',
                'Corpus': 'TenIndivCorpus'
                }
            else: 
                print(filename)
                raise RuntimeError("Filename unaccounted for: not in CLMET3, HUM19UK, or TenIndivCorpus format")
            return self.metadata
            
    # def find_help(self): 

