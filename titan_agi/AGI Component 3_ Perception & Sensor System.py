"""
TITAN AGI - PERCEPTION & SENSOR SYSTEM
Add this to backend/modules/agi_brain_03.py
"""

import numpy as np
import json
from collections import deque
from datetime import datetime
import hashlib

class VisionProcessor:
    """Computer Vision - Image Understanding"""
    def __init__(self):
        self.image_memory = deque(maxlen=100)
        self.object_database = {}
        self.scene_history = []
    
    def process_image(self, image_data):
        """
        Simulate image processing
        In production: use OpenCV, PIL, or ML models
        """
        # Convert to numpy array (simulated)
        if isinstance(image_data, str):
            # Hash-based simulation of image
            img_hash = hashlib.md5(image_data.encode()).hexdigest()
            img_array = np.random.rand(224, 224, 3)  # Simulated image tensor
        else:
            img_array = np.array(image_data)
            img_hash = hashlib.md5(img_array.tobytes()).hexdigest()
        
        # Store in memory
        self.image_memory.append({
            'hash': img_hash,
            'timestamp': datetime.now().isoformat(),
            'shape': img_array.shape
        })
        
        return img_hash, img_array
    
    def detect_edges(self, img_array):
        """Simplified edge detection (Sobel-like)"""
        # Horizontal and vertical gradients
        gx = np.diff(img_array, axis=1)
        gy = np.diff(img_array, axis=0)
        
        # Magnitude
        edges = np.sqrt(gx[:-1, :]**2 + gy[:, :-1]**2)
        edge_density = np.mean(edges)
        
        return {
            'edge_density': float(edge_density),
            'high_contrast': edge_density > 0.5
        }
    
    def detect_objects(self, img_array):
        """Simplified object detection"""
        # Simulate detecting objects via brightness regions
        brightness = np.mean(img_array, axis=2)
        
        # Find bright regions (simple thresholding)
        threshold = np.mean(brightness)
        objects = brightness > threshold
        
        # Count connected components (simplified)
        num_objects = int(np.sum(objects) / 100)  # rough estimate
        
        return {
            'objects_detected': max(1, num_objects),
            'brightness': float(np.mean(brightness)),
            'scene_complexity': float(np.std(brightness))
        }
    
    def recognize_scene(self, img_array):
        """Scene classification"""
        # Feature extraction (simplified)
        avg_color = np.mean(img_array, axis=(0, 1))
        texture = np.std(img_array)
        
        # Rough classification
        scene_type = "unknown"
        if avg_color[2] > 0.6:  # Blue dominant
            scene_type = "sky/water"
        elif avg_color[1] > 0.6:  # Green dominant
            scene_type = "nature"
        elif texture < 0.2:
            scene_type = "indoor"
        else:
            scene_type = "urban"
        
        scene = {
            'type': scene_type,
            'dominant_color': avg_color.tolist(),
            'texture_complexity': float(texture)
        }
        
        self.scene_history.append(scene)
        return scene
    
    def analyze(self, image_data):
        """Full vision pipeline"""
        img_hash, img_array = self.process_image(image_data)
        
        edges = self.detect_edges(img_array)
        objects = self.detect_objects(img_array)
        scene = self.recognize_scene(img_array)
        
        return {
            'image_id': img_hash,
            'edges': edges,
            'objects': objects,
            'scene': scene,
            'processed': True
        }

