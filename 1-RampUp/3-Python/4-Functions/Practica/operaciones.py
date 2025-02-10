def factorial_recursiva(n):
  if n == 0:
    return 1
  else:
    return n * factorial_recursiva(n - 1)

numero = 5
resultado = factorial_recursiva(numero)
print(f"El factorial de {numero} es {resultado}") 