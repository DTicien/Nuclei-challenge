#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:47:24 2018

@author: mathieu
Cette fonction permet de charger les images de la BDD sous la forme d'un tenseur 
de dimension 4 : Nim x Nx x Ny x Ncanaux

Nim : Nombre d'images
Nx  : Nombre de pixels selon l'axe des ordonnées
Ny  : Nombre de pixels selon l'axe des abscisses
Ncanaux : Nombre de canaux (3 pour RGB, 1 pour image noir et blanc)

Entrees : 
    - type_bdd  : train ou test
    - NbImAsked : -1 (defaut) on lit toutes les images, sinon on lit NbImAsked images

"""
def load_to_tensor(type_bdd, NbImAsked = -1):

    import os
    from os import walk
    import cv2
    import numpy as np
    from skimage.transform import resize

    train_path = '../../data/stage1_train'
    test_path  = '../../data/stage1_test'
    
    dict_bdd= {'train':1,
               'test':0}
    
    if dict_bdd[type_bdd]: # Si on demande la base d'apprentissage    
        bdd_path   = train_path
    else:
        bdd_path   = test_path
    
    # Lister l'ensemble des répertoires contenant les images et les masques
    list_dir = []
    for (dirpath, dirnames, filenames) in walk(bdd_path):
        list_dir.extend(dirnames)
        break
    
    # Nombre d'images
    Nim = len(list_dir)
    if NbImAsked != -1:
        Nim = np.min([NbImAsked,Nim])
    
    
    # Taille à laquelle redimensionner les images pour la visu
    target_height = 256
    target_width  = 256
    
    X = np.zeros((Nim,target_height,target_width,3),dtype=np.float32);
    
    for i_im in range(0,Nim):
        
        im_full_path = os.path.join(bdd_path,list_dir[i_im],"images",list_dir[i_im]+".png")
        im           = cv2.imread(im_full_path)
    
        # Resize de l'image pour pouvoir les insérer dans la mosaique
        X[i_im,:,:,:] = resize(im,(target_height, target_width))

    return X