class AudioProcessor:
    """Audio Understanding - Speech & Sound"""
    def __init__(self):
        self.audio_buffer = deque(maxlen=50)
        self.known_patterns = {}
    
    def process_audio(self, audio_data):
        """
        Simulate audio processing
        In production: use librosa, speech_recognition, etc.
        """
        # Simulate audio features
        if isinstance(audio_data, str):
            audio_hash = hashlib.md5(audio_data.encode()).hexdigest()
            waveform = np.random.randn(16000)  # 1 second at 16kHz
        else:
            waveform = np.array(audio_data)
            audio_hash = hashlib.md5(waveform.tobytes()).hexdigest()
        
        self.audio_buffer.append({
            'hash': audio_hash,
            'timestamp': datetime.now().isoformat(),
            'duration': len(waveform) / 16000
        })
        
        return audio_hash, waveform
    
    def extract_features(self, waveform):
        """Extract audio features"""
        # Time domain features
        energy = np.sum(waveform**2)
        zero_crossings = np.sum(np.diff(np.sign(waveform)) != 0)
        
        # Frequency domain (simplified FFT)
        fft = np.fft.fft(waveform)
        magnitude = np.abs(fft[:len(fft)//2])
        
        dominant_freq = np.argmax(magnitude)
        spectral_centroid = np.sum(magnitude * np.arange(len(magnitude))) / np.sum(magnitude)
        
        return {
            'energy': float(energy),
            'zero_crossings': int(zero_crossings),
            'dominant_frequency': int(dominant_freq),
            'spectral_centroid': float(spectral_centroid)
        }
    
    def classify_sound(self, features):
        """Classify type of sound"""
        # Simple heuristic classification
        if features['energy'] > 1000:
            sound_type = "loud_noise"
        elif features['zero_crossings'] > 500:
            sound_type = "speech"
        elif features['dominant_frequency'] < 200:
            sound_type = "low_rumble"
        elif features['dominant_frequency'] > 2000:
            sound_type = "high_pitch"
        else:
            sound_type = "ambient"
        
        return {
            'type': sound_type,
            'confidence': 0.7,
            'features': features
        }
    
    def speech_to_text(self, waveform):
        """Simplified speech recognition"""
        # In production: use Whisper, Google Speech API, etc.
        features = self.extract_features(waveform)
        
        # Simulate transcription
        if features['zero_crossings'] > 300:
            return {
                'transcribed': True,
                'text': "[SPEECH_DETECTED]",
                'confidence': 0.85,
                'language': 'en'
            }
        
        return {'transcribed': False, 'text': None}
    
    def analyze(self, audio_data):
        """Full audio pipeline"""
        audio_hash, waveform = self.process_audio(audio_data)
        
        features = self.extract_features(waveform)
        classification = self.classify_sound(features)
        speech = self.speech_to_text(waveform)
        
        return {
            'audio_id': audio_hash,
            'features': features,
            'classification': classification,
            'speech': speech,
            'processed': True
        }

class SensorFusion:
    """Combine multiple sensor inputs"""
    def __init__(self):
        self.sensor_data = {
            'vision': [],
            'audio': [],
            'tactile': [],
            'temporal': []
        }
        self.world_model = {}
    
    def add_sensor_input(self, sensor_type, data):
        """Register new sensor reading"""
        if sensor_type in self.sensor_data:
            self.sensor_data[sensor_type].append({
                'timestamp': datetime.now().isoformat(),
                'data': data
            })
            
            # Keep only recent data
            if len(self.sensor_data[sensor_type]) > 100:
                self.sensor_data[sensor_type].pop(0)
    
    def fuse_perception(self):
        """Combine all sensors into unified world model"""
        # Get latest from each sensor
        latest = {}
        for sensor_type, readings in self.sensor_data.items():
            if readings:
                latest[sensor_type] = readings[-1]['data']
        
        # Build world model
        self.world_model = {
            'timestamp': datetime.now().isoformat(),
            'sensors_active': len(latest),
            'perception': latest,
            'confidence': len(latest) / len(self.sensor_data)
        }
        
        return self.world_model
    
    def detect_anomalies(self):
        """Find unusual patterns across sensors"""
        anomalies = []
        
        # Check for contradictions
        if 'vision' in self.sensor_data and 'audio' in self.sensor_data:
            vision = self.sensor_data['vision']
            audio = self.sensor_data['audio']
            
            if len(vision) > 0 and len(audio) > 0:
                # Example: bright scene but no sound = anomaly
                latest_vision = vision[-1]['data']
                latest_audio = audio[-1]['data']
                
                if latest_vision.get('bright') and latest_audio.get('silent'):
                    anomalies.append({
                        'type': 'sensory_mismatch',
                        'description': 'bright scene but silent'
                    })
        
        return anomalies

class PerceptionService:
    """Main AGI Perception Service"""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.vision = VisionProcessor()
        self.audio = AudioProcessor()
        self.fusion = SensorFusion()
        self.perceptions_processed = 0
    
    def perceive_visual(self, image_data):
        """Process visual input"""
        result = self.vision.analyze(image_data)
        self.fusion.add_sensor_input('vision', result)
        self.perceptions_processed += 1
        return result
    
    def perceive_audio(self, audio_data):
        """Process audio input"""
        result = self.audio.analyze(audio_data)
        self.fusion.add_sensor_input('audio', result)
        self.perceptions_processed += 1
        return result
    
    def perceive_world(self):
        """Get unified perception of environment"""
        world_model = self.fusion.fuse_perception()
        anomalies = self.fusion.detect_anomalies()
        
        return {
            'world_model': world_model,
            'anomalies': anomalies,
            'timestamp': datetime.now().isoformat()
        }
    
    def execute(self):
        """Service interface for Titan swarm"""
        return {
            "id": self.id,
            "module": self.name,
            "status": "PERCEIVING",
            "perceptions_processed": self.perceptions_processed,
            "images_in_memory": len(self.vision.image_memory),
            "audio_in_memory": len(self.audio.audio_buffer),
            "active_sensors": len([k for k, v in self.fusion.sensor_data.items() if v]),
            "world_model_confidence": self.fusion.world_model.get('confidence', 0.0),
            "active": True
        }

# Example usage
if __name__ == "__main__":
    brain = PerceptionService("AGI_BRAIN_03", "Perception Engine")
    
    # Test vision
    vision_result = brain.perceive_visual("test_image_data_001")
    print(f"Vision: {vision_result}")
    
    # Test audio
    audio_result = brain.perceive_audio("test_audio_data_001")
    print(f"\nAudio: {audio_result}")
    
    # Test world model
    world = brain.perceive_world()
    print(f"\nWorld Model: {world}")
    
    # Status
    print(f"\nStatus: {brain.execute()}")