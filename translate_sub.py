from googletrans import Translator


translator = Translator()

f = open('sample.txt')

translation = translator.translate(f.read(), dest='nl').text

f.close()

print(translation)