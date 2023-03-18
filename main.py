import math, os, pickle, re, csv
from typing import Tuple, List, Dict

class BayesClassifier:
    def __init__(self):
        self.real_freqs: Dict[str, int] = {}
        self.fake_freqs: Dict[str, int] = {}
        self.real_filename: str = "real.dat"
        self.fake_filename: str = "fake.dat"

        if os.path.isfile(self.real_filename) and os.path.isfile(self.fake_filename):
            print("Data files found - loading to use cached values...")
            self.real_freqs = self.load_dict(self.real_filename)
            self.fake_freqs = self.load_dict(self.fake_filename)
        else:
            print("Data files not found - running training...")
            self.train()
        
    def train(self):
        print("Running Training...")

        # Train the model on real news data
        with open("True.csv", "r", encoding="utf-8") as true_csv:
            csv_reader = csv.reader(true_csv)
            next(csv_reader)
            for line in csv_reader:
                title = line[0]
                text = line[1]
                title_token = self.tokenize(title)
                text_token = self.tokenize(text)
                self.update_dict(title_token, self.real_freqs)
                self.update_dict(text_token, self.real_freqs)
        true_csv.close()

        with open("Fake.csv", "r", encoding="utf-8") as fake_csv:
            csv_reader = csv.reader(fake_csv)
            next(csv_reader)
            for line in csv_reader:
                title = line[0]
                text = line[1]
                title_token = self.tokenize(title)
                text_token = self.tokenize(text)
                self.update_dict(title_token, self.fake_freqs)
                self.update_dict(text_token, self.fake_freqs)
        true_csv.close()

        # Uncomment later
        self.save_dict(self.real_freqs, self.real_filename)
        self.save_dict(self.fake_freqs, self.fake_filename)

    def classify(self, text: str) -> str:
        """Classifies given text as positive, negative or neutral from calculating the
        most likely document class to which the target string belongs
        Args:
            text - text to classify
        Returns:
            classification, either positive, negative or neutral
        """
        # TODO: fill me out

        
        # get a list of the individual tokens that occur in text
        tokens = self.tokenize(text)


        # create some variables to store the positive and negative probability. since
        # we will be adding logs of probabilities, the initial values for the positive
        # and negative probabilities are set to 0
        real_prob = 0
        fake_prob = 0

        # get the sum of all of the frequencies of the features in each document class
        # (i.e. how many words occurred in all documents for the given class) - this
        # will be used in calculating the probability of each document class given each
        # individual feature
        num_real_words = sum(self.real_freqs.values())
        num_fake_words = sum(self.fake_freqs.values())

        # for each token in the text, calculate the probability of it occurring in a
        # postive document and in a negative document and add the logs of those to the
        # running sums. when calculating the probabilities, always add 1 to the numerator
        # of each probability for add one smoothing (so that we never have a probability
        # of 0)
        for word in tokens:
            num_pos_apps = 1
            if word in self.real_freqs:    
                num_pos_apps += self.real_freqs[word]
            real_prob += math.log(num_pos_apps/num_real_words)

            num_neg_apps = 1
            if word in self.fake_freqs:
                num_neg_apps += self.fake_freqs[word]
            fake_prob += math.log(num_neg_apps/num_fake_words)

        # for debugging purposes, it may help to print the overall positive and negative
        # probabilities
        
        # determine whether positive or negative was more probable (i.e. which one was
        # larger)
        print(f"real_prob is {real_prob}")
        print(f"fake_prob is {fake_prob}")

        if real_prob > fake_prob:
            return "Real"
        elif fake_prob > real_prob:
            return "Fake"
        

    def load_file(self, filepath: str) -> str:
        with open(filepath, "r", encoding='utf8') as f:
            return f.read()

    def save_dict(self, dict: Dict, filepath: str) -> None:
        print(f"Dictionary saved to file: {filepath}")
        with open(filepath, "wb") as f:
            pickle.Pickler(f).dump(dict)

    def load_dict(self, filepath: str) -> Dict:
        print(f"Loading dictionary from file: {filepath}")
        with open(filepath, "rb") as f:
            return pickle.Unpickler(f).load()

    def tokenize(self, text: str) -> List[str]:
        """Splits given text into a list of the individual tokens in order
        Args:
            text - text to tokenize
        Returns:
            tokens of given text in order
        """
        tokens = []
        token = ""
        for c in text:
            if (
                re.match("[a-zA-Z0-9]", str(c)) != None
                or c == "'"
                or c == "_"
                or c == "-"
            ):
                token += c
            else:
                if token != "":
                    tokens.append(token.lower())
                    token = ""
                if c.strip() != "":
                    tokens.append(str(c.strip()))

        if token != "":
            tokens.append(token.lower())
        return tokens

    def update_dict(self, words: List[str], freqs: Dict[str, int]) -> None:
        for word in words:
            if word in freqs:
                freqs[word] += 1
            else:
                freqs[word] =  1

b = BayesClassifier()
real_news = "Pfizer Vaccine Proven Effective in Preventing Covid-19"
fake_news = "ISIS supporter busted in terrifying plot against St. Patrick's Day parade"


print(b.classify(real_news))
print(b.classify(fake_news))