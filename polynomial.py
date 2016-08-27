def lex(n, x, y):   #checks if x > y:   returns x<=y  x, y are terms with coef   n is no. of variables
    for i in range(1, n+1):
        if x[i]==y[i]:
            continue
        else:
            if x[i]>y[i]:
                return -1
            else:
                return 1
    return 0



class Poly(object):
    """Creats polynomial object and perform all polynomial related operations.
        n is number of inderterminants used and l is list of (n+1)-tuples where each tuple represents a term is polynomial
        as first entry as coeficient and remaining n entries are powers of each variables
        p = Poly(3, [(2, 2, 1, 0), (1, 1, 0, 1), (-1, 0, 2, 3)])     # is 2x^2y+xz-y^2z^3"""

    def __init__(self, n, l, order="lex"):
        self.num_of_vars = n
        self.poly = l
        self.num_of_terms = len(l)
        self.order = order
        self.coef = map(lambda x: x[0], self.poly)          #gives list of coeficients
        self.mono = map(lambda x: x[1:], self.poly)         #gives list of multinomials
        self.shape()        
        self.sort()
        self.coef = map(lambda x: x[0], self.poly)
        self.mono = map(lambda x: x[1:], self.poly)
        self.LT = self.poly[0]          #Note self.LT is a tuple but self.LT() is poly object
        self.multideg = self.mono[0]
        self.leading_coef = self.coef[0]

    def sort(self):                  #sort the polynomial in lex order
        if self.order == "lex":
            self.poly.sort(lambda x, y: lex(self.num_of_vars, x, y))
        else:
            print "Sorry Under Construction"

#%%%%%%%%%%%%%%%%
# Remaining work: write for other orders
#%%%%%%%%%%%%%%%%

    def shape(self):                                #removes term with coef 0 and merges terms with same powers
        l = self.poly
        n = self.num_of_vars
        m = self.num_of_terms
        coef = self.coef
        mono = self.mono
        i = 0
        while i<m:
            if float(coef[i])==0.0:
                l.pop(i)
                coef.pop(i)
                mono.pop(i)
                m-=1
            else:
                if mono[i] in mono[i+1:]:
                    c = mono.index(mono[i], i+1)
                    mono.pop(c)
                    coef[i]+=coef.pop(c)
                    l[i]=(coef[i],)+mono[i]
                    l.pop(c)
                    m-=1
                else:
                    i+=1
        if m==0:
            self.poly = [(0, ) + (0,)*n]
            self.num_of_terms = 0
        else:
            self.num_of_terms = m

    def __add__(self, other):
        if self.num_of_vars == other.num_of_vars:
            return Poly(self.num_of_vars, self.poly+other.poly)
        else:
            raise ValueError("variables dont match")

    def __sub__(self, other):
        if self.num_of_vars == other.num_of_vars:
            return Poly(self.num_of_vars, self.poly+map(lambda x: (-x[0],)+x[1:], other.poly))
        else:
            raise ValueError("variables dont match")

    def __mul__(self, other):
        n = self.num_of_vars
        if n == other.num_of_vars:
            poly = []
            for i in range(self.num_of_terms):
                for j in range(other.num_of_terms):
                    poly.append((self.coef[i]*other.coef[j],)+ tuple(map(lambda k: self.mono[i][k]+other.mono[j][k], range(n))))
            return Poly(n, poly)

    def change_indeter_order(self, order):
        """order is a n tuple with ordering o[i]>o[j] if i<j"""
        n = self.num_of_vars
        p = []
        m = []
        for d in self.poly:
            t=(d[0],)
            r=tuple()
            for i in range(n):
                t+=(d[1+order[i]],)
                r+=(d[1+order[i]],)
            p.append(t)
            m.append(r)
        self.poly = p
        self.mono = m

    def LeadingTerm(self):
        return Poly(self.num_of_vars, [self.poly[0]])

    def isdivisible(self, other):    #other is poly object
        n = self.num_of_vars
        if n != other.num_of_vars:
            print "No of Vars is not the same"
            return False
        for i in range(n):
            if self.multideg[i]<other.multideg[i]:
                return False
        return True

    def monodiv(self, other):  #should only used as internal fn; other is tuple
        anscoef = self.leading_coef/other[0]
        ansdeg = tuple()
        for i in range(1, self.num_of_vars+1):
            ansdeg += (self.LT[i]-other[i],)
        return (anscoef,)+ansdeg  #ans is tuple
        
#Aashay Shah :15109267346
