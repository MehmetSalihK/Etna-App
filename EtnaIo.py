import tkinter as tk
from tkinter import messagebox, Toplevel
import requests
from PIL import Image, ImageTk
import io
from datetime import datetime, timedelta
from plyer import notification

class EtnaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ETNA App")  # Titre de l'application
        self.geometry("480x300")  # Taille de la fenêtre
        self.configure(bg="#4C4C4C")  # Couleur de fond de la fenêtre

        # Récupérer les informations de l'utilisateur et le cookie de session
        self.cookie = None  # Initialisation du cookie de session
        self.notification_count = 0  # Compteur de notifications
        user_info = self.fetch_user_info()  # Récupérer les informations de l'utilisateur

        if user_info:
            # Créer les widgets de l'interface utilisateur
            self.create_widgets(user_info)
            # Vérifier s'il y a de nouveaux événements à intervalles réguliers
            self.check_new_events(user_info['login'])
    
    def create_widgets(self, user_info):
        # Photo de l'utilisateur
        photo_frame = tk.Frame(self, bg="#4C4C4C")  # Cadre pour afficher la photo
        photo_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")  # Positionnement du cadre
        photo_url = f"https://auth.etna-alternance.net/api/users/{user_info['id']}/photo"  # URL de la photo de l'utilisateur
        response = requests.get(photo_url)
        photo_data = response.content if response.status_code == 200 else None
        if photo_data:
            image = Image.open(io.BytesIO(photo_data))
            image.thumbnail((100, 100))
            self.user_photo = ImageTk.PhotoImage(image)
            self.photo_label = tk.Label(photo_frame, image=self.user_photo, bg="#4C4C4C")
            self.photo_label.pack()

        # Informations de l'utilisateur
        info_frame = tk.Frame(self, bg="#4C4C4C")  # Cadre pour afficher les informations
        info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nw")  # Positionnement du cadre
        user_info_text = (
            f"Login: {user_info['login']}\n"
            f"Email: {user_info['email']}\n"
            f"Groupes: {', '.join(user_info['groups'])}\n"
            f"Date de connexion: {user_info['login_date']}\n"
            f"ID: {user_info['id']}"
        )
        self.user_info_label = tk.Label(info_frame, text=user_info_text, bg="#4C4C4C", font=("Arial", 12))
        self.user_info_label.pack(anchor="nw")

        # Bouton pour afficher le planning hebdomadaire
        self.show_planning_button = tk.Button(self, text="Afficher le planning hebdomadaire", command=lambda: self.show_weekly_planning(user_info['login']))
        self.show_planning_button.grid(row=1, column=0, columnspan=2, pady=20)

        # Compteur de notifications
        self.notification_label = tk.Label(self, text="Notifications: 0", font=("Arial", 12), bg="#4C4C4C", fg="red")
        self.notification_label.grid(row=2, column=0, columnspan=2, pady=10)

    def fetch_user_info(self):
        login = "votre login"  # Nom d'utilisateur
        password = "votre mots de passe"  # Mot de passe

        login_url = "https://auth.etna-alternance.net/login"  # URL de connexion
        login_data = {"login": login, "password": password}

        try:
            response = requests.post(login_url, data=login_data)
            response.raise_for_status()
            self.cookie = response.headers.get('Set-Cookie')

            identity_url = "https://auth.etna-alternance.net/identity"  # URL pour obtenir les informations de l'utilisateur
            headers = {"Cookie": self.cookie}
            response = requests.get(identity_url, headers=headers)
            user_info = response.json()

            return user_info
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur de connexion", f"Une erreur s'est produite: {e}")
            return None

    def fetch_user_events(self, login):
        if not self.cookie:
            messagebox.showerror("Erreur de session", "Veuillez vous connecter d'abord.")
            return None

        start_date = "2024-01-01"  # Date de début de la période de recherche des événements
        end_date = "2025-01-10"  # Date de fin de la période de recherche des événements
        events_url = f"https://intra-api.etna-alternance.net/students/{login}/events?end={end_date}&start={start_date}"
        try:
            response = requests.get(events_url, headers={"Cookie": self.cookie})
            response.raise_for_status()
            events = response.json()
            print("Events fetched: ", events)  # Debug: Afficher les événements récupérés
            return events
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur de récupération des événements", f"Une erreur s'est produite: {e}")
            return None

    def show_weekly_planning(self, login):
        events = self.fetch_user_events(login)
        if not events:
            messagebox.showwarning("Aucun événement", "Aucun événement trouvé pour cet utilisateur.")
            return

        # Nouvelle fenêtre pour afficher le planning hebdomadaire
        planning_window = Toplevel(self)
        planning_window.title("Planning Hebdomadaire")
        planning_window.geometry("330x630")
        planning_window.configure(bg="#4C4C4C")

        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_events = [
            event for event in events 
            if start_of_week <= datetime.fromisoformat(event['start'].replace('Z', '')) <= end_of_week
        ]

        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        events_by_day = {day: [] for day in days}

        for event in weekly_events:
            event_date = datetime.fromisoformat(event['start'].replace('Z', ''))
            day_name = days[event_date.weekday()]
            start_time = event_date.strftime("%H:%M")
            end_time = datetime.fromisoformat(event['end'].replace('Z', '')).strftime("%H:%M")
            name = event.get('name', 'No Title') 
            location = event.get('location', 'N/A')  # Emplacement de l'événement, si disponible
            events_by_day[day_name].append(f"{name} ({start_time} - {end_time}), Salle: {location}")

        for i, day in enumerate(days):
            day_frame = tk.Frame(planning_window, bg="#e0e0e0", bd=1, relief="solid")
            day_frame.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")

            day_label = tk.Label(day_frame, text=day, font=('Arial', 12, 'bold'), bg="#e0e0e0")
            day_label.pack(anchor="nw", padx=10, pady=5)

            events_text = "\n".join(events_by_day[day]) if events_by_day[day] else "Aucun événement"
            events_label = tk.Label(day_frame, text=events_text, justify="left", bg="#e0e0e0", font=("Arial", 10))
            events_label.pack(anchor="nw", padx=10, pady=5)

    def check_new_events(self, login):
        # Vérifier s'il y a de nouveaux événements toutes les minutes
        self.after(60000, self.check_new_events, login)

        new_events = self.fetch_user_events(login)
        if not new_events:
            return

        now = datetime.now()
        # Définir l'intervalle pour considérer un événement comme nouveau
        interval = timedelta(minutes=1)
        new_events_count = sum(
            1 for event in new_events
            if datetime.fromisoformat(event['start'].replace('Z', '')) > now - interval
        )

        if new_events_count > 0:
            self.notification_count += new_events_count
            self.notification_label.config(text=f"Notifications: {self.notification_count}")
            notification.notify(
                title="Nouveaux événements",
                message=f"Vous avez {new_events_count} nouveaux événements.",
                timeout=10
            )

if __name__ == "__main__":
    app = EtnaApp()
    app.mainloop()
