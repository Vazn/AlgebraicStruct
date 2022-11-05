from xml import dom


class Complex:
   def __init__(self, newA, newB):
      self.values = (newA, newB)

   def __add__(self, complex):
      return Complex(self.values[0] + complex.values[0], self.values[1] + complex.values[1])

   def __mul__(self, complex):
      imaginary1 = self.values[1]
      imaginary2 = complex.values[1]
      real1 = self.values[0] 
      real2 = complex.values[0] 

      if real1 != 0 and real2 != 0:
         resultReal = real1 * real2
         resultIm = 0
         if imaginary1 != 0 and imaginary2 != 0: 
            resultReal -= imaginary1 * imaginary2
            resultIm = real1 * imaginary2 + real2 * imaginary1
         elif imaginary1 == 0 and imaginary2 != 0:
            resultIm = imaginary2 * real1         
         elif imaginary1 != 0 and imaginary2 == 0:
            resultIm = imaginary1 * real2
      elif real1 == 0 and real2 == 0:
         resultReal = 0
         resultIm = 0
         if imaginary1 != 0 and imaginary2 != 0: 
            resultReal -= imaginary1 * imaginary2

      return Complex(resultReal, resultIm)

   def __str__(self):
      if self.values[1] == 0:
         return str(self.values[0])
      if self.values[0] == 0:
         return str(self.values[1]) + "i"
      return str(self.values[0]) + " + " + str(self.values[1]) + "i"
complexe1 = Complex(0, 1);

class Polynomials:

   def __init__(self, *args):    
      self.coefs = self.cutZeroes(args)
      self.exponents = [*range(0, len(self.coefs))]

      self.degree = self.getDegree()
      self.valuation = self.getValuation()

   def __str__(self):
      polynomial = ""
      if (self.degree == "-inf"):
         return "0K[X]"
      for i in range(len(self.coefs)):
         if self.coefs[i] == 0:
            continue
         if i == 0:
            polynomial += f"{self.coefs[i]}"
         elif i == 1:
            polynomial += f"{self.coefs[i]}X"
         else:
            polynomial += f"{self.coefs[i]}X^{i}"

         if i != len(self.coefs) - 1:
            polynomial += " + "
      return polynomial
   def __add__(self, polynomial):   
      list = []
      for i in range(len(self.coefs)):
         newCoef = self.coefs[i] + polynomial.coefs[i]
         list.append(newCoef)

      return Polynomials(*list)    
   def __sub__(self, polynomial):   
      list = []
      for i in range(len(self.coefs)):
         newCoef = self.coefs[i] - polynomial.coefs[i]
         list.append(newCoef)

      return Polynomials(*list)
   def __mul__(self, polynomial):
      degree = self.degree + polynomial.degree
      polynomialsList = []

      for i in range(0, len(self.coefs)):
         coeffList = [0] * (degree + 1)

         for j in range(0, len(polynomial.coefs)): 
            coeffList[i+j] = self.coefs[i] * polynomial.coefs[j]

         polynomialsList.append(coeffList)

      """ Fait la somme termes à termes des différents listes de coefficients """
      finalCoeffs = [sum(x) for x in zip(*polynomialsList)] 

      return Polynomials(*tuple(finalCoeffs))

   """ 
      Algorithme de division naif.
      On trouve les coefficients dominants du dividende et du diviseur. Le coefficient du quotient (au degré correspondant) sera alors la division des deux.
      stepMultiplication stocke simplement le nombre qu'on vient de rajouter au quotient, et permet de faire la multiplication, puis la soustraction au dividende, pour obtenir le reste.

      La récursion répète le processus avec le reste, avec la condition d'arrêt sur le degré du reste.
      On passe le quotient dans l'appel récursif pour pouvoir le retourner à la fin.
   """
   def __truediv__(self, divisor, quotient = []):
      quotientCurrentDegree = self.degree - divisor.degree
      if (divisor.degree > self.degree):
         print("My program is not for idiots, delete it now, please !")
         return
      if (len(quotient) == 0):
         quotient = [0] * (quotientCurrentDegree + 1)

      divisedDominant = self.coefs[self.degree]
      divisorDominant = divisor.coefs[divisor.degree]

      stepMultiplication = [0] * (quotientCurrentDegree + 1)
      stepMultiplication[quotientCurrentDegree] = divisedDominant / divisorDominant
      quotient[quotientCurrentDegree] = divisedDominant / divisorDominant

      # stepMultiplication permet de multiplier seulement par le nouveau terme du quotient. 
      rest = Polynomials(*(self - (Polynomials(*stepMultiplication) * divisor)).coefs)

      if (rest.degree == "-inf" or rest.degree < divisor.degree):
         return [
            Polynomials(*quotient),
            rest
         ]

      else:
         return rest.__truediv__(divisor, quotient)


   def differentiate(self):
      list = []
      for i in range(1, len(self.coefs)):
         newCoef = self.coefs[i] * self.exponents[i]
         list.append(newCoef)
      return Polynomials(*list)
   def integrate(self):
      list = []
      list.append("Constant")
      for i in range(len(self.coefs)):
         # Bugué
         print("index", i)
         print("coef", self.coefs[i])
         newCoef = self.coefs[i] / (i + 1)

         list.append(newCoef)
         print("list", list)
         print("newcoef at line", i, newCoef)
         
      print(list)
      return Polynomials(*list)

   def cutZeroes(self, args):
      for i in range(1, len(args)):
         if (args[-i] == 0): 
            args = args[:-1]
         else: break
      return args
   def getDegree(self):
      if self.coefs[0] == 0 and len(self.coefs) == 1 : return "-inf"

      for i in range(1, len(self.coefs) + 1):
         if self.coefs[-i] == 0:
            continue
         
         return len(self.coefs) - i
   def getValuation(self):
      if self.coefs[0] == 0 and len(self.coefs) == 1 : return "+inf"
      
      for i in range(len(self.coefs)):
         if self.coefs[i] == 0:
            continue
         return i


poly = Polynomials(6, 5, 32)
poly2 = Polynomials(6, 5, 32)

euclidean = poly / poly2
print(euclidean[1])
