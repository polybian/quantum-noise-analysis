# Simplified explanation

*El ruido cuántico, sin matemáticas que asusten: por qué las
computadoras cuánticas se equivocan, cómo se mide eso, y cómo se
corrige. Si puedes explicarlo en voz alta, lo entiendes de verdad.*

---

## 📻 Capítulo 1: La radio con estática

Una computadora cuántica ideal es como una radio con la señal perfecta:
todo se escucha clarito. Una computadora cuántica **real** es esa misma
radio con **estática**: a veces escuchas la canción, a veces escuchas
*chhhhhh*.

Esa estática tiene nombre: **ruido cuántico**. Y no es un solo ruido,
son varios:

- **Ruido de compuertas:** cada operación sale un poquito mal, como un
  cocinero que siempre echa un pelín más de sal.
- **Ruido de lectura:** al final, cuando "miras" el resultado, a veces
  lees mal el número, como confundir un 6 con un 8 en una receta
  escrita a mano.

Este proyecto no usa una computadora cuántica de verdad: usa un
**simulador con modelos de ruido**, o sea, una radio virtual donde
*yo controlo* cuánta estática poner. Así puedo estudiar el ruido sin
necesitar el hardware.

> 🧒 *"¿Y para qué sirve estudiar la estática?"*
> Porque nadie construye nada serio sobre una máquina que no ha medido.
> Medir el ruido es el primer trabajo de la ingeniería cuántica.

---

## 🔔 Capítulo 2: La campana que a veces miente (mitigación)

El ruido de lectura es tramposo pero predecible: es como una campana
que el 95% de las veces suena "ding" cuando debe, y el 5% suena "dong".

El truco: **calibras la campana primero**. La tocas mil veces anotando
qué suena, y armas una tablita: "cuando debía sonar ding, sonó dong
tantas veces". Esa tablita es la **matriz de calibración**.

Después, cuando corres tu implementación de verdad y la campana suena raro,
usas la tablita *al revés* para corregir: "sonó dong, pero según mi
tablita, lo más probable es que fuera ding". Eso es la **mitigación de
errores de lectura**.

En el proyecto: el error de lectura del estado de Bell baja a **menos
de la mitad** después de corregir. La campana sigue imperfecta, pero
ahora la entiendes.

> ⚠️ Ojo: esto solo arregla el ruido de *lectura*. Si las
> compuertas salieron mal desde el principio, ninguna tablita lo salva.
> Por eso el proyecto lo dice clarito en vez de esconderlo.

---

## 📉 Capítulo 3: Subiendo la estática poco a poco (el barrido)

¿Qué pasa si subes la estática de a poquito? El proyecto corre el
algoritmo de Grover (el detective rapidísimo del proyecto anterior)
con seis niveles de ruido, del más suave al más fuerte, y anota cuántas
veces encuentra la respuesta correcta:

- Con poquita estática: casi 100% de aciertos. 🎯
- Con mucha estática: los aciertos caen hacia 25%, que es lo mismo que
  adivinar al azar. 🎲

Esa curva lo dice todo: no basta con tener más qubits; si cada
compuerta mete ruido, el algoritmo se ahoga. Por eso la carrera
cuántica no es solo "quién tiene más qubits" sino "quién tiene los
qubits *más limpios*".

---

## 🖥️ Capítulo 4: Lo que sí y lo que no

Repito lo importante: **esto corre en un simulador**, con modelos de
ruido realistas pero no calibrados contra ningún dispositivo real. Es
como un simulador de vuelo: te enseña a volar, pero no es el cielo.

El siguiente paso (el de verdad) es correr estos mismos circuitos en
hardware cuántico real (IBM presta acceso gratuito) y comparar: ¿el
ruido medido se parece a mis modelos? Esa comparación es el trabajo
real de un ingeniero cuántico.

---

## ▶️ Cómo correrlo

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash run_all.sh
```

Verás los histogramas ideal vs ruidoso, la tablita de calibración con
el antes/después de la mitigación, y la curva del barrido de ruido. 🎉
