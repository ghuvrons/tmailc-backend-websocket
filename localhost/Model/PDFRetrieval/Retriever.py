import re

class Retriever:
    def __init__(self):
        pass
    
    def numWord(self, text, word):
        text = text.lower()
        word = word.lower()
        i = -1 * len(word)
        result = []
        word = word.replace('*', '[A-z]*')
        while True:
            srcObj = re.search(r'(^|[^A-z])'+word+'($|[^A-z])', text[i+len(word):])
            if srcObj:
                flag = srcObj.start()
                if flag == 0:
                    flag = -1
                i = i+len(word) + flag+1
                result.append(i)
            else:
                break
        return result
    
    def listSentence(self, arrText, words, limit = -1, isGetWordNum = False):
        negative_tone = [
            'negative*', 'material*', 'adverse*', 'damage*', 
            'destroy*', 'loss', 'harm', 'catastroph*', 'tragic*',
            'destruct', 'significant', 'serious', 'hamper']
        tmpWords = []
        for word in words:
            word = word.lower()
            tmpWords.append(word)
        words = tmpWords
        j = 0
        word_number = {}
        for word in words:
            word_number[word] = 0
        sentences = []
        page = 0
        for text in arrText:
            if j == limit and not isGetWordNum:
                break
            textlow = text.lower()
            textlength = len(text)
            page += 1
            listWordsPosition = []
            for word in words:
                tmplistWordPosition = self.numWord(textlow, word)
                word_number[word] += len(tmplistWordPosition)
                listWordsPosition += tmplistWordPosition
            listWordsPosition.sort()
            for wordPosition in listWordsPosition:
                if j == limit:
                    break
                j += 1
                f_flag = wordPosition
                b_flag = wordPosition-1
                while( f_flag < textlength):
                    if re.search(r'\A.[\n\t\r;]|\W\.\W|\.\W\Z|\A\W\.', textlow[f_flag - 1:f_flag + 2]):
                        break
                    f_flag += 1
                while( b_flag > 0):
                    if re.search(r'[\n\t\r;].\Z|\W\.\W|\.\W\Z|\A\W\.', textlow[b_flag - 1:b_flag + 2]):
                        if textlow[b_flag+1] == ' ':
                            b_flag += 1
                        break
                    b_flag -= 1
                sentence = text[b_flag+1:f_flag]
                negtone = {}
                for nt in negative_tone:
                    negtone[nt] = len(self.numWord(sentence, nt))
                sentences.append({'sentence': sentence, 'page':page, 'negative tone': negtone})
                
        if isGetWordNum:
            return [word_number, sentences]
        return sentences