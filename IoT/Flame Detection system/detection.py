"""
Fire Detection System - Laptop Application
Receives alerts via USB/Serial from Arduino and plays custom alarm

Requirements:
    pip install pyserial pygame

Usage:
    1. Upload the USB/Wired Arduino code to your Arduino Nano 33 IoT
    2. Connect Arduino to laptop via USB cable
    3. Place your custom alarm sound file (alarm.mp3 or alarm.wav) in the same folder
    4. Run this script: python fire_alert_receiver.py
    5. Select the correct COM port when prompted
"""

import serial
import serial.tools.list_ports
import pygame
import time
import os
from datetime import datetime

class FireAlertSystem:
    def __init__(self):
        self.serial_conn = None
        self.alarm_playing = False
        self.alarm_file = None
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Find alarm sound file
        self.find_alarm_file()
    
    def find_alarm_file(self):
        """Find custom alarm sound file"""
        possible_files = ['alarm.mp3', 'alarm.wav', 'fire_alarm.mp3', 
                         'fire_alarm.wav', 'alert.mp3', 'alert.wav']
        
        for filename in possible_files:
            if os.path.exists(filename):
                self.alarm_file = filename
                print(f"✓ Found alarm sound: {filename}")
                return
        
        print(" No custom alarm sound found!")
        print("  Place 'alarm.mp3' or 'alarm.wav' in the same folder")
        print("  Will use system beep as fallback\n")
    
    def list_ports(self):
        """List all available COM ports"""
        ports = serial.tools.list_ports.comports()
        available_ports = []
        
        print("\n=== Available COM Ports ===")
        for i, port in enumerate(ports):
            print(f"{i + 1}. {port.device} - {port.description}")
            available_ports.append(port.device)
        
        return available_ports
    
    def connect_arduino(self, port):
        """Connect to Arduino via serial"""
        try:
            self.serial_conn = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f" Connected to {port}")
            return True
        except Exception as e:
            print(f" Error connecting to {port}: {e}")
            return False
    
    def play_alarm(self):
        """Play alarm sound"""
        if not self.alarm_playing:
            self.alarm_playing = True
            
            if self.alarm_file:
                try:
                    pygame.mixer.music.load(self.alarm_file)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    print("ALARM PLAYING!")
                except Exception as e:
                    print(f" Error playing alarm: {e}")
                    self.play_system_beep()
            else:
                self.play_system_beep()
    
    def stop_alarm(self):
        """Stop alarm sound"""
        if self.alarm_playing:
            pygame.mixer.music.stop()
            self.alarm_playing = False
            print(" Alarm stopped")
    
    def play_system_beep(self):
        """Fallback beep sound"""
        import winsound
        frequency = 2500  # Hz
        duration = 1000   # milliseconds
        
        for _ in range(3):
            winsound.Beep(frequency, duration)
            time.sleep(0.2)
    
    def log_event(self, message):
        """Log events with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # Also save to file
        with open("fire_detection_log.txt", "a") as f:
            f.write(log_message + "\n")
    
    def monitor(self):
        """Main monitoring loop"""
        print("\n" + "="*50)
        print(" FIRE DETECTION SYSTEM ACTIVE")
        print("="*50)
        print("Monitoring for fire alerts...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    
                    if line:
                        print(f"Received: {line}")
                        
                        if "FIRE_ALERT" in line:
                            self.log_event(" FIRE DETECTED!")
                            self.play_alarm()
                            
                        elif "FIRE_CLEAR" in line:
                            self.log_event(" Fire cleared")
                            self.stop_alarm()
                            
                        elif "SYSTEM_READY" in line:
                            self.log_event(" Arduino system ready")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.stop_alarm()
            if self.serial_conn:
                self.serial_conn.close()
            print("✓ System stopped")

def main():
    print("="*50)
    print("Fire Detection Alert System - Laptop Application")
    print("="*50)
    
    system = FireAlertSystem()
    
    # List available ports
    ports = system.list_ports()
    
    if not ports:
        print("\n✗ No COM ports found!")
        print("Make sure Arduino is connected via USB")
        return
    
    # Select port
    print("\nEnter port number to connect:")
    try:
        choice = int(input("> ")) - 1
        if 0 <= choice < len(ports):
            selected_port = ports[choice]
            
            if system.connect_arduino(selected_port):
                system.monitor()
        else:
            print(f"✗ Invalid selection")
    except Exception as e:
        print(f"✗ Invalid input as {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()