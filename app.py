from flask import Flask, render_template, request, session, redirect, url_for, g
import re
import Levenshtein


app = Flask(__name__)
app.secret_key = 'secretkey'


@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/skurdish', methods = ["GET", "POST"])
def skurdish():
    if request.method == "POST":
        # dictionary to map Latin-based Kurdish alphabets onto Arabic-based Kurdish letters
        latin_to_kurdish = {
            u"a" : u"ا",
            u"e" : u"ە",
            u"b" : u"ب",
            u"ç" : u"چ",
            u"c" : u"چ",
            u"d" : u"د",
            u"ê" : u"ێ",
            u"f" : u"ف",
            u"ğ" : u"غ",
            u"g" : u"گ",
            u"h" : u"ه",
            u"ḧ" : u"ح",
            u"î" : u"ی",
            u"i" : u"",
            u"j" : u"ج",
            u"k" : u"ک",
            u"ł" : u"ڵ",
            u"l" : u"ل",
            u"m" : u"م",
            u"n" : u"ن",
            u"o" : u"ۆ",
            u"p" : u"پ",
            u"q" : u"ق",
            u"ř" : u"ڕ",
            u"r" : u"ر",
            u"ş" : u"ش",
            u"s" : u"س",
            u"t" : u"ت",
            u"û" : u"وو",
            u"u" : u"و",
            u"ü" : u"ۊ" ,
            u"v" : u"ڤ",
            u"w" : u"و",
            u"x" : u"خ",
            u"y" : u"ی",
            u"zh" : u"ژ",
            u"z" : u"ز"
        }

        # retrieves entered text from the input of transliterator and makes it lowercase
        text_to_transliterate2 = request.form["text-to-transliterate"].lower()

        # opens file with kurdish words stored for Levenshtein
        with open('latin_kurdish_words.txt', 'r', encoding='utf-8') as f:
            listedWords = f.read().splitlines()

        # Function for calculating Levenshtein Distance
        def distance(k1, k2):
            return Levenshtein.distance(k1, k2)

        # Function finds word resembling entered word at a Levenshtein Distance of 1
        def fetchWord(word, listedWords):
            distances = [distance(word, w) for w in listedWords]
            closest_kurdish_words = distances.index(min(distances))
            closest_kurdishWord = listedWords[closest_kurdish_words]
            if distance(word, closest_kurdishWord) > 1:
                return None
            else:
                return closest_kurdishWord

        # Function that changes spelling of words at the distance of 1
        def newSpelling(text_to_transliterate2, listedWords):
            words = re.findall(r'\w+', text_to_transliterate2)
            newKurdishString = []
            for word in words:
                closest_kurdishWord = fetchWord(word, listedWords)
                if closest_kurdishWord is None:
                    newKurdishString.append(word)
                else:
                    newKurdishString.append(closest_kurdishWord)
            return ' '.join(newKurdishString)

        text_to_transliterate = newSpelling(text_to_transliterate2, listedWords)


        def transliterate_latin_to_kurdish(text_to_transliterate, latin_to_kurdish):
            
            text_to_transliterate = text_to_transliterate.split()

            for i in range(len(text_to_transliterate)):
                # Adds the ئ letter to signify the the word starts with a vowel
                right_character = list(text_to_transliterate[i])
                for j in range(len(text_to_transliterate[i])):

                    if j == 0:
                        if right_character[0] == 'a' or right_character[0] == 'e' or right_character[0] == 'i' or \
                                right_character[0] == 'o' or right_character[0] == 'u' or right_character[0] == 'ü' \
                                or right_character[0] == 'ê' or right_character[0] == 'î' or right_character[0] == 'û' :
                            y = 'ئ'
                            right_character[j] = y + right_character[j]
                    else:
                        continue

                # joins separated characters back into words
                text_to_transliterate[i] = ''.join(str(right_character) for right_character in right_character)

            # joins separated words back into sentences
            text_to_transliterate = ' '.join(str(text_to_transliterate) for text_to_transliterate in text_to_transliterate)

            regex = re.compile('|'.join(map(re.escape, latin_to_kurdish)))

            kurdish_string = regex.sub(lambda match: latin_to_kurdish[match.group(0)], text_to_transliterate)
            return kurdish_string


        kurdish_string = transliterate_latin_to_kurdish(text_to_transliterate, latin_to_kurdish)


        return render_template('skurdish.html', transliteration_result=kurdish_string)
    return render_template("skurdish.html")

