"""
database.py — Gestionnaire de tournoi de Jujitsu
Base de données SQLite avec toutes les tables du schéma.
"""

import sqlite3
from datetime import date
from typing import Optional


DB_PATH = "tournoi_jujitsu.db"


# ─────────────────────────────────────────
#  Connexion
# ─────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    """Retourne une connexion SQLite avec les clés étrangères activées."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # accès aux colonnes par nom
    return conn


# ─────────────────────────────────────────
#  Création des tables
# ─────────────────────────────────────────

def create_tables():
    """Crée toutes les tables si elles n'existent pas déjà."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tournoi (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nom     TEXT    NOT NULL,
                date    TEXT    NOT NULL,
                lieu    TEXT    NOT NULL,
                statut  TEXT    NOT NULL DEFAULT 'planifie'
                        CHECK(statut IN ('planifie', 'en_cours', 'termine'))
            );

            CREATE TABLE IF NOT EXISTS categorie (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                tournoi_id  INTEGER NOT NULL REFERENCES tournoi(id) ON DELETE CASCADE,
                nom         TEXT    NOT NULL,
                genre       TEXT    NOT NULL CHECK(genre IN ('masculin', 'feminin', 'mixte')),
                tranche_age TEXT,
                poids_min   REAL,
                poids_max   REAL
            );

            CREATE TABLE IF NOT EXISTS competiteur (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                prenom          TEXT NOT NULL,
                nom             TEXT NOT NULL,
                date_naissance  TEXT,
                club            TEXT,
                grade           TEXT,
                numero_licence  TEXT UNIQUE,
                poids_declare   REAL,
                poids_reel      REAL
            );

            CREATE TABLE IF NOT EXISTS inscription (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                competiteur_id  INTEGER NOT NULL REFERENCES competiteur(id) ON DELETE CASCADE,
                categorie_id    INTEGER NOT NULL REFERENCES categorie(id)   ON DELETE CASCADE,
                statut          TEXT NOT NULL DEFAULT 'inscrit'
                                CHECK(statut IN ('inscrit', 'pese', 'disqualifie', 'forfait')),
                UNIQUE(competiteur_id, categorie_id)
            );

            CREATE TABLE IF NOT EXISTS match (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                categorie_id    INTEGER NOT NULL REFERENCES categorie(id)    ON DELETE CASCADE,
                competiteur1_id INTEGER NOT NULL REFERENCES competiteur(id),
                competiteur2_id INTEGER NOT NULL REFERENCES competiteur(id),
                vainqueur_id    INTEGER          REFERENCES competiteur(id),
                phase           TEXT NOT NULL DEFAULT 'poule'
                                CHECK(phase IN ('poule', 'huitieme', 'quart', 'demi', 'finale', 'petite_finale')),
                ordre           INTEGER NOT NULL DEFAULT 1,
                tapis           INTEGER NOT NULL DEFAULT 1,
                resultat        TEXT
            );
        """)
    print("✅ Tables créées avec succès.")


# ─────────────────────────────────────────
#  CRUD — Tournoi
# ─────────────────────────────────────────

def ajouter_tournoi(nom: str, date: str, lieu: str) -> int:
    """Crée un nouveau tournoi et retourne son id."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO tournoi (nom, date, lieu) VALUES (?, ?, ?)",
            (nom, date, lieu)
        )
        assert cur.lastrowid is not None
        return cur.lastrowid


def lister_tournois() -> list:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM tournoi ORDER BY date DESC").fetchall()


def mettre_a_jour_statut_tournoi(tournoi_id: int, statut: str):
    with get_connection() as conn:
        conn.execute(
            "UPDATE tournoi SET statut = ? WHERE id = ?",
            (statut, tournoi_id)
        )


# ─────────────────────────────────────────
#  CRUD — Catégorie
# ─────────────────────────────────────────

def ajouter_categorie(
    tournoi_id: int,
    nom: str,
    genre: str,
    tranche_age: str,
    poids_min: float,
    poids_max: float
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO categorie (tournoi_id, nom, genre, tranche_age, poids_min, poids_max)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (tournoi_id, nom, genre, tranche_age, poids_min, poids_max)
        )
        assert cur.lastrowid is not None
        return cur.lastrowid


def lister_categories(tournoi_id: int) -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM categorie WHERE tournoi_id = ? ORDER BY nom",
            (tournoi_id,)
        ).fetchall()


# ─────────────────────────────────────────
#  CRUD — Compétiteur
# ─────────────────────────────────────────

def ajouter_competiteur(
    prenom: str,
    nom: str,
    club: str,
    numero_licence: str,
    date_naissance: str,
    grade: str ,
    poids_declare: float,
    poids_reel: Optional[float],
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO competiteur
               (prenom, nom, date_naissance, club, grade, numero_licence, poids_declare, poids_reel)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (prenom, nom, date_naissance, club, grade, numero_licence, poids_declare, poids_reel)
        )
        assert cur.lastrowid is not None
        return cur.lastrowid


def mettre_a_jour_poids_reel(competiteur_id: int, poids_reel: float):
    """Met à jour le poids réel après la pesée officielle."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE competiteur SET poids_reel = ? WHERE id = ?",
            (poids_reel, competiteur_id)
        )


