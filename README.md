# 🔣 Symba - Un interpréteur pédagogique en français 🇫🇷

**Symba** est un interpréteur écrit en Python basé sur [Lark](https://github.com/lark-parser/lark). Il exécute un petit langage inspiré du français, conçu pour l’apprentissage de la compilation, des arbres syntaxiques et de l’interprétation.

##  Fonctionnalités

- Opérations arithmétiques : `+`, `-`, `*`, `/`, avec gestion des priorités
-  Variables avec mémoire persistante
-  Structures de contrôle : conditions et boucles
-  Évaluation dynamique avec l’opérateur `@` (substitution et re-parsing)

---

## 📦 Installation

```bash
git clone https://github.com/<ton-utilisateur>/symba
cd symba
pip install -r requirements.txt
```

---

## ▶️ Utilisation

```bash
python symba.py mon_programme.symba
```

Avec affichage du contenu de la mémoire :

```bash
python symba.py mon_programme.symba -m
```

---

## 📝 Exemple de programme

```symba
x = 1 + 2
y = 2 * x
print @y    # Affiche 6

z = 2 * (1 + 2)
print @z    # Affiche 6 aussi

a = 1 + 2
print @(2 * a)  # Affiche 4
```

---

## 🧠 À propos de l’opérateur `@`

L’opérateur `@` évalue une expression après :
1. Substitution récursive des variables
2. Re-parsing pour respecter la priorité des opérations
3. Évaluation complète

Cela permet une gestion fine de l'ordre d’évaluation, par exemple :

```symba
x = 1 + 2
y = 2 * x       # Interprété comme 2 * 1 + 2 => 4
print @y        # Affiche 4
```

---

## 📁 Structure du projet

```
symba/
├── symba.py               # Point d’entrée principal
├── symba.lark             # Fichier de grammaire Lark
├── SymbaInterpreter.py    # Visiteur/interpréteur
├── memory.py              # Gestion de la mémoire
├── errors.py              # Exceptions personnalisées
└── examples/              # Exemples de programmes
```

✨ Merci d'utiliser Symba !
