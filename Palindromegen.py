from collections import Counter

s='Alex is a good boy and he also love to cheat others that he hate'
x=s.split()
print (x)
word=Counter(x)
print (word)
print (sum(word.values()))
print (len(list (word)))
print (set(word))
print (dict(word))

print(word.items())
print (Counter(dict(word.items())))

print (word.most_common(3)[:-1-1:-1])

