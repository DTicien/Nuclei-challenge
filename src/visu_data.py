#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:44:01 2018

@author: mathieu
Ce script permet de visualiser une mosaique d'image ainsi que les masques associés
Entrées : 
    gshape : Tuple (Nrow,Ncol) Taille de la mosaique de sortie. Ex : (10,5)
    flagMask : True si on veut la mosaique des masques, False sinon
"""
def visu_im(gshape,flagMask):

    import os
    from os import walk
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2
    from skimage.transform import resize
    from skimage.util.montage import montage2d

    # Taille auquelle redimensionner les images pour la visu
    target_height = 256
    target_width  = 256
    
    # Chemin vers la base d'apprentissage
    train_path = "/home/mathieu/Documents/Kaggle/nuclei_challenge/stage1_train";
    
    Nmos = np.prod(np.array(gshape))
    tab_im = np.zeros((Nmos,target_height,target_width,3),dtype=np.float32);
    
    # Lister l'ensemble des répertoires contenant les images et les masques
    list_dir = []
    for (dirpath, dirnames, filenames) in walk(train_path):
        list_dir.extend(dirnames)
        break
    
    i_deb = 0;
    for i_im in range(i_deb,Nmos+i_deb):
    
        #fig1.add_subplot(np.sqrt(Nmos),np.sqrt(Nmos),i_im+1)
    
        # Lecture de l'image
        im_full_path = os.path.join(train_path,list_dir[i_im],"images",list_dir[i_im]+".png")
        im           = cv2.imread(im_full_path)       
    
        # Recupération de la taille de l'image
        height_im, width_im, _  = im.shape        

    
        if flagMask:
            # Listage des fichiers de masques (Il y a un masque par nuclei)
            masks_directory_path = os.path.join(train_path,list_dir[i_im],"masks")
            
            list_masks = [];
            for (dirpath, dirnames, filenames) in walk(masks_directory_path):
                list_masks.extend(filenames)        
        
            # On cherche à visualiser un masque global pour l'image, on fait le "ou logique de tous les masques"
            Nmask = len(list_masks)
            mask  = np.zeros([height_im,width_im,3])!=0;
            for i_mask in range(0,Nmask):
                mask_full_path = os.path.join(train_path,list_dir[i_im],"masks", list_masks[i_mask])
                mask = mask | (cv2.imread(mask_full_path) != 0)
            
            # Resize du masque pour pouvoir les insérer dans la mosaique
            tab_im[i_im-i_deb,:,:,:] = resize(mask,(target_height, target_width))                
        else:            
            # Resize de l'image pour pouvoir les insérer dans la mosaique
            tab_im[i_im-i_deb,:,:,:] = resize(im,(target_height, target_width))

    # On stack les trois couleurs pour reformer l'image RGB
    mosaic = np.stack([montage2d(tab_im[:,:,:,0],grid_shape=gshape),montage2d(tab_im[:,:,:,1],grid_shape=gshape),montage2d(tab_im[:,:,:,2],grid_shape=gshape)],axis=2)
    mosaic = np.uint8(255*mosaic);
    
    # Affichage de la mosaique
    plt.figure()
    plt.imshow(mosaic)
    plt.tight_layout
    
visu_im((10,20),False)