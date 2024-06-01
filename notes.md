Data Augmentation:

```py
from tensorflow.keras.preprocessing.image import ImageDataGenerator
```

# Lung Cancer Detection using Deep Learning

## Implementation Steps

1. Load the dataset
2. Print the class labels
3. Show samples from each class
4. Check the shape of the images
5. Resize the images
6. Check the distribution of the classes
7. Handle imbalanced data
8. Use filters
9. Split the dataset into training and testing
10. Create the model
11. Compile the model
12. Train the model
13. Evaluate the model
14. Save the model

- filters 
- handle imbalanced data (undersampling)
- X,y
- X_train, X_test, y_train, y_test
- build the model

## We should also consider the following points

1. Compare the our results with other papers.
2. Use different models, parameters, optimizers, and loss functions, and compare the results.
3. The dataset is imbalanced, so we should use techniques to handle this issue like augmentation, sampling, and so on.
4. See the best filters for the biomedical images.
5. Focus on error when the model predicts the case as normal but it is malignant or benign.
6. support everything with related papers.
7. Link the model with the web.
