import py5
import pandas as pd
import numpy as np

# --- VARIÁVEIS DE CONTROLE ---
df = None
current_frame = 0
cam_dist = 3000 # Aumentei um pouco o zoom out inicial
cam_lat = py5.PI/4
cam_lon = 0

def setup():
    global df
    # Definindo tamanho e permitindo maximizar
    py5.size(1280, 720, py5.P3D)
    py5.window_resizable(True)
    
    # Ativando cores HSB (Hue, Saturation, Brightness)
    py5.color_mode(py5.HSB, 255)
    
    try:
        # Carregando o dataset de alta fidelidade
        df = pd.read_parquet("harpia_enriched_telemetry.parquet")
        print(f"✅ Sistema Harpia Carregado: {len(df)} frames.")
    except Exception as e:
        print(f"❌ Erro ao carregar telemetria: {e}")
        print("Certifique-se de rodar o simulador primeiro.")
        py5.exit_sketch()

def draw():
    global current_frame, cam_dist, cam_lat, cam_lon
    if df is None: return
    
    py5.background(5) # Espaço Profundo (quase preto)
    
    # --- CÂMERA DINÂMICA ADAPTATIVA ---
    py5.translate(py5.width/2, py5.height/2, -cam_dist)
    py5.rotate_x(cam_lat)
    py5.rotate_z(cam_lon)
    
    row = df.iloc[current_frame]
    
    # 1. O SOL (Pulsação SPHY)
    sun_size = row['sun_resonance']
    py5.push_matrix()
    py5.no_stroke()
    for i in range(3): # Glow em camadas
        py5.fill(30, 150, 255, 60 - (i*20))
        py5.sphere(sun_size + (i*12))
    py5.pop_matrix()

    # 2. CINTURÃO DE ASTEROIDES (400 Corpos)
    py5.stroke(160, 50, 200, 180) # Roxo translúcido
    py5.stroke_weight(2)
    py5.begin_shape(py5.POINTS)
    for i in range(400):
        py5.vertex(row[f'b_{i}_x'], row[f'b_{i}_y'], row[f'b_{i}_z'])
    py5.end_shape()

    # 3. PLANETAS E ANÉIS (AQUI ESTÁ A MUDANÇA!)
    planet_names = ["Mercúrio", "Vênus", "Terra", "Marte", "Ceres", "Júpiter", "Saturno", "Urano", "Netuno", "Plutão"]
    for p_name in planet_names:
        px, py, pz = row[f'p_{p_name}_x'], row[f'p_{p_name}_y'], row[f'p_{p_name}_z']
        hue = row[f'p_{p_name}_hue']
        size = row[f'p_{p_name}_size']
        
        py5.push_matrix()
        # Primeiro movemos para a posição orbital
        py5.translate(px, py, pz)
        
        # --- LÓGICA DE INCLINAÇÃO AXIAL (REBELDIAS SPHY) ---
        if p_name == "Saturno":
            # Inclinação Axial Extrema (quase 90º)
            # Rotacionamos o próprio planeta e seus anéis
            py5.rotate_x(py5.HALF_PI) # Deita o sistema de anéis
            py5.rotate_y(py5.frame_count * 0.005) # Rotação própria lenta
        elif p_name == "Urano":
            # Urano também é rebelde (roda de lado, ~98º)
            py5.rotate_x(py5.PI * 0.55)
        else:
            # Inclinação padrão leve para os outros
            py5.rotate_x(0.1) 
            
        # Desenhar o Corpo do Planeta
        py5.no_stroke()
        py5.fill(hue, 150, 255)
        py5.sphere(size)
        
        # Desenhar Anéis (se existirem no status)
        ring_key = f'p_{p_name}_ring_status'
        if ring_key in row:
            draw_rings(size, hue, row[ring_key], p_name)
            
        py5.pop_matrix()

    # 4. LUAS (Mantendo a coerência de fase)
    moon_names = ["Lua", "Fobos", "Deimos", "Io", "Europa", "Ganimedes", "Calisto", "Titan", "Titânia", "Tritão", "Caronte"]
    for m_name in moon_names:
        mx, my, mz = row[f'm_{m_name}_x'], row[f'm_{m_name}_y'], row[f'm_{m_name}_z']
        hue = row[f'm_{m_name}_hue']
        size = row[f'm_{m_name}_size']
        
        py5.push_matrix()
        py5.translate(mx, my, mz)
        py5.no_stroke()
        py5.fill(hue, 50, 255) # Luas mais pálidas
        py5.sphere(size)
        py5.pop_matrix()

    draw_hud(current_frame, cam_dist)
    
    # Avanço de Frame
    current_frame = (current_frame + 1) % len(df)

def draw_rings(p_size, hue, status, p_name):
    # Desabilitando o Depth Test temporariamente para os anéis
    # ficarem bonitos e translúcidos sem bug visual
    py5.hint(py5.DISABLE_DEPTH_TEST) 
    py5.no_fill()
    
    # Cores e estilos diferentes para anéis rebeldes
    if p_name == "Saturno":
        py5.stroke(hue, 100, 200, 150) # Dourado mais forte
        py5.stroke_weight(2)
        count = 6
    else:
        py5.stroke(hue, 80, 150, 80) # Anéis de gelo mais sutis
        py5.stroke_weight(1)
        count = 3
        
    for r in range(count):
        # O raio é afetado pela pulsação SPHY (status)
        r_dist = p_size * (1.6 + r*0.4) * status
        py5.ellipse(0, 0, r_dist*2, r_dist*2)
        
    py5.hint(py5.ENABLE_DEPTH_TEST)

def draw_hud(f, dist):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.camera() # Reseta a matriz para 2D (HUD fixo)
    py5.no_lights()
    
    # Caixa de Fundo do HUD
    py5.fill(0, 150) # Preto translúcido
    py5.no_stroke()
    py5.rect(20, 20, 480, 70, 8)
    
    # Texto
    py5.fill(255) # Branco
    py5.text_align(py5.LEFT, py5.CENTER)
    py5.text(f"HARPIA OS - SPHY REBEL SYSTEM | FRAME: {f} | ZOOM: {dist:.0f}", 40, 45)
    py5.text("CONTROLES: F: MAXIMIZAR | MOUSE DIR: GIRAR | SCROLL: ZOOM", 40, 65)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

# --- SISTEMA DE NAVEGAÇÃO INTERATIVA ---

def mouse_wheel(event):
    global cam_dist
    cam_dist += event.get_count() * 120
    # Impede que a câmera entre dentro do sol ou fuja do sistema
    cam_dist = py5.constrain(cam_dist, 300, 12000)

def mouse_dragged():
    global cam_lat, cam_lon
    if py5.mouse_button == py5.RIGHT:
        # Rotação suave baseada no arraste do mouse
        cam_lon += (py5.mouse_x - py5.pmouse_x) * 0.01
        cam_lat -= (py5.mouse_y - py5.pmouse_y) * 0.01
        # Trava a latitude para não dar cambalhota na câmera
        cam_lat = py5.constrain(cam_lat, 0.01, py5.HALF_PI * 0.98)

def key_pressed():
    if py5.key.lower() == 'f':
        # Alterna entre Janela e Tela Cheia (Maximizar)
        py5.set_full_screen(not py5.is_full_screen())

if __name__ == "__main__":
    # Rodando o Sketch
    py5.run_sketch()
