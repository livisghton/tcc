#Codigo extraido do stackoverflow
#https://stackoverflow.com/questions/8703496/hash-map-in-python
"""
Este pacote implementa um hashmap, onde tem por definicao key, value
"""


class Node:
    "Cria uma instancia de Hash"
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    def __init__(self):
        self.store = [None for _ in range(151)]
    def get(self, key):
        index = hash(key) & 150
        if self.store[index] is None:
            return None
        n = self.store[index]
        while True:
            if n.key == key:
                return n.value
            else:
                if n.next:
                    n = n.next
                else:
                    return None
    def put(self, key, value):
        nd = Node(key, value)
        index = hash(key) & 150
        n = self.store[index]
        if n is None:
            self.store[index] = nd
        else:
            if n.key == key:
                n.value = value
            else:
                while n.next:
                    if n.key == key:
                        n.value = value
                        return
                    else:
                        n = n.next
                n.next = nd

"""
Exemplo de uso
hm = HashMap()
hm.put("C", 1)
hm.put("D", 1)
hm.put("E", 1)
hm.put("F", 1)
hm.put("G", 1)
hm.put("A", 1)
hm.put("B", 1)
# hm.put("C", hm.put("C")+1)
k = hm.get("C")
print(hm.get("C"))
k = k+1
hm.put("C", k)
print(hm.get("C"))"""