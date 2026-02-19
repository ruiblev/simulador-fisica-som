# Simulador: Velocidade do Som (A.L. 2.2)

Este projeto é uma simulação interativa da Atividade Laboratorial de Física 2.2 (11º ano) para determinar a velocidade de propagação do som no ar.

## Funcionalidades
- **Configuração Ambiental**: Definição da temperatura e cálculo da velocidade teórica.
- **Procedimento I (Método do Impulso)**: Simulação de propagação de som em mangueira de 15m com osciloscópio.
- **Procedimento II (Método do Desfasamento)**: Simulação de ondas com desfasamento por distância variável.
- **Análise de Dados**: Tabelas interativas e regressão linear automática.

## Como Executar (O mais fácil)

Para facilitar o uso pelos alunos, basta descarregar a pasta e executar o script correspondente ao sistema operativo:

- **Windows**: Duplo clique no ficheiro `run_windows.bat`
- **Mac ou Linux**: Executar o ficheiro `run_mac_linux.sh` (ou via terminal: `bash run_mac_linux.sh`)

Estes scripts irão criar automaticamente o ambiente necessário e iniciar o simulador.

---

## Execução Manual (Alternativa)

1. Certifique-se de ter Python 3 instalado.
2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação Streamlit:
   ```bash
   streamlit run app.py
   ```

## Requisitos
- Python 3.8+
- Bibliotecas listadas em `requirements.txt`
