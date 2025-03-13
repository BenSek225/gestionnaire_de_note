# database.py
import json
import os
from notes import Note, GestionnaireNotes

class Database:
    """Classe pour gérer la sauvegarde et le chargement des notes."""
    
    def __init__(self, fichier="notes.json"):
        self.fichier = fichier
        
    def sauvegarder_notes(self, gestionnaire_notes):
        """Sauvegarde les notes dans un fichier JSON."""
        notes_dict = [note.to_dict() for note in gestionnaire_notes.notes]
        
        with open(self.fichier, 'w', encoding='utf-8') as f:
            json.dump(notes_dict, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Notes sauvegardées dans {self.fichier}")
        
    def charger_notes(self, gestionnaire_notes):
        """Charge les notes depuis un fichier JSON."""
        if not os.path.exists(self.fichier):
            print(f"⚠️ Fichier {self.fichier} n'existe pas encore.")
            return False
            
        try:
            with open(self.fichier, 'r', encoding='utf-8') as f:
                notes_dict = json.load(f)
                
            gestionnaire_notes.notes = []
            for note_dict in notes_dict:
                note = Note(
                    titre=note_dict['titre'],
                    contenu=note_dict['contenu'],
                    categorie=note_dict.get('categorie', 'Général'),
                    id=note_dict.get('id'),
                    date_creation=note_dict.get('date_creation')
                )
                gestionnaire_notes.notes.append(note)
                
            print(f"✅ {len(gestionnaire_notes.notes)} notes chargées depuis {self.fichier}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des notes: {e}")
            return False