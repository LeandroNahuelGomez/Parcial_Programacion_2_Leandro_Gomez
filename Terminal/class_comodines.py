# class Comodines:
#     def __init__(self, lista_comodines:list):
#         self.lista_comodines = lista_comodines

#     def usar_comodin(self, comodin:int):
#         if comodin == 1:
#             if self.lista_comodines[0] > 0:
#                 self.lista_comodines[0] -= 1
#                 print(f"Se ha usado el comodín {comodin}")
#             else:
#                 print(f"No tiene más comodines de tipo {comodin}")
#         elif comodin == 2:
#             if self.lista_comodines[1] > 0:
#                 self.lista_comodines[1] -= 1
#                 print(f"Se ha usado el comodín {comodin}")
#             else:
#                 print(f"No tiene más comodines de tipo {comodin}")
#         elif comodin == 3:
#             if self.lista_comodines[2] > 0:
#                 self.lista_comodines[2] -= 1
#                 print(f"Se ha usado el comodín {comodin}")
#             else:
#                 print(f"No tiene más comodines de tipo {comodin}")
#         else:
#             print(f"Comodín invalido: {comodin}")

#     def lista_comodines_disponibles(self):
#         lista_comodines_bool = []
#         for comodin in self.lista_comodines:
#             if comodin > 0:
#                 lista_comodines_bool.append(True)
#             else:
#                 lista_comodines_bool.append(False)
#         return lista_comodines_bool
    
#     def preguntar_comodin(self):
#         uso = input("Desea utilizar algun comodin? (Si/No): ")
#         if uso.lower() == "si":
#             numero_comodin = int(input("ingrese que comodin desea utilizar: "))
#             self.usar_comodin(numero_comodin)



class Comodines:
    def __init__(self, lista_comodines: list[int]) -> None:
        self.lista_comodines = lista_comodines

    def usar_comodin(self, comodin: int) -> None:
        if 1 <= comodin <= len(self.lista_comodines):
            if self.lista_comodines[comodin - 1] > 0:
                self.lista_comodines[comodin - 1] -= 1
                print(f"Se ha usado el comodín {comodin}")
            else:
                print(f"No tiene más comodines de tipo {comodin}")
        else:
            print(f"Comodín inválido: {comodin}")

    def lista_comodines_disponibles(self) -> list[bool]:
        lista_disponibles = [comodin > 0 for comodin in self.lista_comodines]
        return lista_disponibles

    def preguntar_comodin(self) -> bool:
        uso = input("¿Desea utilizar un comodín? (Si/No): ").lower()
        if uso == "si":
            try:
                numero_comodin = int(input("Ingrese el número de comodín que desea usar: "))
                self.usar_comodin(numero_comodin)
                valor = True
            except ValueError:
                print("Entrada inválida. Ingrese un número entero.")
                valor = False
        
        elif uso == "no":
            valor = False
        else:
            print("Entrada inválida. Ingrese 'Si' o 'No'.")
            valor = False
        
        return valor

# Example usage"""
"""
comodines = Comodines([3, 2, 1])  # Initialize with initial comodin counts

comodines.usar_comodin(1)  # Use comodin type 1
comodines.usar_comodin(2)  # Use comodin type 2

lista_disponibles = comodines.lista_comodines_disponibles()
print(lista_disponibles)  # Output: [True, True, False]

uso_comodin = comodines.preguntar_comodin()
if uso_comodin:
    print("Comodín utilizado correctamente.")
else:
    print("No se utilizó comodín.")"""
