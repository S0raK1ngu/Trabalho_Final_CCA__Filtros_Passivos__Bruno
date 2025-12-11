# Trabalho_Final_CCA__Filtros_Passivos__Bruno

## Circuitos de Corrente Alternada - CC44CP
**Prof. Dionatan Cieslak, Dr. Eng.**

## **Autor:** Bruno Tiecher

---

## Apresentação do Problema

### Enunciado

Você foi contratado(a) como engenheiro(a) para projetar um crossover passivo para uma caixa de som de duas vias (woofer e tweeter). O objetivo é garantir que os sinais de baixa frequência sejam enviados apenas para o woofer e os de alta frequência apenas para o tweeter, com máxima fidelidade e uma transição suave.

### Contexto

Em sistemas de áudio de alta qualidade, diferentes alto-falantes (woofers e tweeters) são responsáveis por reproduzir diferentes faixas de frequência. O **crossover de áudio** é um circuito eletrônico que divide o sinal de áudio em bandas de frequência específicas, direcionando frequências baixas para o woofer e frequências altas para o tweeter.

O desafio é projetar um sistema de crossover passivo de **2ª ordem** utilizando componentes comerciais (indutores e capacitores) que se aproximem dos valores ideais calculados teoricamente, mantendo a qualidade da resposta em frequência do sistema e garantindo uma transição suave entre os alto-falantes.

---

## Objetivos e Especificações do Projeto

### Objetivos Principais:
1. **Projetar filtros Butterworth de 2ª ordem** para separação de frequências
2. **Calcular valores ideais** de indutores e capacitores baseados na teoria de filtros
3. **Selecionar componentes comerciais** mais próximos dos valores ideais
4. **Analisar o impacto** da diferença entre componentes ideais e comerciais
5. **Gerar diagramas de Bode** comparativos para visualização das respostas em frequência

### Especificações Técnicas:
- **Impedância de carga (R_L):** 6 Ω (Atribuido pelo Professor)
- **Frequência de corte (f_c):** 3200 Hz (Atribuido pelo Professor)
- **Tipo de filtro:** Butterworth de 2ª ordem (ζ = √2)
- **Topologia:** 
  - **LPF (Low-Pass Filter):** Para o woofer (frequências ≤ 3200 Hz)
  - **HPF (High-Pass Filter):** Para o tweeter (frequências ≥ 3200 Hz)

---

## Funções de Transferência e Fórmulas

### Denominador Comum
Ambos os filtros compartilham o mesmo denominador:

```
D(jω) = (1 - LC·ω²) + j·(L/R)·ω
```

### Filtro Passa-Baixas (LPF)
A função de transferência do filtro passa-baixas é:

```
H_LPF(jω) = 1 / D(jω)
```

Este filtro permite a passagem de frequências abaixo de f_c com atenuação mínima e atenua progressivamente as frequências acima de f_c.

### Filtro Passa-Altas (HPF)
A função de transferência do filtro passa-altas é:

```
H_HPF(jω) = -LC·ω² / D(jω)
```

Este filtro permite a passagem de frequências acima de f_c e atenua as frequências abaixo de f_c.

### Cálculo dos Componentes Ideais

**Indutor ideal:**
```
L = (ζ · R_L) / ω_c
onde ω_c = 2π · f_c
```

**Capacitor ideal:**
```
C = 1 / (ζ · R_L · ω_c)
```

### Métricas de Desempenho

**Ganho em dB:**
```
G(dB) = 20 · log₁₀(|H(jω)|)
```

**Fase:**
```
φ = arctan(Im(H) / Re(H))
```

---

## Explicação da Lógica do Programa

### Estrutura do Código

O programa está organizado em 5 seções principais:

#### 1. Parâmetros e Constantes
Define os parâmetros fundamentais do projeto:
- Impedância de carga (R_L = 6 Ω)
- Frequência de corte (f_c = 3200 Hz)
- Coeficiente de amortecimento para Butterworth (ζ = √2)

#### 2. Listas de Componentes Comerciais
Contém arrays com valores padronizados de indutores (série E12) e capacitores disponíveis no mercado. Estes valores seguem as séries comerciais padrão da indústria eletrônica.

