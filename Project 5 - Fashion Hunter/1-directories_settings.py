import numpy as np
import os, shutil
import random
import pprint
##
base_dir = '/Users/liviasalgueiro/Documents/Data Science/Metis Bootcamp/clothes'
train_dir = os.path.join(base_dir, 'train')
categories = [f for f in os.listdir(train_dir) if not f.startswith('.')]
print(categories)
##
# How many images in each category?
total_images = {}
for cat in categories:
    cat_train_dir = os.path.join(train_dir, cat)
    total_images[cat] = len([f for f in os.listdir(cat_train_dir) if not f.startswith('.')])
pprint.pprint(total_images)
print("total images:", np.sum(list(total_images.values())))
##
validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)
##
# Copy 20% of each category's images to validation and test folders (randomly):
for categ in total_images.keys():
    cat_dir_val = os.path.join(validation_dir, categ)
    os.mkdir(cat_dir_val)
    cat_dir_test = os.path.join(test_dir, categ)
    os.mkdir(cat_dir_test)
    cat_dir_train = os.path.join(train_dir, categ)
##
for categ in total_images.keys():
    cat_dir_val = os.path.join(validation_dir, categ)
    cat_dir_test = os.path.join(test_dir, categ)
    cat_dir_train = os.path.join(train_dir, categ)

    num_of_images = total_images[categ]
    val_range = int(0.2 * num_of_images)

    fnames = list(random.sample([f for f in os.listdir(cat_dir_train) if not f.startswith('.')], k=2 * val_range))
    print(fnames)

    for fname in fnames[0:val_range]:
        src = os.path.join(cat_dir_train, fname)
        dst_val = cat_dir_val
        shutil.move(src, dst_val)

    for fname in fnames[val_range:]:
        src = os.path.join(cat_dir_train, fname)
        dst_test = cat_dir_test
        shutil.move(src, dst_test)
##
# sanity check:
for categ in total_images.keys():
    cat_total = total_images[categ]
    cat_dir_val = os.path.join(validation_dir, categ)
    cat_dir_test = os.path.join(test_dir, categ)
    cat_dir_train = os.path.join(train_dir, categ)
    print('total training {} images:'.format(categ), len(os.listdir(cat_dir_train)),
          "-%:", len(os.listdir(cat_dir_train))/total_images[categ])
    print('total validation {} images:'.format(categ), len(os.listdir(cat_dir_val)),
          "-%:", len(os.listdir(cat_dir_val))/total_images[categ])
    print('total test {} images:'.format(categ), len(os.listdir(cat_dir_test)),
          "-%:", len(os.listdir(cat_dir_test))/total_images[categ])
    print("*" * 20, "/n")

