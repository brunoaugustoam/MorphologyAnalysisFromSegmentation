import numpy as np
import cv2
import os


# class Particle_Dataset():
#     def __init__(self, root,img_idx):
#         '''
#         img_idx reffers to the particle codification: 124 for trimer; 116 for dumbbells; and 59 for spheres
#         '''
#         self.root = root
#         self.img_idx = img_idx
#         self.files = self.make_dataset()

        
#     def __len__(self):
#         return len(self.files)
    
#     def make_dataset(self):
#         self.data_path = os.path.join(self.root,'Dataset','SEM')
#         files = os.listdir(self.data_path)
#         filtered_files = sorted([ r for r in files if  r.split('.')[-1]=='tif' ])
#         filtered_imgs = sorted([ r for r in filtered_files if  r.split('_')[1]==self.img_idx])
#         return filtered_imgs
    
#     def get_idx_crop(self,image, sample):
#         img_crop = image[2:-2,2:-2,:]
#         i, j , k= np.where(img_crop <2 )
#         unique_white, counts_white = np.unique(i, return_counts=True)

#         #x,y,z = np.where(img_crop > 253)

#         if sample.split('_')[1]  != '59':
#             return unique_white[0]
#         else:
#             return list(counts_white).index(max(counts_white))

    
#     def __getitem__(self,index):
#         particle_idx = self.files[index]
#         particle_name = str(particle_idx).split("/")[-1]
#         filename = os.path.join(self.data_path,particle_name)
#         image =  cv2.imread(filename, cv2.IMREAD_UNCHANGED)
#         cropped_img = image[2:-2,2:-2,:]
#         cropped_img = image[:self.get_idx_crop(image, particle_name),:,:]
#         return cropped_img, particle_name

class Particle_Dataset:
  """
  This class represents a dataset of particle images for a specific particle type.

  Args:
      root (str): The root directory of the dataset.
      img_idx (int): The particle type code (e.g., 124 for trimers, 116 for dumbbells, 59 for spheres).
  """

  def __init__(self, root, img_idx):
    """
    Initializes the Particle_Dataset object.

    Args:
        root (str): The root directory of the dataset.
        img_idx (int): The particle type code.
    """

    self.root = root
    self.img_idx = img_idx
    self.files = self.make_dataset()

  def __len__(self):
    """
    Returns the number of images in the dataset.

    Returns:
        int: The number of images in the dataset.
    """

    return len(self.files)

  def make_dataset(self):
    """
    Creates a list of filenames of the particle images based on the particle type code.

    Returns:
        list: A list of filenames of the particle images.
    """

    # Define data path
    files = os.listdir(self.root)  # Get all files in the path
    # print(files)
    # Filter files based on extension and particle type code
    filtered_files = sorted([r for r in files if r.split('.')[-1] == 'tif'])
    
    filtered_imgs = sorted([r for r in filtered_files if r.split('_')[0].split(' ')[1] == str(self.img_idx)])
    return filtered_imgs

  def get_idx_crop(self, image, sample):
    """
    Crops the image and identifies the index for further processing based on the particle type.

    Args:
        image (np.ndarray): The raw image data.
        sample (str): The filename of the image.

    Returns:
        int or list: The index for further processing depending on the particle type.
    """

    cropped_img = image[2:-2, 2:-2, :]  # Crop the image

    # Find and analyze white pixels (background)
    i, j, k = np.where(cropped_img < 2)
    unique_white, counts_white = np.unique(i, return_counts=True)
    # print(sample.split('_')[1],sample.split('_'))
    # Determine the index based on particle type
    if sample.split('_')[0].split(' ')[1] != '59':
      return unique_white[0]  # Return the first white pixel index for non-spherical particles
    else:
      return list(counts_white).index(max(counts_white))  # Return the index of the most frequent white pixel for spheres

  def __getitem__(self, index):
    """
    Retrieves a specific image and its name from the dataset.

    Args:
        index (int): The index of the image to retrieve.

    Returns:
        tuple: A tuple containing the cropped image (np.ndarray) and its filename (str).
    """

    particle_idx = self.files[index]
    particle_name = str(particle_idx).split("/")[-1]
    filename = os.path.join(self.root, particle_name)

    image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    cropped_img = image[2:-2, 2:-2, :]

    # Apply cropping based on the particle type and retrieved index
    cropped_img = cropped_img[:self.get_idx_crop(image, particle_name), :, :]

    return cropped_img, particle_name
