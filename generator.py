"""Générateur de vidéos publicitaires RedPill IA"""

import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import imageio
import numpy as np
from pathlib import Path
import time
import importlib
import sys

from config import *


class VideoGenerator:
    def __init__(self):
        """Initialise le générateur"""
        self.device = self._get_device()
        self.pipe = None
        print(f"🖥️  Device: {self.device}")
    
    def _get_device(self):
        """Détecte le meilleur device disponible"""
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        return "cpu"
    
    def load_model(self):
        """Charge le modèle text-to-video"""
        print(f"\n📦 Chargement du modèle {MODEL_NAME}...")
        print("⏳ Cela peut prendre 2-3 minutes...")
        
        self.pipe = DiffusionPipeline.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16
        )
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        self.pipe = self.pipe.to(self.device)
        
        print("✅ Modèle chargé\n")
    
    def generate_scene(self, prompt, num_frames, scene_num, total_scenes):
        """Génère une scène"""
        print(f"\n{'='*60}")
        print(f"🎬 SCÈNE {scene_num}/{total_scenes}")
        print(f"📝 Prompt: {prompt[:60]}...")
        print(f"🎞️  Frames: {num_frames} ({num_frames/FPS:.1f}s)")
        print(f"⏳ Génération en cours (30-45 min)...")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        video_frames = self.pipe(
            prompt,
            num_frames=num_frames,
            num_inference_steps=NUM_INFERENCE_STEPS
        ).frames[0]
        
        elapsed = time.time() - start_time
        print(f"✅ Scène terminée en {elapsed/60:.1f} minutes")
        
        return video_frames
    
    def generate_video(self, pub_number):
        """Génère une vidéo complète depuis un fichier de prompts"""
        
        # Charger le fichier de prompts
        try:
            pub_module = importlib.import_module(f"prompts.pub_{pub_number}")
            scenes = pub_module.SCENES
            video_name = pub_module.VIDEO_NAME
        except ImportError:
            print(f"❌ Fichier prompts/pub_{pub_number}.py introuvable")
            return
        
        print(f"\n{'='*60}")
        print(f"🎥 GÉNÉRATION PUB #{pub_number}")
        print(f"📹 Sortie: {video_name}")
        print(f"🎬 {len(scenes)} scènes")
        print(f"{'='*60}")
        
        # Charger modèle si nécessaire
        if self.pipe is None:
            self.load_model()
        
        all_frames = []
        
        # Générer chaque scène
        for i, scene in enumerate(scenes, 1):
            frames = self.generate_scene(
                scene["prompt"],
                scene["frames"],
                i,
                len(scenes)
            )
            all_frames.extend(frames)
            
            # Pause entre scènes (sauf dernière)
            if i < len(scenes):
                print(f"\n💤 Pause {PAUSE_BETWEEN_SCENES/60:.0f} min (refroidissement)...")
                time.sleep(PAUSE_BETWEEN_SCENES)
        
        # Assembler et sauvegarder
        print(f"\n📹 Assemblage final...")
        output_path = Path(OUTPUT_DIR) / video_name
        output_path.parent.mkdir(exist_ok=True)
        
        frames_array = [np.array(frame) for frame in all_frames]
        imageio.mimsave(str(output_path), frames_array, fps=FPS)
        
        duration = len(all_frames) / FPS
        print(f"\n{'='*60}")
        print(f"✅ TERMINÉ !")
        print(f"📁 Fichier: {output_path}")
        print(f"⏱️  Durée: {duration:.1f}s")
        print(f"🎞️  Frames: {len(all_frames)}")
        print(f"{'='*60}\n")


def main():
    """Point d'entrée principal"""
    
    if len(sys.argv) < 2:
        print("Usage: python generator.py <numero_pub>")
        print("Exemple: python generator.py 1")
        sys.exit(1)
    
    pub_number = sys.argv[1]
    
    generator = VideoGenerator()
    generator.generate_video(pub_number)


if __name__ == "__main__":
    main()