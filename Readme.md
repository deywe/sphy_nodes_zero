# Harpia OS - Sphy Nodes Zero
### Auditor de Fase e Telemetria Orbital Enriquecida
"A estabilidade do sistema é alcançada através da aplicação de um Tensor de Fase Quântica ($\mathcal{T}_{\phi}$). Este operador mapeia as flutuações gravitacionais em um domínio de frequência coerente, onde a instabilidade de Poincaré é neutralizada pela simetria da Proporção Áurea ($\phi$), transformando o caos dinâmico em uma série temporal determinística."

Este repositório contém o ecossistema de simulação para a teoria de **Propulsão por Tencionamento Geométrico**. O sistema utiliza o motor **SPHY (Sovereign Phase Harmony)** para resolver o movimento de n-corpos através de ressonância harmônica, eliminando o caos clássico.

## 🚀 A Solução do Enigma de Poincaré
Na mecânica clássica, o problema dos três corpos é insolúvel de forma determinística geral devido à sensibilidade às condições iniciais (Caos de Poincaré). O Harpia OS contorna essa limitação ao tratar a gravidade não como força, mas como **Condutância de Fase**.

A "resolução" operacional aplicada neste simulador redefine a estabilidade orbital através do Kernel de Fase:

$$\Omega_{stab} = \lim_{\Phi_D \to 1} \oint (\hat{\mathcal{Q}} \cdot \Psi_{res}) d\tau = 0$$

Onde o operador $\hat{\mathcal{Q}}$ atua como um filtro de ruído geométrico, forçando os corpos a ocuparem nós de ressonância baseados na proporção áurea ($\phi$), impedindo a divergência caótica exponencial.

---

## 📊 Dataset: `harpia_enriched_telemetry.parquet`
O arquivo de telemetria é gerado em formato **Apache Parquet**, otimizado para alta performance e baixa latência. Ele contém a "verdade matemática" de cada frame da simulação.

* **Corpos Celestes:** 10 planetas (incluindo Ceres e Plutão) e 11 luas principais.
* **Cinturão de Asteroides:** Matriz vetorial com 400 objetos individuais processados em tempo real.
* **Variáveis por Frame:** Coordenadas $(x, y, z)$, estados de ressonância solar, status de anéis e metadados visuais (Hues e Sizes).

---

## 🖥️ Visualizador: Harpia Auditor v2.1
O visualizador foi desenvolvido em **py5** (Processing para Python) para atuar como uma interface de auditoria dos dados do Parquet.

### Funcionalidades:
* **Trail Rendering:** Rastros dinâmicos que mostram a história da fase de cada corpo.
* **Asteroid Cloud:** Renderização de 400 partículas representando o cinturão de asteroides.
* **Navegação 3D:** Controle total de câmera (Orbital e Zoom).
* **Sincronia de HSB:** Cores baseadas na frequência de ressonância de cada nó.

### Como Executar:
1. Instale as dependências:
   ```bash
   pip install py5 pandas pyarrow
   ```
2. Certifique-se de que o arquivo `harpia_enriched_telemetry.parquet` esteja na mesma pasta.
3. Execute o script:
   ```bash
   python sphy_solar7_visualyzer.py
   ```

### Controles:
* **ESPAÇO:** Pausa/Retoma a linha do tempo.
* **Botão Direito do Mouse:** Rotaciona a câmera.
* **Scroll do Mouse:** Zoom in/out.

---

## 📝 Citação e Referência
Este trabalho faz parte da formalização matemática:
**"Propulsão por Tencionamento Geométrico e Singularidades de Massa Zero"**
*Autor: Deywe Okabe - IA Simbiótica (Harpia OS / SEFLP)*

