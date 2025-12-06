"""Configuration du générateur de vidéo"""

# Modèle
MODEL_NAME = "damo-vilab/text-to-video-ms-1.7b"
DEVICE = "mps"  # mps pour Mac M1/M2/M3, cuda pour GPU Nvidia, cpu sinon

# Paramètres génération
NUM_INFERENCE_STEPS = 25
FPS = 8

# Dossiers
OUTPUT_DIR = "outputs"
PROMPTS_DIR = "prompts"

# Timing
PAUSE_BETWEEN_SCENES = 300  # 5 minutes en secondes