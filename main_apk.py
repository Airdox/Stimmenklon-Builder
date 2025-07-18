from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.clock import Clock
import os
import threading
from voice_model import ZonosVoiceModel, check_zonos_installation, install_zonos_tts

class VoiceCloningApp(App):
    def build(self):
        # Initialize voice model
        self.current_voice_model = None
        self.training_in_progress = False
        self.synthesis_in_progress = False
        
        # Check Zonos installation on startup
        self.zonos_available = check_zonos_installation()
        
        # Hauptlayout erstellen
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Status bar for Zonos availability
        if not self.zonos_available:
            self.status_bar = Label(
                text='⚠️ Zonos TTS nicht installiert. Tippen Sie auf "Zonos installieren" um fortzufahren.',
                size_hint=(1, 0.05),
                color=(1, 0.5, 0, 1)  # Orange color
            )
            self.main_layout.add_widget(self.status_bar)
            
            # Install button
            install_btn = Button(text='Zonos TTS installieren', size_hint=(1, 0.05))
            install_btn.bind(on_press=self.install_zonos)
            self.main_layout.add_widget(install_btn)
        
        # TabbedPanel für die verschiedenen Funktionen
        self.tabs = TabbedPanel(do_default_tab=False)
        
        # Tab 1: Stimmenmodell trainieren
        self.train_tab = TabbedPanelItem(text='Stimmenmodell trainieren')
        self.train_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Bereich für Audiodateien auswählen
        self.train_layout.add_widget(Label(text='Audiodateien für Training auswählen (WAV, MP3, FLAC):'))
        
        # Dateiauswahl
        try:
            user_path = os.path.expanduser('~')
            if not os.path.exists(user_path) or not os.path.isdir(user_path):
                user_path = '/'
        except Exception:
            user_path = '/'
        self.file_chooser = FileChooserListView(path=user_path, multiselect=True)
        # Filter for audio files
        self.file_chooser.filters = ['*.wav', '*.mp3', '*.flac', '*.ogg', '*.m4a']
        self.train_layout.add_widget(self.file_chooser)
        
        # Button zum Auswählen der Dateien
        self.select_button = Button(text='Audiodateien auswählen', size_hint=(1, 0.1))
        self.select_button.bind(on_press=self.select_files)
        self.train_layout.add_widget(self.select_button)
        
        # Ausgewählte Dateien anzeigen
        self.selected_files_label = Label(text='Keine Dateien ausgewählt', size_hint=(1, 0.1))
        self.train_layout.add_widget(self.selected_files_label)
        
        # Modellname eingeben
        self.model_name_input = TextInput(
            hint_text='Modellname eingeben (z.B. "meine_stimme")', 
            size_hint=(1, 0.1)
        )
        self.train_layout.add_widget(self.model_name_input)
        
        # Training starten Button
        self.train_button = Button(text='Voice-Cloning Training starten', size_hint=(1, 0.1))
        self.train_button.bind(on_press=self.start_training)
        self.train_layout.add_widget(self.train_button)
        
        # Fortschrittsbalken
        self.progress_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.progress_label = Label(text='Fortschritt: 0%')
        self.progress_bar = ProgressBar(max=100, value=0)
        self.progress_layout.add_widget(self.progress_label)
        self.progress_layout.add_widget(self.progress_bar)
        self.train_layout.add_widget(self.progress_layout)
        
        # Log-Bereich
        self.log_label = Label(text='Training-Log:', size_hint=(1, 0.1), halign='left')
        self.log_label.bind(size=self.log_label.setter('text_size'))
        self.train_layout.add_widget(self.log_label)
        
        self.log_output = Label(
            text='Bereit für Voice-Cloning Training.\nWählen Sie Audiodateien Ihrer Stimme aus (mindestens 30 Sekunden empfohlen).', 
            size_hint=(1, 0.3), 
            halign='left', 
            valign='top'
        )
        self.log_output.bind(size=self.log_output.setter('text_size'))
        self.train_layout.add_widget(self.log_output)
        
        self.train_tab.add_widget(self.train_layout)
        self.tabs.add_widget(self.train_tab)
        
        # Tab 2: Text-to-Speech
        self.tts_tab = TabbedPanelItem(text='Deutsche Sprachsynthese')
        self.tts_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Modell auswählen
        self.tts_layout.add_widget(Label(text='Trainiertes Stimmenmodell auswählen:'))
        
        # Model selection layout
        model_select_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.model_selection = Button(text='Modell laden', size_hint=(0.7, 1))
        self.model_selection.bind(on_press=self.select_model)
        self.refresh_models_btn = Button(text='Aktualisieren', size_hint=(0.3, 1))
        self.refresh_models_btn.bind(on_press=self.refresh_models)
        model_select_layout.add_widget(self.model_selection)
        model_select_layout.add_widget(self.refresh_models_btn)
        self.tts_layout.add_widget(model_select_layout)
        
        # Ausgewähltes Modell anzeigen
        self.selected_model_label = Label(text='Kein Modell geladen', size_hint=(1, 0.1))
        self.tts_layout.add_widget(self.selected_model_label)
        
        # Text eingeben
        self.tts_layout.add_widget(Label(text='Deutschen Text für Sprachsynthese eingeben:'))
        self.text_input = TextInput(
            hint_text='Geben Sie hier Ihren deutschen Text ein...', 
            size_hint=(1, 0.3),
            multiline=True
        )
        self.text_input.text = "Hallo, ich bin Ihre geklonte Stimme. Dies ist ein Test der deutschen Sprachsynthese."
        self.tts_layout.add_widget(self.text_input)
        
        # Synthesis controls layout
        synthesis_controls = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        # Sprachsynthese starten
        self.synthesize_button = Button(text='Deutsche Sprache generieren', size_hint=(0.7, 1))
        self.synthesize_button.bind(on_press=self.start_synthesis)
        synthesis_controls.add_widget(self.synthesize_button)
        
        # Audio abspielen
        self.play_button = Button(text='Abspielen', size_hint=(0.3, 1), disabled=True)
        self.play_button.bind(on_press=self.play_audio)
        synthesis_controls.add_widget(self.play_button)
        
        self.tts_layout.add_widget(synthesis_controls)
        
        # Output file path
        self.output_path_label = Label(text='Ausgabedatei: Noch nicht generiert', size_hint=(1, 0.1))
        self.tts_layout.add_widget(self.output_path_label)
        
        # Status anzeigen
        self.tts_status = Label(
            text='Bereit für deutsche Sprachsynthese mit Voice-Cloning', 
            size_hint=(1, 0.1)
        )
        self.tts_layout.add_widget(self.tts_status)
        
        self.tts_tab.add_widget(self.tts_layout)
        self.tabs.add_widget(self.tts_tab)
        
        # TabbedPanel zum Hauptlayout hinzufügen
        self.main_layout.add_widget(self.tabs)
        
        return self.main_layout
    
    def install_zonos(self, instance):
        """Install Zonos TTS package"""
        self.show_popup("Installation", "Installing Zonos TTS...\nThis may take a few minutes.")
        
        def install_thread():
            success = install_zonos_tts()
            Clock.schedule_once(lambda dt: self.installation_complete(success), 0)
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def installation_complete(self, success):
        """Handle installation completion"""
        if success:
            self.zonos_available = True
            if hasattr(self, 'status_bar'):
                self.status_bar.text = '✅ Zonos TTS erfolgreich installiert!'
                self.status_bar.color = (0, 1, 0, 1)  # Green color
            self.show_popup("Installation", "Zonos TTS wurde erfolgreich installiert!")
        else:
            self.show_popup("Fehler", "Installation fehlgeschlagen. Bitte versuchen Sie es erneut.")
    
    def show_popup(self, title, message):
        """Show a popup message"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        close_btn = Button(text='OK', size_hint=(1, 0.3))
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def select_files(self, instance):
        """Select audio files for training"""
        selected = self.file_chooser.selection
        if selected:
            # Filter for audio files
            audio_files = [f for f in selected if any(f.lower().endswith(ext) 
                          for ext in ['.wav', '.mp3', '.flac', '.ogg', '.m4a'])]
            
            if audio_files:
                self.selected_files_label.text = f'{len(audio_files)} Audiodateien ausgewählt'
                self.update_log(f'Audiodateien ausgewählt: {len(audio_files)} Dateien')
                for file in audio_files[:3]:  # Show first 3 files
                    self.update_log(f'  - {os.path.basename(file)}')
                if len(audio_files) > 3:
                    self.update_log(f'  ... und {len(audio_files) - 3} weitere')
            else:
                self.selected_files_label.text = 'Keine Audiodateien gefunden'
                self.update_log('Fehler: Keine gültigen Audiodateien in der Auswahl gefunden')
        else:
            self.selected_files_label.text = 'Keine Dateien ausgewählt'
    
    def update_log(self, message):
        """Update the log output"""
        self.log_output.text += f'{message}\n'
    
    def start_training(self, instance):
        """Start the voice cloning training process"""
        if not self.zonos_available:
            self.show_popup("Fehler", "Zonos TTS ist nicht installiert. Bitte installieren Sie es zuerst.")
            return
            
        if self.training_in_progress:
            self.show_popup("Training läuft", "Ein Training ist bereits im Gange. Bitte warten Sie, bis es abgeschlossen ist.")
            return
        
        # Validate inputs
        selected_files = self.file_chooser.selection
        audio_files = [f for f in selected_files if any(f.lower().endswith(ext) 
                      for ext in ['.wav', '.mp3', '.flac', '.ogg', '.m4a'])]
        
        if not audio_files:
            self.show_popup("Fehler", "Keine Audiodateien ausgewählt")
            return
        
        model_name = self.model_name_input.text.strip()
        if not model_name:
            self.show_popup("Fehler", "Bitte geben Sie einen Modellnamen ein")
            return
        
        # Check for reasonable amount of audio
        if len(audio_files) < 3:
            self.show_popup("Warnung", 
                          "Für optimales Voice-Cloning werden mindestens 3 Audiodateien empfohlen.\n"
                          "Möchten Sie trotzdem fortfahren?")
        
        self.training_in_progress = True
        self.train_button.text = "Training läuft..."
        self.train_button.disabled = True
        
        self.update_log(f'=== Voice-Cloning Training gestartet ===')
        self.update_log(f'Modellname: {model_name}')
        self.update_log(f'Anzahl Audiodateien: {len(audio_files)}')
        self.update_log(f'Zonos TTS wird verwendet für deutsche Sprachsynthese')
        
        # Reset progress
        self.progress_bar.value = 0
        self.progress_label.text = 'Fortschritt: 0%'
        
        # Start training in background thread
        def train_thread():
            try:
                # Create voice model
                voice_model = ZonosVoiceModel(model_name)
                
                # Progress callback
                def progress_callback(progress):
                    Clock.schedule_once(lambda dt: self.update_training_progress(progress), 0)
                
                # Train the model
                success = voice_model.train_voice_model(audio_files, progress_callback)
                
                # Handle completion
                Clock.schedule_once(lambda dt: self.training_complete(success, voice_model), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.training_error(str(e)), 0)
        
        threading.Thread(target=train_thread, daemon=True).start()
    
    def update_training_progress(self, progress):
        """Update training progress on UI thread"""
        self.progress_bar.value = progress
        self.progress_label.text = f'Fortschritt: {int(progress)}%'
        
        # Log progress milestones
        if int(progress) in [25, 50, 75]:
            stage_names = {25: "Audiodateien verarbeitet", 
                          50: "Speaker-Embedding erstellt", 
                          75: "Modell trainiert"}
            self.update_log(f'{stage_names.get(int(progress), "")} ({int(progress)}%)')
    
    def training_complete(self, success, voice_model):
        """Handle training completion"""
        self.training_in_progress = False
        self.train_button.text = "Voice-Cloning Training starten"
        self.train_button.disabled = False
        
        if success:
            self.update_log('=== Training erfolgreich abgeschlossen! ===')
            self.update_log(f'Stimmenmodell "{voice_model.model_name}" ist bereit')
            self.update_log('Sie können jetzt zum "Deutsche Sprachsynthese" Tab wechseln')
            self.current_voice_model = voice_model
            self.show_popup("Training abgeschlossen", 
                          f'Voice-Cloning Training für "{voice_model.model_name}" erfolgreich!\n'
                          'Das Modell kann jetzt für deutsche Sprachsynthese verwendet werden.')
        else:
            self.update_log('=== Training fehlgeschlagen ===')
            self.show_popup("Training fehlgeschlagen", 
                          "Das Training konnte nicht abgeschlossen werden. "
                          "Bitte überprüfen Sie die Audiodateien und versuchen Sie es erneut.")
    
    def training_error(self, error_message):
        """Handle training error"""
        self.training_in_progress = False
        self.train_button.text = "Voice-Cloning Training starten"
        self.train_button.disabled = False
        
        self.update_log(f'Training-Fehler: {error_message}')
        self.show_popup("Training-Fehler", f"Ein Fehler ist aufgetreten:\n{error_message}")
    
    def refresh_models(self, instance):
        """Refresh the list of available models"""
        models = ZonosVoiceModel.list_available_models()
        if models:
            self.show_popup("Verfügbare Modelle", f"Gefundene Modelle:\n" + "\n".join(models))
        else:
            self.show_popup("Keine Modelle", "Keine trainierten Modelle gefunden.\nTrainieren Sie zuerst ein Modell.")
    
    def select_model(self, instance):
        """Select a trained voice model"""
        models = ZonosVoiceModel.list_available_models()
        
        if not models:
            self.show_popup("Keine Modelle", 
                          "Keine trainierten Modelle gefunden.\n"
                          "Bitte trainieren Sie zuerst ein Modell im ersten Tab.")
            return
        
        # For simplicity, use the first available model
        # In a real app, you'd show a selection dialog
        selected_model_name = models[0]
        
        try:
            # Load the model
            voice_model = ZonosVoiceModel(selected_model_name)
            if voice_model.load_voice_model():
                self.current_voice_model = voice_model
                self.selected_model_label.text = f'Geladenes Modell: {selected_model_name}'
                self.tts_status.text = f'Modell "{selected_model_name}" bereit für deutsche Sprachsynthese'
            else:
                self.show_popup("Fehler", f"Konnte Modell '{selected_model_name}' nicht laden")
        except Exception as e:
            self.show_popup("Fehler", f"Fehler beim Laden des Modells: {e}")
    
    def start_synthesis(self, instance):
        """Start speech synthesis"""
        if not self.zonos_available:
            self.show_popup("Fehler", "Zonos TTS ist nicht installiert")
            return
            
        if self.synthesis_in_progress:
            self.show_popup("Synthese läuft", "Eine Sprachsynthese ist bereits im Gange")
            return
            
        if not self.current_voice_model:
            self.show_popup("Fehler", "Kein Stimmenmodell geladen.\nBitte laden Sie zuerst ein trainiertes Modell.")
            return
        
        text = self.text_input.text.strip()
        if not text:
            self.show_popup("Fehler", "Bitte geben Sie einen Text ein")
            return
        
        self.synthesis_in_progress = True
        self.synthesize_button.text = "Generierung läuft..."
        self.synthesize_button.disabled = True
        self.play_button.disabled = True
        self.tts_status.text = 'Deutsche Sprachsynthese mit Voice-Cloning läuft...'
        
        def synthesis_thread():
            try:
                # Generate output path
                output_path = os.path.join(
                    os.path.expanduser("~"), 
                    f"stimmenklon_output_{self.current_voice_model.model_name}.wav"
                )
                
                # Synthesize speech
                result_path = self.current_voice_model.synthesize_speech(text, output_path)
                
                # Handle completion
                Clock.schedule_once(lambda dt: self.synthesis_complete(result_path), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.synthesis_error(str(e)), 0)
        
        threading.Thread(target=synthesis_thread, daemon=True).start()
    
    def synthesis_complete(self, output_path):
        """Handle synthesis completion"""
        self.synthesis_in_progress = False
        self.synthesize_button.text = "Deutsche Sprache generieren"
        self.synthesize_button.disabled = False
        
        if output_path and os.path.exists(output_path):
            self.play_button.disabled = False
            self.output_path_label.text = f'Ausgabedatei: {output_path}'
            self.tts_status.text = f'Deutsche Sprachsynthese abgeschlossen! Audio bereit zum Abspielen.'
            self.current_output_path = output_path
            self.show_popup("Synthese abgeschlossen", 
                          f'Deutsche Sprache erfolgreich generiert!\n'
                          f'Datei: {os.path.basename(output_path)}')
        else:
            self.tts_status.text = 'Sprachsynthese fehlgeschlagen'
            self.show_popup("Synthese fehlgeschlagen", "Die Sprachgenerierung konnte nicht abgeschlossen werden")
    
    def synthesis_error(self, error_message):
        """Handle synthesis error"""
        self.synthesis_in_progress = False
        self.synthesize_button.text = "Deutsche Sprache generieren"
        self.synthesize_button.disabled = False
        
        self.tts_status.text = f'Synthese-Fehler: {error_message}'
        self.show_popup("Synthese-Fehler", f"Fehler bei der Sprachgenerierung:\n{error_message}")
    
    def play_audio(self, instance):
        """Play the generated audio file"""
        if hasattr(self, 'current_output_path') and os.path.exists(self.current_output_path):
            try:
                # In a real Android app, you'd use Android's MediaPlayer
                # For now, we'll just show a message
                self.tts_status.text = f'Audio wird abgespielt: {os.path.basename(self.current_output_path)}'
                
                # Simulate playback time
                Clock.schedule_once(lambda dt: setattr(self.tts_status, 'text', 
                                   'Audio-Wiedergabe abgeschlossen'), 3)
                
                self.show_popup("Audio-Wiedergabe", 
                              f'Audio wird abgespielt:\n{os.path.basename(self.current_output_path)}\n\n'
                              'Hinweis: In der Android-App würde das Audio über die Lautsprecher wiedergegeben.')
            except Exception as e:
                self.show_popup("Wiedergabe-Fehler", f"Fehler beim Abspielen: {e}")
        else:
            self.show_popup("Fehler", "Keine Audiodatei zum Abspielen verfügbar")

if __name__ == '__main__':
    VoiceCloningApp().run()
