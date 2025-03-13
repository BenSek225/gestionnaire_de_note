# notes.py
from datetime import datetime

class Note:
    """Classe représentant une note avec un titre, un contenu et une date de création."""
    
    def __init__(self, titre: str, contenu: str, categorie: str = "Général", id=None, date_creation=None):
        self.id = id if id else datetime.now().timestamp()
        self.titre = titre
        self.contenu = contenu
        self.categorie = categorie
        self.date_creation = date_creation if date_creation else datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        """Convertit la note en dictionnaire pour la sauvegarde JSON"""
        return {
            "id": self.id,
            "titre": self.titre,
            "contenu": self.contenu,
            "categorie": self.categorie,
            "date_creation": self.date_creation
        }
        
    def __repr__(self):
        return f"{self.titre} ({self.categorie}) - {self.date_creation}"


class GestionnaireNotes:
    """Classe pour gérer les notes (ajout, suppression, modification)."""
    
    def __init__(self):
        self.notes = []

    def ajouter_note(self, note: Note):
        """Ajoute une note à la liste."""
        self.notes.append(note)
        print(f"✅ Note ajoutée : {note}")
        return note
        
    def supprimer_note(self, index=None, note_id=None):
        """Supprime une note de la liste par index ou ID."""
        if index is not None:
            if 0 <= index < len(self.notes):
                note_supprimee = self.notes.pop(index)
                print(f"✅ Note supprimée : {note_supprimee}")
                return True
        elif note_id is not None:
            for i, note in enumerate(self.notes):
                if note.id == note_id:
                    note_supprimee = self.notes.pop(i)
                    print(f"✅ Note supprimée : {note_supprimee}")
                    return True
                    
        print("❌ Note non trouvée")
        return False
    
    def modifier_note(self, note_id, titre=None, contenu=None, categorie=None):
        """Modifie une note existante."""
        for note in self.notes:
            if note.id == note_id:
                if titre:
                    note.titre = titre
                if contenu:
                    note.contenu = contenu
                if categorie:
                    note.categorie = categorie
                print(f"✅ Note modifiée : {note}")
                return note
        
        print("❌ Note non trouvée")
        return None
        
    def rechercher_notes(self, terme_recherche):
        """Recherche des notes par titre, contenu ou catégorie."""
        resultats = []
        terme_recherche = terme_recherche.lower()
        
        for note in self.notes:
            if (terme_recherche in note.titre.lower() or 
                terme_recherche in note.contenu.lower() or 
                terme_recherche in note.categorie.lower()):
                resultats.append(note)
                
        return resultats
        
    def filtrer_par_categorie(self, categorie):
        """Filtre les notes par catégorie."""
        return [note for note in self.notes if note.categorie == categorie]
        
    def get_categories(self):
        """Retourne la liste de toutes les catégories utilisées."""
        categories = set()
        for note in self.notes:
            categories.add(note.categorie)
        return sorted(list(categories))
    
    def get_notes(self):
        """Retourne la liste de toutes les notes."""
        return self.notes