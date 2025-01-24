# Traits

La classe `Characteristic` implementa una caratteristica definita da diversi `Trait`.
In un `Trait` troviamo
- nome (`.name`)
- valore (`.optional_value`)
- indice di dominanza (`.dominance`)
- sequenze che lo codificano (`.coding_sequences`)

Una `Characteristic` colleziona diversi `Trait`, di modo che non esistano valori con lo stesso nome, conflitti di sequenze codificanti, o che non completino l'indice di dominanza.

## Quickstart

```python
from traits import Trait, Characteristic


red = Trait("red", dominance=0.1, coding_sequences={"AA", "AA"})
brown = Trait("brown", dominance=0.8, coding_sequences={"CG", "GG"})
blue = Trait("blue", dominance=0.1, coding_sequences={"TT", "CT"})

eye_color = Characteristic("eye_color", 10, [red, brown, blue])

print(eye_color)
# Trait eye_color with values:
#         Trait red with dominance 0.1 and coding sequences {'AA'}
#         Trait brown with dominance 0.8 and coding sequences {'CG', 'GG'}
#         Trait blue with dominance 0.1 and coding sequences {'TT', 'CT'}
```

#### Operazioni
Le `Characteristic` supportano accesso per nome
```python
print(eye_color["red"])
# Trait red with dominance 0.1 and coding sequences {'AA'}
```
e operatore `in`, sia per nome che per `Trait`
```python
print("red" in eye_color, red in eye_color)
```

#### Metodi
Possiamo estrarre un valore da una `Characteristic`
```python
print(eye_color.random_value())
```
Volendo, possiamo anche tenere in considerazione gli indici di dominanza:
```python
print(eye_color.random_value(weighted=True))
```

Inoltre, possiamo cercare il valore di un tratto codificato da un dato genoma:
```python
print(eye_color.search_genome("AA"))
print(eye_color.search_genome("CT"))
print(eye_color.search_genome("TT"))
print(eye_color.search_genome("CG"))
print(eye_color.search_genome("GG"))
print(eye_color.search_genome("TA"))
```