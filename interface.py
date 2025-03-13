# interface.py
import tkinter as tk
from tkinter import messagebox, ttk
from notes import GestionnaireNotes, Note
from database import Database

class NotesApp:
    """Classe pour l'interface graphique du gestionnaire de notes."""
    
    def __init__(self, root):
        """Initialise l'application avec une fenêtre Tkinter."""
        self.gestionnaire = GestionnaireNotes()
        self.database = Database("notes.json")
        self.root = root
        self.root.title("Gestionnaire de Notes Intelligent")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Définir les couleurs de l'interface
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4CAF50"  # Vert pour ajout
        self.delete_color = "#f44336"  # Rouge pour suppression
        self.search_color = "#2196F3"   # Bleu pour recherche
        self.reset_color = "#607D8B"   # Gris pour reset
        self.button_text_color = "white"
        self.highlight_color = "#e0f2e0"
        
        # Configurer la fenêtre principale
        self.root.configure(bg=self.bg_color)
        
        # Charger les notes existantes
        self.database.charger_notes(self.gestionnaire)
        
        # Créer l'interface
        self.creer_interface()

    def creer_interface(self):
        """Crée les éléments de l'interface graphique."""
        # Style personnalisé pour ttk
        style = ttk.Style()
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11))
        
        # Cadre principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Section supérieure (formulaire)
        form_frame = ttk.Frame(main_frame, padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Titre de l'application
        ttk.Label(form_frame, text="Gestionnaire de Notes Intelligent", 
                  font=("Helvetica", 16, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Formulaire
        input_frame = ttk.Frame(form_frame)
        input_frame.pack(fill=tk.X)
        
        # Ligne 1: Titre et Catégorie
        row1 = ttk.Frame(input_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Titre:", width=10).pack(side=tk.LEFT)
        self.entry_titre = ttk.Entry(row1, font=("Helvetica", 11))
        self.entry_titre.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Label(row1, text="Catégorie:").pack(side=tk.LEFT)
        self.entry_categorie = ttk.Combobox(row1, font=("Helvetica", 11), width=20)
        self.entry_categorie.pack(side=tk.LEFT, padx=(0, 5))
        self.mettre_a_jour_categories()
        
        # Ligne 2: Contenu
        row2 = ttk.Frame(input_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Contenu:", width=10).pack(side=tk.LEFT, anchor=tk.N)
        text_frame = ttk.Frame(row2)
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.entry_contenu = tk.Text(text_frame, height=5, font=("Helvetica", 11), 
                                    wrap=tk.WORD, borderwidth=1, relief=tk.SOLID)
        self.entry_contenu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.entry_contenu.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_contenu.config(yscrollcommand=scrollbar.set)
        
        # Ligne 3: Boutons et recherche
        row3 = ttk.Frame(input_frame)
        row3.pack(fill=tk.X, pady=(10, 0))
        
        search_frame = ttk.Frame(row3)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="Rechercher:").pack(side=tk.LEFT)
        self.entry_recherche = ttk.Entry(search_frame, font=("Helvetica", 11))
        self.entry_recherche.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.btn_rechercher = tk.Button(search_frame, text="🔍", command=self.rechercher,
                                       bg=self.search_color, fg=self.button_text_color, 
                                       font=("Helvetica", 11), padx=8, pady=4, relief=tk.FLAT)
        self.btn_rechercher.pack(side=tk.LEFT)
        
        self.btn_ajouter = tk.Button(row3, text="Ajouter Note", command=self.ajouter_note,
                                    bg=self.accent_color, fg=self.button_text_color,
                                    font=("Helvetica", 11, "bold"), padx=15, pady=5, relief=tk.FLAT)
        self.btn_ajouter.pack(side=tk.RIGHT, padx=5)
        
        # Section centrale (liste des notes)
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        list_header = ttk.Frame(list_frame)
        list_header.pack(fill=tk.X)
        
        ttk.Label(list_header, text="Mes Notes", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        
        self.btn_afficher_tout = tk.Button(list_header, text="Afficher Tout", command=self.mettre_a_jour_liste,
                                          bg=self.reset_color, fg=self.button_text_color,
                                          font=("Helvetica", 10), padx=10, pady=2, relief=tk.FLAT)
        self.btn_afficher_tout.pack(side=tk.RIGHT)
        
        listbox_frame = ttk.Frame(list_frame, borderwidth=1, relief=tk.SOLID)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.listbox_notes = tk.Listbox(listbox_frame, font=("Helvetica", 11),
                                       selectbackground=self.accent_color, activestyle="none",
                                       borderwidth=0, highlightthickness=0)
        self.listbox_notes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        list_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox_notes.yview)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_notes.config(yscrollcommand=list_scrollbar.set)
        
        self.listbox_notes.bind("<Double-Button-1>", self.ouvrir_detail_note)
        
        # Section inférieure (boutons et infos)
        bottom_frame = ttk.Frame(main_frame, padding="5")
        bottom_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.btn_supprimer = tk.Button(bottom_frame, text="Supprimer Note", command=self.supprimer_note,
                                      bg=self.delete_color, fg=self.button_text_color,
                                      font=("Helvetica", 11, "bold"), padx=15, pady=5, relief=tk.FLAT)
        self.btn_supprimer.pack(side=tk.LEFT)
        
        self.lbl_info = ttk.Label(bottom_frame, text="", font=("Helvetica", 10))
        self.lbl_info.pack(side=tk.RIGHT)
        
        # Initialiser l'interface
        self.mettre_a_jour_liste()
        self.ajouter_effets_boutons()

    def ajouter_effets_boutons(self):
        """Ajoute des effets de survol aux boutons."""
        boutons = [
            (self.btn_ajouter, self.accent_color, "#3d8c40"),
            (self.btn_rechercher, self.search_color, "#1976D2"),
            (self.btn_supprimer, self.delete_color, "#d32f2f"),
            (self.btn_afficher_tout, self.reset_color, "#455A64")
        ]
        for btn, normal, hover in boutons:
            btn.bind("<Enter>", lambda e, b=btn, c=hover: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=normal: b.config(bg=c))

    def mettre_a_jour_categories(self):
        """Met à jour la liste des catégories dans le Combobox."""
        categories = self.gestionnaire.get_categories()
        if "Général" not in categories:
            categories.insert(0, "Général")
        self.entry_categorie["values"] = categories
        if not self.entry_categorie.get():
            self.entry_categorie.set("Général")

    def ajouter_note(self):
        """Ajoute une nouvelle note."""
        titre = self.entry_titre.get().strip()
        contenu = self.entry_contenu.get("1.0", tk.END).strip()
        categorie = self.entry_categorie.get().strip() or "Général"
        if titre and contenu:
            note = Note(titre, contenu, categorie)
            self.gestionnaire.ajouter_note(note)
            self.database.sauvegarder_notes(self.gestionnaire)
            self.mettre_a_jour_liste()
            self.mettre_a_jour_categories()
            self.entry_titre.delete(0, tk.END)
            self.entry_contenu.delete("1.0", tk.END)
            messagebox.showinfo("Succès", "Note ajoutée !")
        else:
            messagebox.showwarning("Erreur", "Titre et contenu requis !")

    def supprimer_note(self):
        """Supprime la note sélectionnée."""
        try:
            index = self.listbox_notes.curselection()[0]
            if self.gestionnaire.supprimer_note(index=index):
                self.database.sauvegarder_notes(self.gestionnaire)
                self.mettre_a_jour_liste()
                self.mettre_a_jour_categories()
                messagebox.showinfo("Succès", "Note supprimée !")
        except IndexError:
            messagebox.showwarning("Erreur", "Sélectionnez une note à supprimer !")

    def rechercher(self):
        """Recherche et affiche les notes correspondantes."""
        terme = self.entry_recherche.get().strip()
        if terme:
            resultats = self.gestionnaire.rechercher_notes(terme)
            self.listbox_notes.delete(0, tk.END)
            for note in resultats:
                self.listbox_notes.insert(tk.END, note.__repr__())
            self.lbl_info.config(text=f"{len(resultats)} note(s) trouvée(s)")
        else:
            self.mettre_a_jour_liste()

    def mettre_a_jour_liste(self):
        """Met à jour la liste des notes."""
        self.listbox_notes.delete(0, tk.END)
        notes = self.gestionnaire.get_notes()
        for note in notes:
            self.listbox_notes.insert(tk.END, note.__repr__())
        self.lbl_info.config(text=f"Total: {len(notes)} note(s)")

    def ouvrir_detail_note(self, event):
        """Ouvre une fenêtre pour voir et modifier une note."""
        try:
            index = self.listbox_notes.curselection()[0]
            note = self.gestionnaire.get_notes()[index]
            self.creer_fenetre_detail(note)
        except IndexError:
            pass

    def creer_fenetre_detail(self, note):
        """Crée une fenêtre pop-up pour modifier une note."""
        fenetre = tk.Toplevel(self.root)
        fenetre.title(f"Détail: {note.titre}")
        fenetre.geometry("600x400")
        fenetre.minsize(400, 300)
        fenetre.configure(bg=self.bg_color)
        
        # Cadre principal
        detail_frame = ttk.Frame(fenetre, padding="10")
        detail_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        ttk.Label(detail_frame, text="Titre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_titre = ttk.Entry(detail_frame, font=("Helvetica", 11))
        entry_titre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        entry_titre.insert(0, note.titre)
        
        # Catégorie
        ttk.Label(detail_frame, text="Catégorie:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        combo_categorie = ttk.Combobox(detail_frame, font=("Helvetica", 11), width=20)
        combo_categorie.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        combo_categorie["values"] = self.gestionnaire.get_categories() or ["Général"]
        combo_categorie.set(note.categorie)
        
        # Contenu
        ttk.Label(detail_frame, text="Contenu:").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        text_frame = ttk.Frame(detail_frame)
        text_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        entry_contenu = tk.Text(text_frame, height=10, font=("Helvetica", 11), wrap=tk.WORD, 
                               borderwidth=1, relief=tk.SOLID)
        entry_contenu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        entry_contenu.insert("1.0", note.contenu)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=entry_contenu.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        entry_contenu.config(yscrollcommand=scrollbar.set)
        
        # Bouton Modifier
        btn_modifier = tk.Button(detail_frame, text="Modifier", 
                                bg=self.accent_color, fg=self.button_text_color,
                                font=("Helvetica", 11, "bold"), padx=15, pady=5, relief=tk.FLAT,
                                command=lambda: self.modifier_note(note.id, entry_titre.get(), 
                                                                 entry_contenu.get("1.0", tk.END), 
                                                                 combo_categorie.get(), fenetre))
        btn_modifier.grid(row=3, column=1, pady=10, sticky="e")
        
        # Configurer le redimensionnement
        detail_frame.columnconfigure(1, weight=1)
        detail_frame.rowconfigure(2, weight=1)
        
        # Effet hover sur le bouton
        btn_modifier.bind("<Enter>", lambda e: btn_modifier.config(bg="#3d8c40"))
        btn_modifier.bind("<Leave>", lambda e: btn_modifier.config(bg=self.accent_color))

    def modifier_note(self, note_id, titre, contenu, categorie, fenetre):
        """Modifie une note et met à jour l'interface."""
        if titre.strip() and contenu.strip():
            note = self.gestionnaire.modifier_note(note_id, titre.strip(), contenu.strip(), categorie.strip())
            if note:
                self.database.sauvegarder_notes(self.gestionnaire)
                self.mettre_a_jour_liste()
                self.mettre_a_jour_categories()
                fenetre.destroy()
                messagebox.showinfo("Succès", "Note modifiée !")
        else:
            messagebox.showwarning("Erreur", "Titre et contenu requis !")

def lancer_application():
    """Lance l'application Tkinter."""
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    lancer_application()