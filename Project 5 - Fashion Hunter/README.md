# FASHION HUNTER - Where Can I Buy This Outfit?

This was my final and passion project for Metis. 

As a person who loves fashion, I know that inspiration can come from many sources when it comes to finding a good outfit.
Maybe you got inspired by a celebrity in a movie or a TV show you watched, by someone you follow on Instagram or even by someone you saw walking down the street.

Most of the times you can't ask the person where did she/he buy the outfit and even if you can, maybe they bought it a long time ago and the store doesn't sell it anymore or if is a celebrity/influencer outfit, it's probably too expensive...

My idea for this project is to find a way for you to follow this inspirations. 

**What if we can build a tool in which the user can upload a picture of an outfit that he/she really liked and the tool would search through online stores to find similar outfits to recommend?**

This was my approach:

## 1. Data Collection
**For this step, I used the files inside the "scraper" folder**
- Using BeautifulSoup, I scraped 35,000 images from major e-commerce stores (Macy's, Neiman Marcus, Bloomingdale's) of clothes within seven categories.

## 2. Data Storage and Pre-Processing
**For this step, I used the .py file #1**
- Due to the size of my images, I had to process the data using an Deep Learning - AWS instance with GPU. 
- The first .py file is the code for directory settings so we can run the model. I had to save all the clothes in folders separated by train, test and validation and inside each folder, separated in sub-folders named with the category (coat, dress, top, etc.)

## 3. Modeling
**For this step, I used the jupyter notebook file #2**
- I adopted a Convolutional Neural Network framework using a pre-trained network that follows VGG16 Architecture, with data augmentation.
- For my transfer learning, I used only the convolutional base and extended it by adding additional sequential layers to classify my clothes within the seven categories.
- I got an accuracy of 91% on test set, which meant that my transfer learning was performing really weel and that I could use the flatten layer I had added to the model to do my features extraction.

## 4. Features Extraction
**For this step, I used the jupyter notebook file #3**
- Using the pre-trained flatten layer mentioned on step #3, I could calculate the features vector for each image in my dataset (for all the sub-sets, test, train and validation). The vector's shape was arround 1 x 8192 features.
- I stored all the vectors in a dataframe, along with other information about the clothes (price, brand, description, etc.)

## 5. Recommendation System
**For this step, I used the last jupyter notebook file, #4**
- With all the vectors stored in the dataframe, I could then take a new image as my input, calculate its own vector using the flatten layer and through cosine similarity, find the most similar outfit to recommend.
- There were some cases in which the background noise of the image I wanted to input affected negatively my results. Therefore, I used OpenCV to implement a built-in option of removing the background in my recommendation function.

## 6. Presentation and App Prototype
**Please reference the .pdf file with the final presentation**
- In order to display my results, I built a prototype app interface using Balsamiq. Is easy to use and very effective.

Thank you for reading and feel free to contact me if you have any doubts!

