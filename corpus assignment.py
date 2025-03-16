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
                with open(filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                    text_id = filename.replace('.txt', '')
                
                    lines = text.split("\n")  # Split text by lines
                    self.HUM19UK_metadata[text_id] = {
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
                        line = line.replace(">", "").strip()  # Remove ">" if it exists
                        if "Title:" in line:
                            self.HUM19UK_metadata['text_title'] = line.split("Title:")[-1].strip()
                        elif "Author:" in line:
                            self.HUM19UK_metadata['author_name'] = line.split("Author:")[-1].strip()
                        elif "Publication date:" in line:
                            self.HUM19UK_metadata['year'] = line.split(":")[-1].strip()
                        elif "Gender:" in line:
                            self.HUM19UK_metadata['author_gender'] = line.split("Gender:")[-1].strip()
                        elif "Genre:" in line:
                            self.HUM19UK_metadata['genre'] = line.split("Genre:")[-1].strip()
                        elif "Mode:" in line:
                            self.HUM19UK_metadata['mode'] = line.split("Mode:")[-1].strip()
                        elif "Variety:" in line:
                            self.HUM19UK_metadata['variety'] = line.split("Variety:")[-1].strip()

                    return self.HUM19UK_metadata


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
            
    def find_help(self, corpus_name): 
        #tells function which metadata to use based on the corpus name in parameters
        if corpus_name == 'HUM19UK':
            corpus_metadata = self.HUM19UK_metadata
        elif corpus_name == 'CLMET3':
            corpus_metadata = self.CLMET_metadata
        elif corpus_name == 'TenIndivCorpus':
            corpus_metadata == self.TenIndivCorpus_metadata
        else:
            print(corpus_name)
            raise ValueError("Corpus title unrecognised: please use HUM19UK, CLMET3, or TenIndivCorpus.")
     
            

            #JUST A TEST TO SEE IF THE MERGE THING WORKS


            #Codes for finding "help" (based on HUM19UK):

            # List to store tuples of (hit_id, concordance, metadata)
all_concordances = []

# Define the search term
search_term = "help"
hit_id = 1  # Unique identifier for each instance

# Loop through each text file and its metadata
for filename, metadata in self.HUM19UK_metadata.items():
    if "conc_index" not in metadata:
        print(f"Warning: Missing 'conc_index' for {filename}")
        continue  # Skip this entry if 'conc_index' is missing

    concordance_index = metadata["conc_index"]  # The precomputed concordance index

    # Get concordance lines directly
    concordance_lines = concordance_index.find_concordance(search_term, width=90)

    for line in concordance_lines:
        # Extract KWIC text from ConcordanceLine object
        kwic_context = f"{' '.join(line.left[-15:])} {line.query} {' '.join(line.right[:30])}"  # Ensure 15 before & 30 after

        # Store extracted data
        all_concordances.append(
            (
                hit_id,
                kwic_context.strip(),  # Remove any accidental leading/trailing spaces
                metadata.get("author_name", "Unknown"),
                metadata.get("year", "Unknown"),
                metadata.get("text_title", "Unknown"),
                metadata.get("author_gender", "Unknown"),
                metadata.get("genre", "Unknown"),
                metadata.get("mode", "Unknown"),
                metadata.get("variety", "Unknown"),
                metadata.get("corpus", "Unknown"),
            )
        )
        hit_id += 1  # Increment hit ID

# Print the extracted concordance lines
output = "Hit\tKWIC\tAuthor\tYear\tTitle\tGender\tGenre\tMode\tVariety\tCorpus\n"

for record in all_concordances:
    output += "\t".join(map(str, record)) + "\n"

print(output)