#### 3. Cálculo e Seleção de Componentes
- Calcula valores ideais usando as fórmulas de Butterworth
- Implementa função `encontrar_comercial()` que busca o valor comercial mais próximo do ideal usando distância mínima
- Calcula o erro percentual entre valores ideais e comerciais

#### 4. Funções de Transferência
Implementa três funções principais:
- `H_denominador()`: Calcula o denominador comum D(jω)
- `H_LPF()`: Retorna a função de transferência do filtro passa-baixas
- `H_HPF()`: Retorna a função de transferência do filtro passa-altas

Além disso, calcula:
- Ganho em dB para visualização logarítmica
- Fase em graus para análise de resposta temporal
- Frequência de corte real no ponto de -3 dB

#### 5. Geração de Gráficos e Tabelas
Produz 4 figuras:
1. **Diagrama de Bode do LPF** (magnitude e fase)
2. **Diagrama de Bode do HPF** (magnitude e fase)
3. **Tabela de Componentes** (valores ideais vs comerciais)
4. **Tabela de Frequências de Corte** (comparação ideal vs real)

### Fluxo de Execução

```
1. Definir parâmetros do projeto (R_L, f_c, ζ)
2. Calcular valores ideais (L_ideal, C_ideal)
3. Buscar valores comerciais mais próximos
4. Gerar vetor de frequências logaritmicamente espaçado (100 Hz a 20 kHz)
5. Calcular H_LPF e H_HPF para cada frequência (ideal e comercial)
6. Converter para ganho (dB) and fase (graus)
7. Encontrar frequências de corte reais (-3 dB)
8. Plotar gráficos comparativos
9. Gerar tabelas de análise
10. Exibir resultados
```

---

## Como Executar o Código

### Requisitos
- Python 3.7 ou superior
- Bibliotecas necessárias:
  - `numpy`
  - `matplotlib`

### Instalação das Dependências
```bash
pip install numpy matplotlib
```

### Execução
```bash
python trabalho_CCA_Bruno.py
```

### Resultados Gerados
O programa irá exibir 4 janelas:
1. **Figura 1:** Diagrama de Bode do LPF (Woofer)
2. **Figura 2:** Diagrama de Bode do HPF (Tweeter)
3. **Figura 3:** Tabela de Componentes
4. **Figura 4:** Tabela de Frequências de Corte

Cada gráfico de Bode contém dois subplots:
- **Superior:** Magnitude em dB vs Frequência
- **Inferior:** Fase em graus vs Frequência

As linhas tracejadas representam os valores ideais (teóricos), enquanto as linhas sólidas representam os valores reais (com componentes comerciais).

---

## Análise dos Resultados

### Figura 1: Diagrama de Bode - Filtro Passa-Baixas (LPF)