@app.route('/latin', methods = ["GET", "POST"])
def latin():
    if request.method == "POST":
        # dictionary to map Arabic-based Kurdish letters onto Latin-based Kurdish alphabets
        kurdish_to_latin = {
            u"ا": u"a",
            u"ە": u"e",
            u"ب": u"b",
            u"چ": u"ç",
            u"ج": u"c",
            u"د": u"d",
            u"ێ": u"ê",
            u"ف": u"f",
            u"غ": u"ğ",
            u"گ": u"g",
            u"ه": u"h",
            u"ح": u"ḧ",
            u"ی": u"î",
            u"ی": u"",
            u"ژ": u"j",
            u"ک": u"k",
            u"ڵ": u"ł",
            u"ل": u"l",
            u"م": u"m",
            u"ن": u"n",
            u"ۆ": u"o",
            u"پ": u"p",
            u"ق": u"q",
            u"ڕ": u"ř",
            u"ر": u"r",
            u"ش": u"ş",
            u"س": u"s",
            u"ت": u"t",
            u"و": u"u",
            u"ۊ": u"ü",
            u"ڤ": u"v",
            u"و": u"w",
            u"خ": u"x",
            u"ی": u"y",
            u"ز": u"z",
            u"ئ": u""
        }

        # retrieves entered text from the input of transliterator and makes it lowercase
        text_to_transliterate2 = request.form["text-to-transliterate"].lower()

        # opens file with kurdish words stored for Levenshtein 
        with open('kurdish_words.txt', 'r', encoding='utf-8') as f:
            listedWords = f.read().splitlines()

        # Functions for calculating Levenshtein Distance
        def distance(k1, k2):
            return Levenshtein.distance(k1, k2)

        # Functions finds word resembling entered word at a Levenshtein Distance of 1
        def fetchWord(word, listedWords):
            distances = [distance(word, w) for w in listedWords]
            closest_kurdish_words = distances.index(min(distances))
            closest_kurdishWord = listedWords[closest_kurdish_words]
            if distance(word, closest_kurdishWord) > 2:
                return None
            else:
                return closest_kurdishWord

        # Function that changes spelling of words at the distance of 1
        def newSpelling(text_to_transliterate2, listedWords):
            words = re.findall(r'\w+', text_to_transliterate2)
            newKurdishString = []
            for word in words:
                closest_kurdishWord = fetchWord(word, listedWords)
                if closest_kurdishWord is None:
                    newKurdishString.append(word)
                else:
                    newKurdishString.append(closest_kurdishWord)
            return ' '.join(newKurdishString)

        text_to_transliterate = newSpelling(text_to_transliterate2, listedWords)

        # function to transliterate from Kurdish Script to Latin-based Script.
        def transliterate_kurdish_to_latin2(text_to_transliterate):
            text_to_transliterate = text_to_transliterate.split()

            for i in range(len(text_to_transliterate)):
                right_character = list(text_to_transliterate[i])

                for j in range(len(text_to_transliterate[i])):
                    if j:
                        # changes first character in a word to follow rules of writing in Kurdish
                        if j == 0:
                            if right_character[j] == 'ی':
                                right_character[j] = 'y'
                            if right_character[j] == 'و':
                                right_character[j] = 'w'
                        else:
                            if right_character[j] == 'ی':
                                right_character[j] = 'î'
                            if right_character[j] == 'و':
                                right_character[j] = 'u'

                text_to_transliterate[i] = ''.join(str(right_character) for right_character in right_character)

            join_latin_string = ' '.join(str(text_to_transliterate) for text_to_transliterate in text_to_transliterate)

            latin_string = join_latin_string.translate(str.maketrans(kurdish_to_latin))
            return latin_string

        latin_string = transliterate_kurdish_to_latin2(text_to_transliterate)

        return render_template('latin.html', transliteration_result=latin_string)
    return render_template("latin.html")


if __name__=='__main__':
    app.run(debug=True)