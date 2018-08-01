class Stack:

    def __init__(self):
        self.items = []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def isEmpty(self):
        if len(self.items)==0:
            return True
        else:
            return False

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return " ".join(map(str,self.items))

if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print s
    a = s.pop()
    print a
    print len(s)