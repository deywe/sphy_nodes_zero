import py5
import pandas as pd
import numpy as np

# --- VARIÁVEIS DE CONTROLE ---
df = None
current_frame = 0
cam_dist = 3000 
cam_lat = py5.PI/4
cam_lon = 0

def setup():
    global df
    py5.size(1280, 720, py5.P3D)
    py5.window_resizable(True)
    py5.color_mode(py5.HSB, 255)
    
    try:
        df = pd.read_parquet("harpia_enriched_telemetry.parquet")
        print(f"✅ Sistema Harpia Carregado: {len(df)} frames.")
    except Exception as e:
        print(f"❌ Erro: Rode o simulador primeiro ou verifique o arquivo parquet.")
        py5.exit_sketch()

def draw():
    global current_frame, cam_dist, cam_lat, cam_lon
    if df is None: return
    
    py5.background(5) 
    
    # --- CÂMERA ---
    py5.translate(py5.width/2, py5.height/2, -cam_dist)
    py5.rotate_x(cam_lat)
    py5.rotate_z(cam_lon)
    
    row = df.iloc[current_frame]
    
    # 1. SOL
    sun_size = row['sun_resonance']
    py5.push_matrix()
    py5.no_stroke()
    for i in range(3):
        py5.fill(30, 150, 255, 60 - (i*20))
        py5.sphere(sun_size + (i*12))
    py5.pop_matrix()

    # 2. CINTURÃO DE ASTEROIDES
    py5.stroke(160, 50, 200, 180)
    py5.stroke_weight(2)
    py5.begin_shape(py5.POINTS)
    for i in range(400):
        py5.vertex(row[f'b_{i}_x'], row[f'b_{i}_y'], row[f'b_{i}_z'])
    py5.end_shape()

    # 3. PLANETAS E ANÉIS
    planet_names = ["Mercúrio", "Vênus", "Terra", "Marte", "Ceres", "Júpiter", "Saturno", "Urano", "Netuno", "Plutão"]
    for p_name in planet_names:
        px, py, pz = row[f'p_{p_name}_x'], row[f'p_{p_name}_y'], row[f'p_{p_name}_z']
        hue = row[f'p_{p_name}_hue']
        size = row[f'p_{p_name}_size']
        
        py5.push_matrix()
        py5.translate(px, py, pz)
        
        # --- LÓGICA DE INCLINAÇÃO ---
        if p_name == "Saturno":
            # ÚNICO REBELDE: Inclinação Axial de 90º (HALF_PI)
            py5.rotate_x(py5.HALF_PI) 
            py5.rotate_y(py5.frame_count * 0.005) 
        else:
            # Todos os outros seguem a inclinação padrão do plano orbital
            py5.rotate_x(0.1) 
            
        py5.no_stroke()
        py5.fill(hue, 150, 255)
        py5.sphere(size)
        
        # Desenhar Anéis se existirem no dataset
        ring_key = f'p_{p_name}_ring_status'
        if ring_key in row:
            draw_rings(size, hue, row[ring_key], p_name)
            
        py5.pop_matrix()

    # 4. LUAS
    moon_names = ["Lua", "Fobos", "Deimos", "Io", "Europa", "Ganimedes", "Calisto", "Titan", "Titânia", "Tritão", "Caronte"]
    for m_name in moon_names:
        mx, my, mz = row[f'm_{m_name}_x'], row[f'm_{m_name}_y'], row[f'm_{m_name}_z']
        hue = row[f'm_{m_name}_hue']
        size = row[f'm_{m_name}_size']
        
        py5.push_matrix()
        py5.translate(mx, my, mz)
        py5.no_stroke()
        py5.fill(hue, 50, 255)
        py5.sphere(size)
        py5.pop_matrix()

    draw_hud(current_frame, cam_dist)
    current_frame = (current_frame + 1) % len(df)

def draw_rings(p_size, hue, status, p_name):
    py5.hint(py5.DISABLE_DEPTH_TEST) 
    py5.no_fill()
    
    if p_name == "Saturno":
        py5.stroke(hue, 100, 200, 150)
        py5.stroke_weight(2)
        count = 6
    else:
        py5.stroke(hue, 80, 150, 80)
        py5.stroke_weight(1)
        count = 3
        
    for r in range(count):
        r_dist = p_size * (1.6 + r*0.4) * status
        py5.ellipse(0, 0, r_dist*2, r_dist*2)
        
    py5.hint(py5.ENABLE_DEPTH_TEST)

def draw_hud(f, dist):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.camera()
    py5.fill(0, 150)
    py5.no_stroke()
    py5.rect(20, 20, 480, 70, 8)
    py5.fill(255)
    py5.text(f"HARPIA OS - SPHY REBEL (SATURN 90º) | FRAME: {f}", 40, 45)
    py5.text("F: TELA CHEIA | MOUSE DIR: GIRAR | SCROLL: ZOOM", 40, 65)
    py5.hint(py5.ENABLE_DEPTH_TEST)

# --- NAVEGAÇÃO ---
def mouse_wheel(event):
    global cam_dist
    cam_dist += event.get_count() * 120
    cam_dist = py5.constrain(cam_dist, 300, 12000)

def mouse_dragged():
    global cam_lat, cam_lon
    if py5.mouse_button == py5.RIGHT:
        cam_lon += (py5.mouse_x - py5.pmouse_x) * 0.01
        cam_lat -= (py5.mouse_y - py5.pmouse_y) * 0.01
        cam_lat = py5.constrain(cam_lat, 0.01, py5.HALF_PI * 0.98)

def key_pressed():
    if py5.key.lower() == 'f':
        py5.set_full_screen(not py5.is_full_screen())

if __name__ == "__main__":
    py5.run_sketch()
