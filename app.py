
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import time

# --- Configuration ---
st.set_page_config(
    page_title="Simulador: Velocidade do Som (AL 2.2)",
    page_icon="🔊",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #0e1117;
    }
    h2 {
        color: #262730;
        border-bottom: 1px solid #d6d6d8;
        padding-bottom: 0.5rem;
    }
    .stButton>button {
        color: white;
        background-color: #ff4b4b;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Oscilloscope_sine_square.jpg/640px-Oscilloscope_sine_square.jpg", use_column_width=True, caption="Osciloscópio")
    st.header("Configuração Ambiental")
    temperature = st.number_input(r"Temperatura do Ar ($^\circ$C)", min_value=0.0, max_value=40.0, value=20.0, step=0.1)
    
    # Theoretical Calculation
    # v = 331.29 + 0.61 * T
    v_theo = 331.29 + 0.61 * temperature
    # st.metric(label="Velocidade Teórica do Som", value=f"{v_theo:.2f} m/s") # Hidden for student challenge
    
    st.markdown("---")
    st.header("Navegação")
    procedure = st.radio("Escolha o Procedimento:", 
        ["1. Método do Impulso/Eco", "2. Método do Desfasamento", "3. Análise de Dados"])

    st.markdown("---")
    st.markdown("**Sobre:** Simulador da A.L. 2.2 - Velocidade de propagação do som.")

# --- Helper Functions ---
def generate_pulse(t, t0, width=0.002):
    return np.exp(-((t - t0)**2) / (2 * width**2))

def plot_oscilloscope(time, ch1, ch2, t_range, y_range=(-1, 1), trigger_level=0.1):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor("#1e1e1e")  # Oscilloscope screen color
    ax.grid(color="#444", linestyle='--', linewidth=0.5)
    
    # Plot signals
    ax.plot(time * 1000, ch1, color="#00ff00", linewidth=1.5, label="CH1 (Fonte/Gerador)")
    ax.plot(time * 1000, ch2, color="#ffff00", linewidth=1.5, label="CH2 (Recetor/Microfone)")
    
    # Setup axis
    ax.set_xlabel("Tempo (ms)", fontsize=12)
    ax.set_ylabel("Tensão (V)", fontsize=12)
    ax.set_xlim(t_range[0]*1000, t_range[1]*1000)
    ax.set_ylim(y_range)
    
    # Add minor ticks for grid
    ax.minorticks_on()
    ax.grid(which='major', color='#888888', linestyle='-', linewidth=1.0) # Brighter, thicker major grid
    ax.grid(which='minor', color='#444444', linestyle=':', linewidth=0.6) # Brighter minor grid
    
    # Legend
    legend = ax.legend(loc='upper right', facecolor='#333', edgecolor='white', labelcolor='white')
    
    plt.tight_layout()
    return fig

# --- Main Content ---
st.title("🔊 A.L. 2.2: Velocidade de Propagação do Som")

if procedure == "1. Método do Impulso/Eco":
    st.header("Procedimento I: Método do Impulso (Mangueira)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        **Material:**
        - Mangueira enrolada (comprimento $d = 15.0$ m)
        - Microfone na extremidade
        - Blocos de madeira (fonte sonora)
        - Osciloscópio
        """)
        
        # Schematic for Procedure I
        st.graphviz_chart("""
        digraph G {
            rankdir=LR;
            node [shape=box, style=filled, fillcolor="#faebd7"];
            Source [label="Fonte Sonora\n(Blocos de Madeira)", fillcolor="#deb887"];
            Mic [label="Microfone"];
            Osc [label="Osciloscópio", shape=component, fillcolor="#add8e6"];
            
            Source -> Mic [label="Som direto (t=0)", style=dashed];
            Source -> Mic [label="Som pela mangueira (d=15m)", color="blue"];
            Mic -> Osc [label="Sinal Elétrico"];
        }
        """)

        st.markdown(r"""
        **Instruções:**
        1. Clique em 'Bater Blocos' para gerar o som.
        2. O canal 1 (verde) mostra o som inicial (t=0).
        3. O canal 2 (amarelo) mostra o som após percorrer a mangueira.
        4. Meça a diferença de tempo $\Delta t$ entre os picos.
        """)
        
        if 'animation_complete' not in st.session_state:
            st.session_state.animation_complete = False
            
        with st.container(border=True):
            st.subheader("🕹️ Realizar Experiência")
            st.write("Clique no botão abaixo para simular o choque entre os blocos:")
            
            if st.button("🪵 Bater Blocos de Madeira", use_container_width=True):
                st.session_state.animation_complete = False
                st.session_state['triggered_p1'] = True
                
                # SVG Animation with Full-Screen Overlay style (using st.markdown to escape iframe limits)
                animation_html = f"""<div id="sound-animation-overlay" style="
position: fixed;
top: 0;
left: 0;
width: 100vw;
height: 100vh;
background-color: rgba(0, 0, 0, 0.75);
display: flex;
justify-content: center;
align-items: center;
z-index: 10000;
backdrop-filter: blur(8px);
animation: fadeIn 0.4s ease-out forwards;
font-family: sans-serif;
">
<style>
@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes clapLeft {{
    0% {{ transform: translateX(0); }}
    20% {{ transform: translateX(120px); }} /* exact fit: 300(center) - 120(start) - 80(width)*/
    25% {{ transform: translateX(120px); }}
    100% {{ transform: translateX(0); }}
}}
@keyframes clapRight {{
    0% {{ transform: translateX(0); }}
    20% {{ transform: translateX(-120px); }} /* exact fit */
    25% {{ transform: translateX(-120px); }}
    100% {{ transform: translateX(0); }}
}}
@keyframes soundWave {{
    0% {{ opacity: 0; offset-distance: 0%; }}
    5% {{ opacity: 1; offset-distance: 0%; }}
    95% {{ opacity: 1; offset-distance: 100%; }}
    100% {{ opacity: 0; offset-distance: 100%; }}
}}
.modal-content {{
    background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
    padding: 40px;
    border-radius: 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    position: relative;
    width: 750px;
    height: 550px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 3px solid #ff4b4b;
}}
.block-left {{
    width: 60px; height: 120px; background: linear-gradient(135deg, #a67c52 0%, #8b4513 100%); 
    position: absolute; left: 120px; top: 100px;
    animation: clapLeft 1s ease-in-out forwards;
    border: 2px solid #5D4037;
    z-index: 10;
    box-shadow: 5px 10px 20px rgba(0,0,0,0.4);
    border-radius: 6px;
}}
.block-right {{
    width: 60px; height: 120px; background: linear-gradient(135deg, #a67c52 0%, #8b4513 100%); 
    position: absolute; right: 120px; top: 100px;
    animation: clapRight 1s ease-in-out forwards;
    border: 2px solid #5D4037;
    z-index: 10;
    box-shadow: -5px 10px 20px rgba(0,0,0,0.4);
    border-radius: 6px;
}}
.sound-pulse {{
    width: 24px; height: 24px; background: radial-gradient(circle, #ff4b4b, #b30000);
    border-radius: 50%;
    position: absolute;
    offset-path: path('M 150 160 L 180 160 C 550 160 550 220 200 220 C 550 220 550 280 200 280 C 550 280 550 340 200 340 C 550 340 550 400 200 400 L 150 400');
    animation: soundWave 3s linear forwards;
    animation-delay: 0.2s;
    opacity: 0;
    z-index: 20;
    box-shadow: 0 0 15px #ff4b4b;
}}
.hose-path {{
    fill: none; stroke: #FFD700; stroke-width: 22; stroke-linecap: round;
    filter: drop-shadow(4px 4px 6px rgba(0,0,0,0.4));
}}
.hose-bg {{
    fill: none; stroke: #B8860B; stroke-width: 28; stroke-linecap: round; opacity: 0.25;
}}
.instruction-text {{
    position: absolute;
    bottom: 40px;
    color: #333;
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.close-hint {{
    position: absolute;
    bottom: 15px;
    color: #666;
    font-size: 0.9rem;
    font-style: italic;
}}
</style>
<div class="modal-content">
    <div style="position: absolute; top: 50px; width: 600px; height: 400px;">
        <svg width="600" height="400" style="position: absolute; top: 0; left: 0; z-index: 1;">
            <text x="300" y="20" text-anchor="middle" fill="#555" font-weight="bold" font-size="14">MÉTODO DO IMPULSO (MANGUEIRA 15M)</text>
            <path class="hose-bg" d="M 150 160 L 180 160 C 550 160 550 220 200 220 C 550 220 550 280 200 280 C 550 280 550 340 200 340 C 550 340 550 400 200 400 L 150 400" />
            <path class="hose-path" d="M 150 160 L 180 160 C 550 160 550 220 200 220 C 550 220 550 280 200 280 C 550 280 550 340 200 340 C 550 340 550 400 200 400 L 150 400" />
        </svg>
        <div class="block-left"></div>
        <div class="block-right"></div>
        <div class="sound-pulse"></div>
    </div>
    <div class="instruction-text">A propagar som...</div>
    <div class="close-hint">(A aguardar conclusão da experiência)</div>
</div>
</div>"""
                st.markdown(animation_html, unsafe_allow_html=True)


                
                # Wait for animation to finish in Python (synchronization)
                with st.spinner("Som a propagar-se..."):
                    time.sleep(3.0) 
                
                st.session_state.animation_complete = True
                st.session_state['measured_time_p1'] = (15.0 / v_theo) * np.random.normal(1.0, 0.005)
                st.rerun()

    
    with col2:
        if st.session_state.get('triggered_p1') and st.session_state.get('animation_complete'):
            # Simulation parameters
            total_time = 0.1  # 100 ms window
            t = np.linspace(0, total_time, 2000)
            
            # Pulse 1 at t=0 (approx, slight delay for visibility)
            t_pulse1 = 0.005
            sig1 = generate_pulse(t, t_pulse1)
            
            # Pulse 2 at t = t_pulse1 + measured_time
            dt = st.session_state['measured_time_p1']
            t_pulse2 = t_pulse1 + dt
            
            # Attenuation for second pulse
            sig2 = 0.6 * generate_pulse(t, t_pulse2) + 0.02 * np.random.normal(size=len(t)) # Add noise
            sig1 += 0.02 * np.random.normal(size=len(t))
            
            st.subheader("Ecrã do Osciloscópio")
            # Controls for Oscilloscope View
            view_range_ms = st.slider("Base de Tempo (Janela de visualização em ms)", 10.0, 100.0, 60.0)
            
            fig = plot_oscilloscope(t, sig1, sig2, (0, view_range_ms/1000))
            st.pyplot(fig)
            
            st.info(f"Dica: Cada divisão principal horizontal corresponde tipicamente a 1/10 da largura total, ou use a base de tempo. O pico verde ocorre em ~5ms.")
            
            st.markdown("---")
            st.subheader("Verificação da Medição")
            st.write(r"Meça a diferença de tempo $\Delta t$ entre o pico do sinal do emissor (verde) e o respetivo pico do sinal do recetor (amarelo) usando a grelha do ecrã do osciloscópio.")
            user_dt = st.number_input(r"Introduza o valor de $\Delta t$ medido (em ms):", min_value=0.0, max_value=200.0, value=0.0, step=0.1)
            
            # Use the actual generated time from the simulation for validation
            actual_dt_ms = st.session_state['measured_time_p1'] * 1000
            
            if st.button("Verificar Tempo"):
                margin_of_error = 0.5 # Allow +/- 0.5 ms tolerance
                
                if abs(user_dt - actual_dt_ms) <= margin_of_error:
                    st.success(f"Tempo Correto! O tempo de propagação aproximado é de **{actual_dt_ms:.1f} ms**.")
                else:
                    st.error("Tempo Incorreto. Verifique a leitura na grelha do osciloscópio. Dica: conte o número de divisões entre os dois picos e multiplique pelo valor de cada divisão (Base de Tempo / 10).")

            st.markdown("---")
            st.write(r"Com base no tempo medido ($\Delta t$) e na distância percorrida pelo som ao longo da mangueira ($d = 15.0$ m), calcule a velocidade de propagação do som.")
            user_v = st.number_input(r"Introduza o valor da velocidade calculada ($v$) em m/s:", min_value=0.0, max_value=1000.0, value=0.0, step=0.1)
            
            if st.button("Verificar Velocidade"):
                # Avoid division by zero
                if user_dt <= 0:
                    st.warning(r"Tem de ter um tempo $\Delta t$ válido (>0) na sua medição primeiro.")
                else:
                    # Calculate what the student should have gotten based on THEIR input
                    expected_v_based_on_user_dt = 15.0 / (user_dt / 1000.0)
                    
                    # Round both to 2 decimal places to compare (this checks 2 significant figures precision loosely as requested, or rather 2 decimal precision)
                    # We accept a small margin of error (e.g. 1.0 m/s) to cover rounding differences in intermediate steps
                    if abs(user_v - expected_v_based_on_user_dt) <= 1.0:
                        st.success(f"Velocidade Correta! Com o tempo de {user_dt} ms, a velocidade é de aproximadamente **{expected_v_based_on_user_dt:.1f} m/s**.")
                        
                        # Show bonus feedback on how close they are to theoretical
                        if abs(user_v - v_theo) <= 10.0:
                             st.balloons()
                             st.info(f"O seu valor experimental está muito próximo do valor teórico esperado para a temperatura atual ({v_theo:.1f} m/s)!")
                    else:
                        st.error(f"Velocidade Incorreta. Reveja os seus cálculos. Lembre-se que $v = \\frac{{d}}{{\\Delta t}}$ e que o tempo tem de estar em segundos.")

elif procedure == "2. Método do Desfasamento":
    st.header("Procedimento II: Método do Desfasamento")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        **Material:**
        - Gerador de Sinais e Altifalante
        - Microfone móvel
        - Régua/Calha ótica
        """)
        
        # Schematic for Procedure II
        st.graphviz_chart("""
        digraph G {
            rankdir=LR;
            node [shape=box, style=filled, fillcolor="#faebd7"];
            Gen [label="Gerador de Sinais\nFrequency f", fillcolor="#90ee90"];
            Speaker [label="Altifalante"];
            Mic [label="Microfone Móvel"];
            Osc [label="Osciloscópio", shape=component, fillcolor="#add8e6"];
            
            Gen -> Speaker [dir=both];
            Gen -> Osc [label="CH1 (Ref)"];
            Speaker -> Mic [label="Som (distância d)", style=dotted];
            Mic -> Osc [label="CH2 (Sinal)", color="orange"];
        }
        """)
        
        st.markdown("""
        **Instruções:**
        1. Defina a frequência do gerador.
        2. Mova o microfone afastando-o do altifalante.
        3. Observe o desfasamento entre o sinal da fonte (CH1) e do microfone (CH2).
        4. Registre o tempo de atraso ou distância para picos coincidentes.
        """)
        
        freq = st.slider("Frequência do Gerador (Hz)", 500, 3000, 1500, step=100)
        dist = st.slider("Distância Microfone-Altifalante (m)", 0.0, 1.5, 0.0, step=0.01)
        
        wavelength = v_theo / freq
        # Theoretical Delay
        delay_theo = dist / v_theo
        
    with col2:
        st.subheader("Montagem Experimental")
        
        # Calculate visual position (1.5m max range mapped to ~500px width)
        # Scale: 0m -> 100px (start), 1.5m -> 550px
        scale_factor = 300 # pixels per meter
        mic_x_pos = 100 + (dist * scale_factor)
        
        # Interactive SVG for Procedure II
        proc2_html = f"""
        <div style="display: flex; justify-content: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 1px solid #ddd;">
            <style>
                @keyframes speakerPulse {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.05); }}
                    100% {{ transform: scale(1); }}
                }}
                @keyframes waveMove {{
                    0% {{ opacity: 0.8; transform: translateX(0) scale(0.5); }}
                    100% {{ opacity: 0; transform: translateX(200px) scale(2); }}
                }}
                .speaker-icon {{
                    fill: #333;
                    animation: speakerPulse 1s infinite;
                }}
                .mic-icon {{
                    fill: #d32f2f;
                    transition: transform 0.2s ease-out;
                }}
                .wave {{
                    fill: none; stroke: #888; stroke-width: 2;
                    opacity: 0;
                    transform-origin: 80px 75px;
                    animation: waveMove 1s linear infinite;
                }}
            </style>
            <svg width="600" height="150" style="overflow: visible;">
                <!-- Ruler / Rail -->
                <line x1="100" y1="120" x2="550" y2="120" stroke="#555" stroke-width="2" />
                <text x="100" y="140" text-anchor="middle" font-size="12">0 m</text>
                <text x="550" y="140" text-anchor="middle" font-size="12">1.5 m</text>
                
                <!-- Fixed Speaker (at x=80) -->
                <g transform="translate(50, 50)">
                    <!-- Box -->
                    <rect x="0" y="0" width="40" height="50" fill="#444" rx="2" />
                    <!-- Cone -->
                    <path d="M 40 10 L 60 0 L 60 50 L 40 40 Z" fill="#666" />
                    <!-- Sound Waves emitting -->
                    <circle cx="60" cy="25" r="10" class="wave" style="animation-delay: 0s;" />
                    <circle cx="60" cy="25" r="10" class="wave" style="animation-delay: 0.3s;" />
                    <circle cx="60" cy="25" r="10" class="wave" style="animation-delay: 0.6s;" />
                </g>
                
                <!-- Movable Microphone -->
                <g transform="translate({mic_x_pos}, 60)">
                    <!-- Stand -->
                    <line x1="0" y1="0" x2="0" y2="60" stroke="#888" stroke-width="3" />
                    <circle cx="0" cy="60" r="5" fill="#333" />
                    <!-- Mic Head -->
                    <g transform="rotate(-90)">
                         <path d="M -10 -15 L 10 -15 L 10 5 L 5 10 L -5 10 L -10 5 Z" fill="#d32f2f" />
                         <circle cx="0" cy="-15" r="10" fill="#a00" />
                    </g>
                    <!-- Label -->
                    <text x="0" y="-35" text-anchor="middle" fill="#d32f2f" font-weight="bold" font-size="12">Mic</text>
                    <text x="0" y="-50" text-anchor="middle" fill="#333" font-size="10">{dist:.2f} m</text>
                </g>
            </svg>
        </div>
        """
        st.components.v1.html(proc2_html, height=180)
        
        st.subheader("Ecrã do Osciloscópio")
        
        # Simulation
        t_window = 5 / freq # Show 5 periods approx
        if t_window < 0.002: t_window = 0.002
        
        t = np.linspace(0, t_window, 1000)
        omega = 2 * np.pi * freq
        
        # Signal 1: Source
        sig1 = np.sin(omega * t)
        
        # Signal 2: Mic (Delayed by dist/v)
        # Add noise
        sig2 = 0.8 * np.sin(omega * (t - delay_theo)) + 0.05 * np.random.normal(size=len(t))
        
        fig = plot_oscilloscope(t, sig1, sig2, (0, t_window), y_range=(-1.5, 1.5))
        st.pyplot(fig)
        
        st.metric("Atraso Calculado (Simulação)", f"{delay_theo*1000:.3f} ms")
        st.markdown(rf"Desfasamento de fase: $\Delta \phi = {(dist/wavelength * 360) % 360:.1f}^\circ$")

elif procedure == "3. Análise de Dados":
    st.header("Registo e Análise de Dados")
    
    tab1, tab2 = st.tabs(["Dados Procedimento I", "Dados Procedimento II"])
    
    with tab1:
        st.subheader("Cálculo da Velocidade (Impulso)")
        d_p1 = st.number_input("Distância percorrida (m)", value=15.0)
        dt_p1_ms = st.number_input(r"Intervalo de tempo medido $\Delta t$ (ms)", value=0.0, step=0.1)
        
        if dt_p1_ms > 0:
            v_exp_p1 = d_p1 / (dt_p1_ms / 1000.0)
            st.success(f"Velocidade Experimental: **{v_exp_p1:.2f} m/s**")
            
            error_p1 = abs(v_exp_p1 - v_theo) / v_theo * 100
            st.info(f"Erro Percentual (vs Teórico {v_theo:.2f} m/s): **{error_p1:.2f}%**")
    
    with tab2:
        st.subheader("Tabela de Medições (Desfasamento)")
        
        if 'df_p2' not in st.session_state:
            st.session_state.df_p2 = pd.DataFrame(columns=["Distância (m)", "Tempo atraso (ms)"])
        
        col_input1, col_input2, col_btn = st.columns(3)
        with col_input1:
            d_in = st.number_input("Distância d (m)", key="d_in")
        with col_input2:
            t_in = st.number_input("Tempo atraso (ms)", key="t_in")
        with col_btn:
            st.text("")
            st.text("")
            if st.button("Adicionar Ponto"):
                new_row = pd.DataFrame({"Distância (m)": [d_in], "Tempo atraso (ms)": [t_in]})
                st.session_state.df_p2 = pd.concat([st.session_state.df_p2, new_row], ignore_index=True)
        
        # Use data_editor to allow adding/editing rows directly
        edited_df = st.data_editor(st.session_state.df_p2, num_rows="dynamic", key="data_editor_p2")
        
        # Update session state with edits (optional, but good for persistence across reruns if needed)
        st.session_state.df_p2 = edited_df
        
        if not edited_df.empty and len(edited_df) > 1:
            # Linear Regression
            # Ensure data is numeric
            try:
                X = edited_df["Tempo atraso (ms)"].astype(float) / 1000.0 
                y = edited_df["Distância (m)"].astype(float)
                
                # Simple linear fit y = v * x + b
                coef = np.polyfit(X, y, 1) # [slope, intercept]
                v_exp_p2 = coef[0]
                
                st.markdown(f"**Declive da reta (Velocidade):** {v_exp_p2:.2f} m/s")
                
                # Plot
                fig_reg, ax_reg = plt.subplots(figsize=(6, 4))
                ax_reg.scatter(X, y, color='red', label='Dados')
                ax_reg.plot(X, coef[0]*X + coef[1], color='blue', label=f'Ajuste Linear ($v={v_exp_p2:.1f}$ m/s)')
                ax_reg.set_xlabel("Tempo (s)")
                ax_reg.set_ylabel("Distância (m)")
                ax_reg.legend()
                ax_reg.grid(True, linestyle='--', alpha=0.7)
                st.pyplot(fig_reg)
                
                error_p2 = abs(v_exp_p2 - v_theo) / v_theo * 100
                st.info(f"Erro Percentual: **{error_p2:.2f}%**")
            except Exception as e:
                st.warning(f"Insira dados numéricos válidos para calcular. Erro: {e}")

