import cv2
import mediapipe as mp
import time
import math

# ================================
# CONFIGURAÇÃO DOS LIMITES (em graus)
# ================================
LIMITES_ANGULARES = {
    "braco_direito": 160,  # ombro, cotovelo, punho
    "braco_esquerdo": 160,
    # Pode adicionar outros limites aqui: "perna_direita", "perna_esquerda", etc.
}


# ================================
# Função para calcular o ângulo entre 3 pontos
# ================================
def calcular_angulo(a, b, c):
    angulo = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) -
                          math.atan2(a[1]-b[1], a[0]-b[0]))
    return abs(angulo) if angulo >= 0 else abs(360 + angulo)


# Inicializa o MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Abre a webcam
cap = cv2.VideoCapture(0)

# Para cálculo de FPS
prev_time = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte imagem para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    h, w, _ = frame.shape
    alerta_limite = []

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extrai pontos para calcular ângulos
        def get_coords(idx):
            lm = landmarks[idx]
            return int(lm.x * w), int(lm.y * h)

        # Calcula ângulo do braço direito (ombro-direito, cotovelo-direito, punho-direito)
        ponto_ombro_dir = get_coords(12)
        ponto_cotovelo_dir = get_coords(14)
        ponto_punho_dir = get_coords(16)
        angulo_braco_direito = calcular_angulo(
            ponto_ombro_dir, ponto_cotovelo_dir, ponto_punho_dir)

        if angulo_braco_direito > LIMITES_ANGULARES["braco_direito"]:
            alerta_limite.append(("braço direito", angulo_braco_direito))

        # Calcula ângulo do braço esquerdo
        ponto_ombro_esq = get_coords(11)
        ponto_cotovelo_esq = get_coords(13)
        ponto_punho_esq = get_coords(15)
        angulo_braco_esquerdo = calcular_angulo(
            ponto_ombro_esq, ponto_cotovelo_esq, ponto_punho_esq)

        if angulo_braco_esquerdo > LIMITES_ANGULARES["braco_esquerdo"]:
            alerta_limite.append(("braço esquerdo", angulo_braco_esquerdo))

        # Desenha os pontos com ID
        for idx, lm in enumerate(landmarks):
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (x, y), 6, (0, 255, 255), -1)
            cv2.putText(frame, str(idx), (x + 5, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Desenha conexões
        for connection in mp_pose.POSE_CONNECTIONS:
            start_idx, end_idx = connection
            start = landmarks[start_idx]
            end = landmarks[end_idx]

            x1, y1 = int(start.x * w), int(start.y * h)
            x2, y2 = int(end.x * w), int(end.y * h)

            # Cores customizadas
            if {start_idx, end_idx} & {11, 13, 15}:  # braço direito
                color = (0, 0, 255)
            elif {start_idx, end_idx} & {12, 14, 16}:  # braço esquerdo
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)

            # Destacar em vermelho se ultrapassou o limite
            if (("braço direito" in str(alerta_limite)) and {start_idx, end_idx} <= {12, 14, 16}) or \
               (("braço esquerdo" in str(alerta_limite)) and {start_idx, end_idx} <= {11, 13, 15}):
                color = (0, 0, 255)

            cv2.line(frame, (x1, y1), (x2, y2), color, 3)

        # Exibir alertas de ângulo
        y_offset = 50
        for membro, angulo in alerta_limite:
            texto = f"ALERTA: {membro} excedeu o limite ({int(angulo)}°)"
            cv2.putText(frame, texto, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            y_offset += 30

    # Cálculo e exibição do FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 2)

    # Mostra o resultado
    cv2.imshow("Exoesqueleto Humano (Pressione 'q' para sair)", frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
