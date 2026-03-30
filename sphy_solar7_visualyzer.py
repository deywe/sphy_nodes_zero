import py5
import numpy as np
import pandas as pd
import sys
from collections import deque

# --- CONFIGURAÇÕES DO AUDITOR V2.1 ---
INPUT_PATH = "harpia_enriched_telemetry.parquet"
TRAIL_SIZE = 80  # Comprimento do rastro em frames

# Variáveis de Navegação
cam_dist, cam_lat, cam_lon = 1400, py5.PI/3.5, 0
current_frame = 0
total_frames = 0
telemetry_df = None
is_paused = False

# Dicionário de Rastros (Buffers de memória local)
trails = {}

def settings():
    py5.size(1280, 720, py5.P3D)

def setup():
    global telemetry_df, total_frames, planet_names, moon_names, asteroid_count, trails
    
    print(f"\n[Harpia Visualizer] Sincronizando com telemetria: {INPUT_PATH}...")
    try:
        telemetry_df = pd.read_parquet(INPUT_PATH)
        total_frames = len(telemetry_df)
        print(f"[OK] {total_frames} frames detectados.")
    except Exception as e:
        print(f"[!] Erro de leitura: {e}")
        sys.exit()

    cols = telemetry_df.columns
    # Identificação Dinâmica de Corpos e Asteroides
    planet_names = sorted(list(set([c.split('_')[1] for c in cols if c.startswith('p_') and c.endswith('_x')])))
    moon_names = sorted(list(set([c.split('_')[1] for c in cols if c.startswith('m_') and c.endswith('_x')])))
    asteroid_count = len([c for c in cols if c.startswith('b_') and c.endswith('_x')])
    
    # Inicializa buffers de rastro para Planetas e Luas
    for name in planet_names + moon_names:
        trails[name] = deque(maxlen=TRAIL_SIZE)

    py5.window_resizable(True)
    py5.window_title("Harpia Auditor v2.1 - Sovereign Phase Visualization")
    py5.color_mode(py5.HSB, 255)
    py5.text_size(14)

def draw():
    global current_frame, cam_dist, cam_lat, cam_lon, is_paused
    
    if telemetry_df is None: return
    
    py5.background(0)
    
    # HUD de Telemetria (Fixo na tela)
    draw_hud()

    # Espaço 3D
    py5.translate(py5.width/2, py5.height/2, -cam_dist)
    py5.rotate_x(cam_lat)
    py5.rotate_z(cam_lon)
    
    frame_data = telemetry_df.iloc[current_frame]
    
    # 1. O SOL (Fonte de Ressonância)
    draw_sun(frame_data['sun_resonance'])
    
    # 2. CINTURÃO DE ASTEROIDES (Nuvem Real)
    py5.stroke_weight(1.5)
    for i in range(asteroid_count):
        ax = frame_data[f'b_{i}_x']
        ay = frame_data[f'b_{i}_y']
        az = frame_data[f'b_{i}_z']
        py5.stroke(20, 50, 200, 150) # HSB: Cinza azulado para asteroides
        py5.point(ax, ay, az)
    py5.stroke_weight(1)

    # 3. PLANETAS E RASTROS
    for p in planet_names:
        pos = (frame_data[f'p_{p}_x'], frame_data[f'p_{p}_y'], frame_data[f'p_{p}_z'])
        hue = frame_data[f'p_{p}_hue']
        size = frame_data[f'p_{p}_size']
        
        trails[p].append(pos)
        draw_trail(p, hue)
        draw_node(pos, size, hue, p)
        
        if f'p_{p}_ring_status' in frame_data:
            draw_rings(pos, size * 2.4, hue, frame_data[f'p_{p}_ring_status'])

    # 4. LUAS
    for m in moon_names:
        pos = (frame_data[f'm_{m}_x'], frame_data[f'm_{m}_y'], frame_data[f'm_{m}_z'])
        hue = frame_data[f'm_{m}_hue']
        size = frame_data[f'm_{m}_size']
        
        trails[m].append(pos)
        draw_trail(m, hue)
        draw_node(pos, size, hue, m)

    if not is_paused:
        current_frame = (current_frame + 1) % total_frames

def draw_sun(size):
    py5.no_fill()
    py5.stroke(35, 200, 255, 120)
    py5.sphere(size)

def draw_trail(name, hue):
    if len(trails[name]) < 2: return
    py5.no_fill()
    py5.stroke(hue, 150, 255, 80)
    py5.begin_shape()
    for p in trails[name]:
        py5.vertex(p[0], p[1], p[2])
    py5.end_shape()

def draw_node(pos, size, hue, name):
    py5.push_matrix()
    py5.translate(pos[0], pos[1], pos[2])
    py5.fill(hue, 180, 255)
    py5.no_stroke()
    py5.sphere(size)
    py5.fill(255)
    py5.text(name, size + 5, 0)
    py5.pop_matrix()

def draw_rings(pos, base_size, hue, status):
    py5.push_matrix()
    py5.translate(pos[0], pos[1], pos[2])
    py5.rotate_x(py5.PI/2)
    py5.no_fill()
    py5.stroke(hue, 100, 255, 100)
    py5.ellipse(0, 0, base_size * status, base_size * status)
    py5.pop_matrix()

def draw_hud():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.push_matrix(); py5.reset_matrix()
    py5.fill(255)
    py5.text(f"AUDITOR HARPIA v2.1 | FRAME: {current_frame}/{total_frames}", 30, 40)
    py5.text(f"OBJETOS MONITORADOS: {len(planet_names) + len(moon_names)} + {asteroid_count} Asteroides", 30, 60)
    py5.text("ESPAÇO: PAUSAR | MOUSE DIR: ROTACIONAR | SCROLL: ZOOM", 30, 80)
    py5.pop_matrix(); py5.hint(py5.ENABLE_DEPTH_TEST)

def key_pressed():
    global is_paused
    if py5.key == ' ': is_paused = not is_paused

def mouse_wheel(event):
    global cam_dist
    cam_dist = py5.constrain(cam_dist + event.get_count() * 50, 100, 8000)

def mouse_dragged():
    global cam_lat, cam_lon
    if py5.mouse_button == py5.RIGHT:
        cam_lon += (py5.mouse_x - py5.pmouse_x) * 0.01
        cam_lat = py5.constrain(cam_lat - (py5.mouse_y - py5.pmouse_y) * 0.01, 0.05, py5.HALF_PI * 0.98)

if __name__ == "__main__":
    py5.run_sketch()
