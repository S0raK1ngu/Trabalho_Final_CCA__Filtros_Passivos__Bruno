# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                 PROJETO DE CROSSOVER DE ÁUDIO - 2ª ORDEM                   ║
# ║                          Autor: Bruno Tiecher                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import numpy as np              
import matplotlib.pyplot as plt  

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║               1. PARÂMETROS E CONSTANTES DO PROJETO                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# Definição dos parâmetros principais do circuito
R_L = 6.0                          
f_c = 3200.0                       
omega_c = 2 * np.pi * f_c          
ZETA = np.sqrt(2)                   

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║            2. LISTAS DE VALORES COMERCIAIS DE COMPONENTES                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# Lista de indutores disponíveis comercialmente
L_comerciais_mH = [
    0.10, 0.12, 0.15, 0.18, 0.22, 0.27, 0.33, 0.39, 0.47, 0.56, 0.68, 0.82,
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10.0, 12.0, 15.0
]
# Conversão para Henry (H)
L_comerciais_H = np.array([v / 1000 for v in L_comerciais_mH])

# Lista de capacitores disponíveis comercialmente
C_comerciais_uF = [
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2,
    10.0, 12.0, 15.0, 18.0, 22.0, 27.0, 33.0, 39.0, 47.0, 56.0, 68.0, 82.0, 100.0
]
# Conversão para Farad
C_comerciais_F = np.array([v / 1e6 for v in C_comerciais_uF])

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║         3. CÁLCULO DOS VALORES IDEAIS E SELEÇÃO COMERCIAL                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# Cálculo do indutor ideal
L_ideal = (ZETA * R_L) / omega_c

# Cálculo do capacitor ideal
C_ideal = 1 / (ZETA * R_L * omega_c)

def encontrar_comercial(valor_ideal, lista_comercial):

    # Calcula a diferença entre o valor ideal e cada valor da lista
    diferencas = np.abs(lista_comercial - valor_ideal)
    # Encontra a posição do menor valor (mais próximo)
    indice_min = np.argmin(diferencas)
    # Retorna o valor comercial mais próximo
    return lista_comercial[indice_min]

# Seleção dos componentes comerciais mais próximos dos ideais
L_comercial = encontrar_comercial(L_ideal, L_comerciais_H)
C_comercial = encontrar_comercial(C_ideal, C_comerciais_F)

# Conversão das unidades (mH e µF)
L_ideal_mH = L_ideal * 1000        
C_ideal_uF = C_ideal * 1e6         
L_comercial_mH = L_comercial * 1000
C_comercial_uF = C_comercial * 1e6

# Cálculo do erro percentual entre valores ideais e comerciais
erro_L = ((L_comercial - L_ideal) / L_ideal) * 100
erro_C = ((C_comercial - C_ideal) / C_ideal) * 100

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║          4. FUNÇÕES DE TRANSFERÊNCIA E CÁLCULO DE GANHOS                   ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def H_denominador(omega, L, C, R):
    
    j_omega = 1j * omega 

    # Fórmula: D(jω) = (1 - LC×ω²) + j×(L/R)×ω
    return (1 - L * C * (omega**2)) + j_omega * (L / R)

def H_LPF(omega, L, C, R):
    
    return 1 / H_denominador(omega, L, C, R)

def H_HPF(omega, L, C, R):
    
    numerador = -(L * C * (omega**2))
    return numerador / H_denominador(omega, L, C, R)

def ganho_dB(H):
    
    return 20 * np.log10(np.abs(H))

def fase_graus(H):
    
    return np.angle(H, deg=True)

def encontrar_fc_real(f_range, ganho_real_dB):
   
    # Ganho máximo
    ganho_max = np.max(ganho_real_dB)
    index = np.argmin(np.abs(ganho_real_dB - (ganho_max - 3)))
    return f_range[index]

# ─────────────────────────────────────────────────────────────────────────────
#  Cálculo de Todas as Respostas em Frequência
# ─────────────────────────────────────────────────────────────────────────────

f_start = 100          
f_end = 20000          
num_pontos = 1000       


f_range = np.logspace(np.log10(f_start), np.log10(f_end), num_pontos)
omega_range = 2 * np.pi * f_range  

# Para componentes IDEAIS
H_LPF_ideal = H_LPF(omega_range, L_ideal, C_ideal, R_L)
H_HPF_ideal = H_HPF(omega_range, L_ideal, C_ideal, R_L)
ganho_LPF_ideal_dB = ganho_dB(H_LPF_ideal)
ganho_HPF_ideal_dB = ganho_dB(H_HPF_ideal)
fase_LPF_ideal = fase_graus(H_LPF_ideal)
fase_HPF_ideal = fase_graus(H_HPF_ideal)

