# -*- coding: utf-8 -*-

import tweetTokenizer as t
o = t.Tokenizer()
s = "What should I do, be happy with lies or be sad with the truth 😔😩🤔"
print s
s = s.decode('utf8')
print s
o.tokenize(s)
print o.getTokens();