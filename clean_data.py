from nltk.corpus import stopwords
import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Load the CSV file into a Pandas DataFrame
data_frame = pd.read_csv('gutenberg-poetry.csv')

# Create a new DataFrame with only the 'content' column
df1 = pd.DataFrame(data_frame, columns=['content'])

# Define a function to clean the text


def clean_text(text):
    # Remove any non-text characters
    text = re.sub(r'<.*?>', '', text)  # removes HTML tags
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # removes non-ASCII characters
    # Standardize the text
    text = text.lower()
    # removes non-alphanumeric characters except for spaces, commas, full stops, question marks, and exclamation marks
    text = re.sub(r'[^a-zA-Z0-9\s,.?!]', '', text)
    # Remove any irrelevant text
    text = re.sub(r'by [a-zA-Z]+', '', text)  # removes author names
    # Remove space before comma
    text = re.sub(r' (?=,)', '', text)
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    # Remove any stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if not token in stop_words]
    # Join the tokens back into a string
    text = ' '.join(tokens)
    #remove spaces before punctuation
    text = re.sub(r' (?=[.,?!])', '', text)
    #remove double commas and full stops and leave only one
    text = re.sub(r'[,\.]{2,}', '', text)
    # Replace special string with newline characters
    text = text.replace('__NEWLINE__', '\n')
    return text


# Apply the clean_text function to the 'content' column of the DataFrame
df1['content'] = df1['content'].apply(clean_text)

# Write the cleaned data to a text file
with open('gutenberg_poems.txt', 'w') as f:
    for poem in df1['content']:
        f.write(poem)
        f.write('\n\n')  # Add an extra newline between poems