# Para componentes COMERCIAIS
H_LPF_real = H_LPF(omega_range, L_comercial, C_comercial, R_L)
H_HPF_real = H_HPF(omega_range, L_comercial, C_comercial, R_L)
ganho_LPF_real_dB = ganho_dB(H_LPF_real)
ganho_HPF_real_dB = ganho_dB(H_HPF_real)
fase_LPF_real = fase_graus(H_LPF_real)
fase_HPF_real = fase_graus(H_HPF_real)

# Frequências de corte reais
f_c_LPF_real = encontrar_fc_real(f_range, ganho_LPF_real_dB)
f_c_HPF_real = encontrar_fc_real(f_range, ganho_HPF_real_dB)

# Calculo do erro percentual das frequências de corte
erro_fc_LPF = ((f_c_LPF_real - f_c) / f_c) * 100
erro_fc_HPF = ((f_c_HPF_real - f_c) / f_c) * 100

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║             5. GERAÇÃO DOS GRÁFICOS E TABELA                               ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# ─────────────────────────────────────────────────────────────────────────────
#  GRÁFICO 1: Filtro Passa-Baixas (LPF) - Para o Woofer
# ─────────────────────────────────────────────────────────────────────────────

fig1 = plt.figure(1, figsize=(10, 8))  

ax1 = plt.subplot(2, 1, 1)  

plt.semilogx(f_range, ganho_LPF_ideal_dB, 'b--', label='LPF Ideal (Butterworth)', linewidth=2)

plt.semilogx(f_range, ganho_LPF_real_dB, 'r-', label='LPF Real (Componentes Com.)', linewidth=2)

plt.axvline(f_c, color='gray', linestyle=':', linewidth=1, 
            label=f'$f_c$ Ideal = {f_c/1000:.2f} kHz')

plt.axvline(f_c_LPF_real, color='r', linestyle=':', linewidth=1, alpha=0.6, 
            label=f'$f_c$ Real = {f_c_LPF_real/1000:.2f} kHz')

plt.axhline(-3, color='k', linestyle=':', linewidth=0.8, label='Ganho -3 dB')

plt.title(f'Diagrama de Bode - Filtro Passa-Baixas (LPF) de 2ª Ordem ($R_L$={R_L} $\Omega$)', 
          fontsize=12, fontweight='bold')
plt.ylabel('Magnitude (dB)', fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.7)
plt.legend(loc='lower left', fontsize='small')
plt.ylim(-40, 5)

ax2 = plt.subplot(2, 1, 2)

plt.semilogx(f_range, fase_LPF_ideal, 'b--', label='Fase Ideal', linewidth=2)

plt.semilogx(f_range, fase_LPF_real, 'r-', label='Fase Real', linewidth=2)

plt.axvline(f_c, color='gray', linestyle=':', linewidth=1)
plt.axvline(f_c_LPF_real, color='r', linestyle=':', linewidth=1, alpha=0.6)

plt.axhline(-90, color='k', linestyle=':', linewidth=0.8, label='Fase -90°')

plt.xlabel('Frequência (Hz)', fontsize=11)
plt.ylabel('Fase (graus)', fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.7)
plt.legend(loc='lower left', fontsize='small')
plt.ylim(-180, 0)

plt.tight_layout() 

# ─────────────────────────────────────────────────────────────────────────────
#  GRÁFICO 2: Filtro Passa-Altas (HPF) - Para o Tweeter
# ─────────────────────────────────────────────────────────────────────────────

fig2 = plt.figure(2, figsize=(10, 8)) 

ax3 = plt.subplot(2, 1, 1)

plt.semilogx(f_range, ganho_HPF_ideal_dB, 'g--', label='HPF Ideal (Butterworth)', linewidth=2)

plt.semilogx(f_range, ganho_HPF_real_dB, 'm-', label='HPF Real (Componentes Com.)', linewidth=2)

plt.axvline(f_c, color='gray', linestyle=':', linewidth=1, 
            label=f'$f_c$ Ideal = {f_c/1000:.2f} kHz')
plt.axvline(f_c_HPF_real, color='m', linestyle=':', linewidth=1, alpha=0.6, 
            label=f'$f_c$ Real = {f_c_HPF_real/1000:.2f} kHz')
plt.axhline(-3, color='k', linestyle=':', linewidth=0.8, label='Ganho -3 dB')

plt.title(f'Diagrama de Bode - Filtro Passa-Altas (HPF) de 2ª Ordem ($R_L$={R_L} $\Omega$)', 
          fontsize=12, fontweight='bold')
