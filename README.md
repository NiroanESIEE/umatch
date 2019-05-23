<p align="center"><img height="200" src="https://github.com/NiroanESIEE/umatch/blob/master/media/logo_umatch.png"></p>

# UMATCH
> Exprimez vous en restant anonyme

Le but du projet Umatch est de s'exprimer anonymement. La principale fonctionnalité est de détecter les visages sur une image ou une vidéo et les remplacer par un emoji en 3D. Celui-ci présente une expression similaire au visage détecté, une bouche recalquée ainsi qu'une rotation adéquate.

---

## Table de matière

- [Description](#Description)
- [Prérequis](#prerequis)
- [Programme](#programme)
- [Equipe](#equipe)

---

## Description

Le programme pour se déroule en plusieurs étapes

**1) Détection de visage**

La position et la taille de chaque visage de l'image (ou de chaque frame de la vidéo) sont détectées.

<img height="200" src="https://github.com/NiroanESIEE/umatch/blob/master/media/detection_visage.png">

**2) Détection de l'expression**

Le détecteur place 68 points de repères sur chacun des visages, et le programme calcule un certain nombre de paramètres (ex: ouverture des yeux) à partir de ces points qui formeront les caractéristiques de l'expression du visage.

<img height="200" src="https://github.com/NiroanESIEE/umatch/blob/master/media/facial_landmarks_68.jpg">

**3) Modélisation 3D**

Un modèle 3D est chargé et transformé en adéquation avec cette expression ainsi que la rotation de la tête.

<img height="200" src="https://github.com/NiroanESIEE/umatch/blob/master/media/modelisation_3d.png">

**4) Génération de la nouvelle image (ou vidéo)**

Le visage sur l'image (ou la vidéo) est remplacé par le modèle transformé.

<img height="200" src="https://github.com/NiroanESIEE/umatch/blob/master/media/example.png">

---

## Prérequis

Ce projet a été réalisé en langage Python. Les packages suivants sont nécessaires pour le fonctionnement du programme :

- **Détection des visages et des expressions** :
	- Imutils
	- Dlib

- **Machine Learning**
	- SKLearn (LogisticRegression)
	- Pickle
	
- **Traitement d'images**
	- OpenCV (cv2)
	- PIL
	
- **Traitement de modèles 3D** :
	- OpenGL
	- PyGame

- **Autres**
	- os
	- argparse
	- math
	- numpy

---
	
## Programme

### Structure du projet

**Programme principal**

- *Umatch.py*

	Effectue la reconnaissance de l'expression sur l'image ou la vidéo passée en paramètre, et recrée une version où les visages sont remplacés par les emoji correspondants
	
**Programmes complémentaires**

- *ObjectReader.py*

	Lit et stocke d'un modèle 3D (fichiers .obj et .mtl) sous forme d'une classe Python

- *EmojiModifier.py*

	Effectue les transformations nécessaires sur le modèle 3D en fonction des paramètres du visage détecté (rotations, expression des yeux, ouverture de la bouche)

- *face_parameter.py*

	Contient les fonctions utiles au calcul des paramètres du visage
	
- *face_learning.py*

	Apprend les paramètres des différentes expressions à partir d'une base d'images et crée le modèle

- *expression_learning.sav*

	Modèle d'apprentissage des expressions

- *shape_predictor_68_face_landmarks.dat*

	Fichier de données utilisé pour détecter les points d'intérêts du visage
	
**Images**

- *learning_images* : dossier contenant la base d'images pour l'apprentissage
- *images* : dossier contenant les images et vidéos à tester
- *output_images* : dossier contenant les images et vidéos résultants
	
**Modèles 3D**

- *3d_object* : dossier contenant les modèles 3D

### Lancement du programme

#### Test sur une image

```python
python Umatch.py -p image_path
```

#### Test sur une vidéo

```python
python Umatch.py -v video_path
```

---

## Equipe

Ce projet a été réalisé par des étudiants de l'école ESIEE de la filière Informatique et Applications sous la tutelle de M. Benjamin Raynal.
L'équipe est formée de :
- **Cheickalavoudine Safrine**
- **Delphin Alexandra**
- **Jeyathasan Niroan**
- **Martin Estelle**
- **Zhang Lise**