![caminho/para/figura1_lpf.png](https://github.com/S0raK1ngu/Trabalho_Final_CCA__Filtros_Passivos__Bruno/blob/6d1e86d86c295697fb1a630d0338a9099fe05146/Imagens%20e%20dados%20gerados/Diagrama%20de%20Bode%20-%20Filtro%20Passa-Baixas%20de%202%C2%AA%20ordem%20-%20Woofer.png))

*Diagrama de Bode do filtro passa-baixas mostrando a magnitude (dB) e fase (graus) em função da frequência. As curvas tracejadas representam o comportamento ideal (Butterworth), enquanto as curvas sólidas mostram o comportamento real com componentes comerciais.*

### Figura 2: Diagrama de Bode - Filtro Passa-Altas (HPF)

![Figura 2 - Diagrama de Bode HPF](caminho/para/figura2_hpf.png)

*Diagrama de Bode do filtro passa-altas mostrando a magnitude (dB) e fase (graus) em função da frequência. Observa-se a atenuação de frequências abaixo de 3200 Hz e a passagem de frequências superiores.*

### Figura 3: Tabela de Análise de Componentes

![Figura 3 - Tabela de Componentes](caminho/para/figura3_componentes.png)

*Comparação entre valores ideais calculados teoricamente e valores comerciais selecionados para indutor e capacitor, incluindo o erro percentual.*

### Figura 4: Tabela de Frequências de Corte

![Figura 4 - Tabela de Frequências](caminho/para/figura4_frequencias.png)

*Análise das frequências de corte reais obtidas com componentes comerciais comparadas com a frequência de corte ideal de projeto (3200 Hz).*

### Valores Ideais vs Comerciais

Os componentes ideais calculados são:
- **L_ideal ≈ 0.3348 mH**
- **C_ideal ≈ 6.9147 µF**

Os componentes comerciais selecionados são:
- **L_comercial = 0.33 mH** (erro: ~-1.43%)
- **C_comercial = 6.8 µF** (erro: ~-1.66%)

### Impacto no Sistema

**Frequências de Corte Reais:**
- **f_c (LPF) ≈ 3235 Hz** (erro: ~+1.09%)
- **f_c (HPF) ≈ 3235 Hz** (erro: ~+1.09%)

### Análise Crítica

#### Pontos Positivos:
1. **Erro mínimo:** Os componentes comerciais apresentam erro inferior a 2%, considerado excelente
2. **Simetria preservada:** Ambos os filtros mantêm praticamente a mesma frequência de corte
3. **Resposta Butterworth:** A característica de máxima planicidade na banda passante é mantida
4. **Atenuação adequada:** Taxa de -40 dB/década conforme esperado para filtros de 2ª ordem

#### Limitações Práticas:
1. **Tolerâncias dos componentes:** Componentes reais têm tolerâncias (±5%, ±10%, ±20%)
2. **Variação com temperatura:** Indutores e capacitores variam com temperatura
3. **Impedância não-constante:** Alto-falantes reais não têm impedância constante em todas as frequências
4. **Resistências parasitas:** Indutores reais possuem resistência série (DCR)

### Impacto Audível

A diferença de ~35 Hz na frequência de corte (3200 Hz → 3235 Hz) é **praticamente inaudível**, pois:
- Representa apenas 1.09% de desvio
- Está dentro da resolução de frequência do ouvido humano (~3% na região de 3 kHz)
- Não causa descasamento perceptível entre woofer e tweeter

---

## Conclusões

### O projeto atingiu os objetivos?
**Sim.** O sistema projetado atende plenamente aos requisitos:
- Frequência de corte de ~3200 Hz alcançada
- Separação eficiente entre woofer e tweeter
- Erro mínimo com componentes comerciais
- Resposta em frequência suave e previsível

### Maior Desafio
O principal desafio foi **minimizar o impacto dos componentes comerciais** nos valores ideais. A discretização da série comercial limita a precisão, mas a seleção cuidadosa (usando busca por menor distância) garantiu excelentes resultados.

### Aprendizados sobre Componentes do Mundo Real

1. **Séries comerciais são limitantes:** Nem sempre é possível obter o valor exato desejado
2. **Otimização é essencial:** A escolha criteriosa pode reduzir erros significativamente
3. **Tolerâncias importam:** Em produção, deve-se considerar variações de ±10-20%
4. **Simulação vs Realidade:** Componentes reais têm comportamento não-ideal (ESR, ESL, DCR)
5. **Engenharia é compromisso:** Projetos reais exigem balancear teoria, disponibilidade e custo

### Considerações Finais

Este projeto demonstra que é possível projetar sistemas de crossover de alta qualidade usando componentes comerciais padrão. A metodologia apresentada pode ser estendida para:
- Outras frequências de corte
- Diferentes impedâncias de carga
- Ordens de filtro superiores (3ª, 4ª ordem)
- Topologias alternativas (Linkwitz-Riley, Bessel)

O uso de ferramentas computacionais (Python/NumPy/Matplotlib) permite otimização rápida e visualização clara dos resultados, facilitando decisões de projeto informadas.

---

## Informações Acadêmicas

**Disciplina:** Circuitos de Corrente Alternada - CC44CP  
**Professor:** Prof. Dionatan Cieslak, Dr. Eng.  
**Autor:** Bruno Tiecher  
**Instituição:** Unviversidade Tecnológica Federal do Paraná - Campus Pato Branco         
**Curso:** Engenharia de Computação  
**Data:** 10/12/2025

---

Este projeto foi desenvolvido para fins educacionais como trabalho final da disciplina de Circuitos de Corrente Alternada.