def rechercher_competiteur(numero_licence: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM competiteur WHERE numero_licence = ?",
            (numero_licence,)
        ).fetchone()


def lister_competiteurs() -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM competiteur ORDER BY nom, prenom"
        ).fetchall()


# ─────────────────────────────────────────
#  CRUD — Inscription
# ─────────────────────────────────────────

def inscrire_competiteur(competiteur_id: int, categorie_id: int) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO inscription (competiteur_id, categorie_id) VALUES (?, ?)",
            (competiteur_id, categorie_id)
        )
        assert cur.lastrowid is not None
        return cur.lastrowid


def mettre_a_jour_statut_inscription(inscription_id: int, statut: str):
    with get_connection() as conn:
        conn.execute(
            "UPDATE inscription SET statut = ? WHERE id = ?",
            (statut, inscription_id)
        )


def lister_inscrits(categorie_id: int) -> list:
    """Liste les compétiteurs inscrits dans une catégorie avec leurs infos."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT c.*, i.statut as statut_inscription, i.id as inscription_id
               FROM competiteur c
               JOIN inscription i ON i.competiteur_id = c.id
               WHERE i.categorie_id = ?
               ORDER BY c.nom, c.prenom""",
            (categorie_id,)
        ).fetchall()


# ─────────────────────────────────────────
#  CRUD — Match
# ─────────────────────────────────────────

def creer_match(
    categorie_id: int,
    competiteur1_id: int,
    competiteur2_id: int,
    phase: str,
    ordre: int,
    tapis: int
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO match
               (categorie_id, competiteur1_id, competiteur2_id, phase, ordre, tapis)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (categorie_id, competiteur1_id, competiteur2_id, phase, ordre, tapis)
        )
        assert cur.lastrowid is not None
        return cur.lastrowid


def enregistrer_resultat(match_id: int, vainqueur_id: int, resultat: str):
    """Enregistre le vainqueur et le type de victoire (ippon, waza-ari, etc.)."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE match SET vainqueur_id = ?, resultat = ? WHERE id = ?",
            (vainqueur_id, resultat, match_id)
        )


def lister_matchs_par_tapis(tournoi_id: int, tapis: int) -> list:
    """Liste tous les matchs d'un tapis pour affichage tableau de bord."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT m.*,
                      c1.prenom || ' ' || c1.nom AS competiteur1,
                      c2.prenom || ' ' || c2.nom AS competiteur2,
                      cat.nom AS categorie
               FROM match m
               JOIN competiteur c1  ON c1.id = m.competiteur1_id
               JOIN competiteur c2  ON c2.id = m.competiteur2_id
               JOIN categorie  cat  ON cat.id = m.categorie_id
               WHERE cat.tournoi_id = ? AND m.tapis = ?
               ORDER BY m.ordre""",
            (tournoi_id, tapis)
        ).fetchall()


def lister_matchs_categorie(categorie_id: int) -> list:
    with get_connection() as conn:
        return conn.execute(
            """SELECT m.*,
                      c1.prenom || ' ' || c1.nom AS competiteur1,
                      c2.prenom || ' ' || c2.nom AS competiteur2
               FROM match m
               JOIN competiteur c1 ON c1.id = m.competiteur1_id
               JOIN competiteur c2 ON c2.id = m.competiteur2_id
               WHERE m.categorie_id = ?
               ORDER BY m.phase, m.ordre""",
            (categorie_id,)
        ).fetchall()


# ─────────────────────────────────────────
#  Point d'entrée — demo
# ─────────────────────────────────────────

if __name__ == "__main__":
    create_tables()

    # --- Tournoi
    tid = ajouter_tournoi("Open de Frankfurt", "2026-06-14", "Frankfurt Sporthalle")
    print(f"Tournoi créé : id={tid}")

    # --- Catégorie
    cid = ajouter_categorie(tid, "-66kg Masculin", "masculin", "Senior", 0, 66.0)
    print(f"Catégorie créée : id={cid}")

    # --- Compétiteurs
    p1 = ajouter_competiteur("Kaito", "Yamada", "Judo Club Frankfurt",
                              "LIC-001", "2000-03-15", "Ceinture noire 1er dan",
                              65.5, 65.8)
    p2 = ajouter_competiteur("Lucas", "Müller", "SV Jujitsu Köln",
                              "LIC-002", "1998-07-22", "Ceinture noire 2e dan",
                              64.0, 64.3)
    print(f"Compétiteurs créés : {p1}, {p2}")

    # --- Inscriptions
    inscrire_competiteur(p1, cid)
    inscrire_competiteur(p2, cid)

    # --- Match
    mid = creer_match(cid, p1, p2, phase="finale", ordre=1, tapis=1)
    enregistrer_resultat(mid, p1, "ippon")
    print(f"Match créé et résultat enregistré : id={mid}")

    # --- Vérification
    print("\n📋 Matchs sur le tapis 1 :")
    for m in lister_matchs_par_tapis(tid, 1):
        print(f"  [{m['phase']}] {m['competiteur1']} vs {m['competiteur2']} → {m['resultat']}")