"""
Stimmenklon-Builder - Voice Cloning Application
===============================================

Eine mobile Anwendung für Stimmen-Kloning mit intuitiver Benutzeroberfläche.
Ermöglicht das Training von Stimmenmodellen und Text-to-Speech Synthese.

Autor: Stimmenklon-Builder Team
Version: 1.0.0
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
import os
import random

# Konstanten für die Anwendung
MIN_PROGRESS_INCREMENT = 1
MAX_PROGRESS_INCREMENT = 5
TRAINING_UPDATE_INTERVAL = 0.5
SYNTHESIS_DURATION = 2.0
PLAYBACK_DURATION = 2.0

class VoiceCloningApp(App):
    """
    Hauptklasse für die Stimmenklon-Builder Anwendung.
    
    Diese Klasse implementiert eine Kivy-Anwendung mit zwei Hauptfunktionen:
    1. Training von Stimmenmodellen aus Audiodateien
    2. Text-to-Speech Synthese mit trainierten Modellen
    """
    
    def __init__(self, **kwargs):
        """Initialisiert die Anwendung mit notwendigen Attributen."""
        super().__init__(**kwargs)
        self.train_event = None  # Referenz für den Training-Event
        self.selected_files = []  # Liste der ausgewählten Dateien
        self.current_model = None  # Aktuell ausgewähltes Modell
    
    def build(self):
        """
        Erstellt die Benutzeroberfläche der Anwendung.
        
        Returns:
            BoxLayout: Das Hauptlayout der Anwendung
        """
        # Hauptlayout erstellen
        self.main_layout = BoxLayout(orientation='vertical')
        
        # TabbedPanel für die verschiedenen Funktionen
        self.tabs = TabbedPanel(do_default_tab=False)
        
        # Tab für Stimmenmodell-Training erstellen
        self._create_training_tab()
        
        # Tab für Text-to-Speech erstellen
        self._create_tts_tab()
        
        # TabbedPanel zum Hauptlayout hinzufügen
        self.main_layout.add_widget(self.tabs)
        
        return self.main_layout
    
    def _create_training_tab(self):
        """Erstellt den Tab für das Training von Stimmenmodellen."""
        self.train_tab = TabbedPanelItem(text='Stimmenmodell trainieren')
        self.train_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Bereich für Audiodateien auswählen
        self.train_layout.add_widget(Label(text='Audiodateien für Training auswählen:'))
        
        # Dateiauswahl mit sicherem Pfad
        safe_path = self._get_safe_path()
        self.file_chooser = FileChooserListView(path=safe_path)
        self.train_layout.add_widget(self.file_chooser)
        
        # Button zum Auswählen der Dateien
        self.select_button = Button(text='Dateien auswählen', size_hint=(1, 0.1))
        self.select_button.bind(on_press=self.select_files)
        self.train_layout.add_widget(self.select_button)
        
        # Ausgewählte Dateien anzeigen
        self.selected_files_label = Label(text='Keine Dateien ausgewählt', size_hint=(1, 0.1))
        self.train_layout.add_widget(self.selected_files_label)
        
        # Modellname eingeben
        self.model_name_input = TextInput(hint_text='Modellname eingeben', size_hint=(1, 0.1))
        self.train_layout.add_widget(self.model_name_input)
        
        # Training starten Button
        self.train_button = Button(text='Training starten', size_hint=(1, 0.1))
        self.train_button.bind(on_press=self.start_training)
        self.train_layout.add_widget(self.train_button)
        
        # Fortschrittsbereich erstellen
        self._create_progress_section()
        
        # Log-Bereich erstellen
        self._create_log_section()
        
        self.train_tab.add_widget(self.train_layout)
        self.tabs.add_widget(self.train_tab)
    
    def _create_tts_tab(self):
        """Erstellt den Tab für Text-to-Speech Funktionalität."""
        self.tts_tab = TabbedPanelItem(text='Text-to-Speech')
        self.tts_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Modell auswählen
        self.tts_layout.add_widget(Label(text='Stimmenmodell auswählen:'))
        self.model_selection = Button(text='Modell auswählen', size_hint=(1, 0.1))
        self.model_selection.bind(on_press=self.select_model)
        self.tts_layout.add_widget(self.model_selection)
        
        # Ausgewähltes Modell anzeigen
        self.selected_model_label = Label(text='Kein Modell ausgewählt', size_hint=(1, 0.1))
        self.tts_layout.add_widget(self.selected_model_label)
        
        # Text eingeben
        self.tts_layout.add_widget(Label(text='Text eingeben:'))
        self.text_input = TextInput(hint_text='Text für Sprachsynthese eingeben', size_hint=(1, 0.3))
        self.tts_layout.add_widget(self.text_input)
        
        # Sprachsynthese starten
        self.synthesize_button = Button(text='Sprachsynthese starten', size_hint=(1, 0.1))
        self.synthesize_button.bind(on_press=self.start_synthesis)
        self.tts_layout.add_widget(self.synthesize_button)
        
        # Audio abspielen
        self.play_button = Button(text='Audio abspielen', size_hint=(1, 0.1), disabled=True)
        self.play_button.bind(on_press=self.play_audio)
        self.tts_layout.add_widget(self.play_button)
        
        # Status anzeigen
        self.tts_status = Label(text='Bereit', size_hint=(1, 0.1))
        self.tts_layout.add_widget(self.tts_status)
        
        self.tts_tab.add_widget(self.tts_layout)
        self.tabs.add_widget(self.tts_tab)
    
    def _create_progress_section(self):
        """Erstellt den Fortschrittsbereich für das Training."""
        self.progress_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.progress_label = Label(text='Fortschritt: 0%')
        self.progress_bar = ProgressBar(max=100, value=0)
        self.progress_layout.add_widget(self.progress_label)
        self.progress_layout.add_widget(self.progress_bar)
        self.train_layout.add_widget(self.progress_layout)
    
    def _create_log_section(self):
        """Erstellt den Log-Bereich für Statusmeldungen."""
        self.log_label = Label(text='Log-Ausgabe:', size_hint=(1, 0.1), halign='left')
        self.log_label.bind(size=self.log_label.setter('text_size'))
        self.train_layout.add_widget(self.log_label)
        
        self.log_output = Label(text='', size_hint=(1, 0.3), halign='left', valign='top')
        self.log_output.bind(size=self.log_output.setter('text_size'))
        self.train_layout.add_widget(self.log_output)
    
    def _get_safe_path(self):
        """
        Ermittelt einen sicheren Pfad für die Dateiauswahl.
        
        Returns:
            str: Sicherer Pfad für die Dateiauswahl
        """
        try:
            # Versuche das Home-Verzeichnis zu verwenden
            user_path = os.path.expanduser('~')
            if os.path.exists(user_path) and os.path.isdir(user_path):
                return user_path
        except Exception as e:
            self._log_message(f'Warnung: Konnte Home-Verzeichnis nicht ermitteln: {e}')
        
        # Fallback auf Root-Verzeichnis
        return '/'
    
    def _log_message(self, message):
        """
        Fügt eine Nachricht zum Log hinzu.
        
        Args:
            message (str): Die Nachricht, die geloggt werden soll
        """
        if hasattr(self, 'log_output'):
            self.log_output.text += f'{message}\n'
    
    def select_files(self, instance):
        """
        Behandelt die Auswahl von Audiodateien für das Training.
        
        Args:
            instance: Die Button-Instanz, die das Event ausgelöst hat
        """
        try:
            selected = self.file_chooser.selection
            if selected:
                self.selected_files = selected
                self.selected_files_label.text = f'{len(selected)} Dateien ausgewählt'
                self._log_message(f'Dateien ausgewählt: {", ".join([os.path.basename(f) for f in selected])}')
            else:
                self.selected_files = []
                self.selected_files_label.text = 'Keine Dateien ausgewählt'
                self._log_message('Keine Dateien ausgewählt')
        except Exception as e:
            self._log_message(f'Fehler bei der Dateiauswahl: {e}')
    
    def start_training(self, instance):
        """
        Startet den Trainingsprozess für ein Stimmenmodell.
        
        Args:
            instance: Die Button-Instanz, die das Event ausgelöst hat
        """
        # Validierung der Eingaben
        if not self.selected_files:
            self._log_message('Fehler: Keine Audiodateien ausgewählt')
            return
        
        model_name = self.model_name_input.text.strip()
        if not model_name:
            self._log_message('Fehler: Kein Modellname eingegeben')
            return
        
        # Validierung des Modellnamens
        if not self._validate_model_name(model_name):
            self._log_message('Fehler: Ungültiger Modellname (nur Buchstaben, Zahlen und Unterstriche erlaubt)')
            return
        
        try:
            self._log_message(f'Training gestartet für Modell: {model_name}')
            self._log_message(f'Anzahl Dateien: {len(self.selected_files)}')
            
            # Training-UI zurücksetzen
            self.progress_bar.value = 0
            self.progress_label.text = 'Fortschritt: 0%'
            self.train_button.disabled = True
            
            # Simuliere Trainingsfortschritt
            self.train_event = Clock.schedule_interval(self.update_progress, TRAINING_UPDATE_INTERVAL)
            
        except Exception as e:
            self._log_message(f'Fehler beim Starten des Trainings: {e}')
            self.train_button.disabled = False
    
    def update_progress(self, dt):
        """
        Aktualisiert den Fortschrittsbalken während des Trainings.
        
        Args:
            dt: Zeitdelta seit dem letzten Update
            
        Returns:
            bool: False wenn das Training abgeschlossen ist, True zum Fortfahren
        """
        try:
            if self.progress_bar.value >= 100:
                # Training abgeschlossen
                if self.train_event:
                    self.train_event.cancel()
                    self.train_event = None
                
                self._log_message('Training erfolgreich abgeschlossen!')
                self.progress_label.text = 'Fortschritt: 100%'
                self.train_button.disabled = False
                return False
            
            # Zufälliger Fortschritt für die Simulation
            progress_increment = random.randint(MIN_PROGRESS_INCREMENT, MAX_PROGRESS_INCREMENT)
            new_value = min(self.progress_bar.value + progress_increment, 100)
            self.progress_bar.value = new_value
            self.progress_label.text = f'Fortschritt: {int(new_value)}%'
            
            # Log-Updates alle 10%
            if int(new_value) % 10 < progress_increment and int(new_value - progress_increment) % 10 >= progress_increment:
                self._log_message(f'Training bei {int(new_value)}%...')
            
            return True
            
        except Exception as e:
            self._log_message(f'Fehler während des Trainings: {e}')
            if self.train_event:
                self.train_event.cancel()
                self.train_event = None
            self.train_button.disabled = False
            return False
    
    def select_model(self, instance):
        """
        Simuliert die Auswahl eines trainierten Stimmenmodells.
        
        Args:
            instance: Die Button-Instanz, die das Event ausgelöst hat
        """
        try:
            # In einer echten App würde hier ein Dateiauswahldialog erscheinen
            available_models = ['Stimme_Person_A', 'Stimme_Person_B', 'Stimme_Person_C']
            selected_model = random.choice(available_models)
            
            self.current_model = selected_model
            self.selected_model_label.text = f'Ausgewähltes Modell: {selected_model}'
            self.tts_status.text = 'Modell geladen - bereit für Synthese'
            
        except Exception as e:
            self.tts_status.text = f'Fehler beim Laden des Modells: {e}'
    
    def start_synthesis(self, instance):
        """
        Startet die Text-to-Speech Synthese.
        
        Args:
            instance: Die Button-Instanz, die das Event ausgelöst hat
        """
        # Validierung der Eingaben
        if not self.current_model:
            self.tts_status.text = 'Fehler: Kein Modell ausgewählt'
            return
        
        text_content = self.text_input.text.strip()
        if not text_content:
            self.tts_status.text = 'Fehler: Kein Text eingegeben'
            return
        
        if len(text_content) > 1000:  # Praktisches Limit für die Demo
            self.tts_status.text = 'Fehler: Text zu lang (max. 1000 Zeichen)'
            return
        
        try:
            self.tts_status.text = 'Sprachsynthese läuft...'
            self.synthesize_button.disabled = True
            self.play_button.disabled = True
            
            # Simuliere Verarbeitungszeit
            Clock.schedule_once(self.finish_synthesis, SYNTHESIS_DURATION)
            
        except Exception as e:
            self.tts_status.text = f'Fehler bei der Sprachsynthese: {e}'
            self.synthesize_button.disabled = False
    
    def finish_synthesis(self, dt):
        """
        Behandelt den Abschluss der Sprachsynthese.
        
        Args:
            dt: Zeitdelta seit dem Start
        """
        try:
            self.tts_status.text = 'Sprachsynthese abgeschlossen'
            self.synthesize_button.disabled = False
            self.play_button.disabled = False
        except Exception as e:
            self.tts_status.text = f'Fehler beim Abschließen der Synthese: {e}'
    
    def play_audio(self, instance):
        """
        Simuliert das Abspielen der generierten Audiodatei.
        
        Args:
            instance: Die Button-Instanz, die das Event ausgelöst hat
        """
        try:
            self.tts_status.text = 'Audio wird abgespielt...'
            self.play_button.disabled = True
            
            # Simuliere Wiedergabezeit
            Clock.schedule_once(self._finish_playback, PLAYBACK_DURATION)
            
        except Exception as e:
            self.tts_status.text = f'Fehler beim Abspielen: {e}'
            self.play_button.disabled = False
    
    def _finish_playback(self, dt):
        """
        Behandelt das Ende der Audio-Wiedergabe.
        
        Args:
            dt: Zeitdelta seit dem Start
        """
        try:
            self.tts_status.text = 'Audio abgespielt'
            self.play_button.disabled = False
        except Exception as e:
            self.tts_status.text = f'Fehler beim Beenden der Wiedergabe: {e}'
    
    def _validate_model_name(self, name):
        """
        Validiert den eingegebenen Modellnamen.
        
        Args:
            name (str): Der zu validierende Modellname
            
        Returns:
            bool: True wenn der Name gültig ist, False sonst
        """
        import re
        # Erlaubt nur Buchstaben, Zahlen und Unterstriche
        return bool(re.match(r'^[a-zA-Z0-9_]+$', name)) and len(name) <= 50


if __name__ == '__main__':
    try:
        VoiceCloningApp().run()
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")
        import traceback
        traceback.print_exc()