plt.ylabel('Magnitude (dB)', fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.7)
plt.legend(loc='lower right', fontsize='small')  
plt.ylim(-40, 5)

ax4 = plt.subplot(2, 1, 2)

plt.semilogx(f_range, fase_HPF_ideal, 'g--', label='Fase Ideal', linewidth=2)

plt.semilogx(f_range, fase_HPF_real, 'm-', label='Fase Real', linewidth=2)

plt.axvline(f_c, color='gray', linestyle=':', linewidth=1)
plt.axvline(f_c_HPF_real, color='m', linestyle=':', linewidth=1, alpha=0.6)

plt.axhline(90, color='k', linestyle=':', linewidth=0.8, label='Fase +90°')

plt.xlabel('Frequência (Hz)', fontsize=11)
plt.ylabel('Fase (graus)', fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.7)
plt.legend(loc='upper left', fontsize='small')  
plt.ylim(0, 180)

plt.tight_layout()  

# ─────────────────────────────────────────────────────────────────────────────
#  TABELA 1: Análise de Componentes (Valores Ideais vs Comerciais)
# ─────────────────────────────────────────────────────────────────────────────

dados_comp_tabela = [
    ["Indutor (L)", f"{L_ideal_mH:.4f} mH", f"{L_comercial_mH:.2f} mH", f"{erro_L:+.2f}%"],
    ["Capacitor (C)", f"{C_ideal_uF:.4f} µF", f"{C_comercial_uF:.2f} µF", f"{erro_C:+.2f}%"]
]
col_comp_labels = ["Componente", "Valor Ideal", "Valor Comercial", "Erro (%)"]

plt.figure(3, figsize=(9, 2.5))
ax_comp = plt.gca()
ax_comp.set_title("Tabela 1: Análise de Componentes - Valores Ideais vs Comerciais", 
                   fontsize=12, fontweight='bold', pad=15)
ax_comp.axis('off')

tabela_comp = ax_comp.table(
    cellText=dados_comp_tabela,
    colLabels=col_comp_labels,
    loc='center',
    cellLoc='center',
    colWidths=[0.25, 0.25, 0.25, 0.25]
)

tabela_comp.auto_set_font_size(False)
tabela_comp.set_fontsize(11)
tabela_comp.scale(1.0, 2.0)

for i in range(4):
    tabela_comp[(0, i)].set_facecolor('#4CAF50')
    tabela_comp[(0, i)].set_text_props(weight='bold', color='white')

cores_linhas = ['#f0f0f0', '#ffffff']
for i in range(1, 3):
    for j in range(4):
        tabela_comp[(i, j)].set_facecolor(cores_linhas[(i-1) % 2])

plt.tight_layout()

# ─────────────────────────────────────────────────────────────────────────────
#  TABELA 2: Análise da Frequência de Corte Real
# ─────────────────────────────────────────────────────────────────────────────

dados_fc_tabela = [
    ["LPF (Woofer)", f"{f_c/1000:.2f} kHz", f"{f_c_LPF_real/1000:.2f} kHz", f"{erro_fc_LPF:+.2f}%"],
    ["HPF (Tweeter)", f"{f_c/1000:.2f} kHz", f"{f_c_HPF_real/1000:.2f} kHz", f"{erro_fc_HPF:+.2f}%"]
]
col_fc_labels = ["Filtro", "fc Ideal", "fc Real", "Erro (%)"]

plt.figure(4, figsize=(9, 2.5))
ax_fc = plt.gca()
ax_fc.set_title("Tabela 2: Análise da Frequência de Corte Real (fc)", 
                fontsize=12, fontweight='bold', pad=15)
ax_fc.axis('off')

tabela_fc = ax_fc.table(
    cellText=dados_fc_tabela,
    colLabels=col_fc_labels,
    loc='center',
    cellLoc='center',
    colWidths=[0.25, 0.25, 0.25, 0.25]
)

tabela_fc.auto_set_font_size(False)
tabela_fc.set_fontsize(11)
tabela_fc.scale(1.0, 2.0)

for i in range(4):
    tabela_fc[(0, i)].set_facecolor('#2196F3')
    tabela_fc[(0, i)].set_text_props(weight='bold', color='white')

for i in range(1, 3):
    for j in range(4):
        tabela_fc[(i, j)].set_facecolor(cores_linhas[(i-1) % 2])

plt.tight_layout()

# ─────────────────────────────────────────────────────────────────────────────
#  Exibição de Todas as Figuras
# ─────────────────────────────────────────────────────────────────────────────

plt.show() 

