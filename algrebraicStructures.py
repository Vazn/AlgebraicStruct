from math import *

from numpy import arccos

class Complex:
   def __init__(self, real, imaginary):
      self.values = (real, imaginary)    
      self.modulus = sqrt(real**2 + imaginary**2)
      self.argument = arccos(real / self.modulus)

   def __str__(self):
      realPart = str(self.values[0])
      complexPart = str(self.values[1]) + "i" if abs(self.values[1]) != 1 else "i"

      if self.values[0] == 0: 
         if (self.values[1] < 0):
            return "- " + complexPart
         return complexPart
      if self.values[1] < 0: return realPart + " - " + complexPart
      if self.values[1] == 0: return realPart
      return realPart + " + " + complexPart
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

   def conjugate(self): 
      return Complex(self.values[0], -self.values[1])


class Polynomials:
   def __init__(self, *args):    
      self.coefs = self.cutZeroes(args)
      self.exponents = [*range(0, len(self.coefs))]

      self.degree = self.getDegree()
      self.valuation = self.getValuation()
   def __str__(self):
      polynomial = ""
      coefs = tuple(reversed(self.coefs))
      if (self.degree == "-inf"):
         return "0K[X]"
      for i in range(len(coefs)):
         if coefs[i] == 0:
            continue
         if i != 0:
            polynomial += " + "
         if i == len(coefs) - 1:
            polynomial += f"{coefs[i]}"
         elif i == len(coefs) - 2:
            polynomial += f"{coefs[i]}X"
         else:
            polynomial += f"{coefs[i]}X^{len(coefs) - 1 - i}"

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
      return rest.__truediv__(divisor, quotient)

   # Dérivée n-ième OK
   def differentiate(self, n = 1):
      list = []
      for i in range(1, len(self.coefs)):
         newCoef = self.coefs[i] * self.exponents[i]
         list.append(newCoef)

      result = Polynomials(*list)
      if (n == 1):
         return result
      return result.differentiate(n - 1)   
   # Primitive n-ième ?
   def integrate(self):
      list = [0] * (self.degree + 2)
      list[0] = "Constant"
      for i in range(len(self.coefs)): list[i + 1] = round(self.coefs[i] / (i + 1), 3)
         
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

# # # # # # # # # # #  TEST # # # # # # # # # # # # # # 

complex1 = Complex(-5, 1);
print(complex1.conjugate())

poly = Polynomials(2, 1, 5, 6, 0, 25)
# print(poly.differentiate(10))

poly2 = Polynomials(6, 5, 2)
division = poly / poly2
print(f"Quotient : {division[0]}, Reste: {division[1]}")
