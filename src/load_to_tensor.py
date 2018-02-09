#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:47:24 2018

@author: mathieu
Cette fonction permet de charger les images de la BDD sous la forme d'un tenseur 
de dimension 4 : Nim x Nx x Ny x Ncanaux
Les labels sont eux chargés dans un tenseur de dimension 3 : Nim x Nx x Ny

Nim : Nombre d'images
Nx  : Nombre de pixels selon l'axe des ordonnées
Ny  : Nombre de pixels selon l'axe des abscisses
Ncanaux : Nombre de canaux (3 pour RGB, 1 pour image noir et blanc)

Entrees : 
    - type_bdd  : train ou test
    - NbImAsked : -1 (defaut) on lit toutes les images, sinon on lit NbImAsked images

Sorties : 
    - X : 

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
    y = np.zeros((Nim,target_height,target_width),dtype=np.bool)
    
    for i_im in range(0,Nim):
        
        # paths vers les images et les masques
        im_full_path         = os.path.join(bdd_path,list_dir[i_im],"images",list_dir[i_im]+".png")
        masks_directory_path = os.path.join(bdd_path,list_dir[i_im],"masks")
        
        im           = cv2.imread(im_full_path)
        
        # Recupération de la taille de l'image
        height_im, width_im, _  = im.shape
        
        # Resize de l'image pour pouvoir les insérer dans la mosaique
        X[i_im,:,:,:] = resize(im,(target_height, target_width))  
       
        # Listage des fichiers de masques (Il y a un masque par nuclei)       
        list_masks = [];
        for (dirpath, dirnames, filenames) in walk(masks_directory_path):
            list_masks.extend(filenames)        
    
        # On cherche à visualiser un masque global pour l'image, on fait le "ou logique de tous les masques"
        Nmask = len(list_masks)
        mask  = np.zeros([height_im,width_im,3])!=0;
        for i_mask in range(0,Nmask):
            mask_full_path = os.path.join(masks_directory_path, list_masks[i_mask])
            mask = mask | (cv2.imread(mask_full_path) != 0)
        
        # Resize du masque pour pouvoir les insérer dans la mosaique
        y[i_im,:,:] = resize(mask[:,:,0],(target_height, target_width)) 

    return (X, y)