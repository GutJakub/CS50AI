In my experience the best way was to create 3 convolutional layers with the more filters I included the better the results got,
but also increased the training time and used computational power. I also completed the Image classification tutorial
on tensorflow, it helped me better understand the concept of the Pooling, which also I tested and find it best to leave it default
which is 2x2, same as in the convolutional layers I used the most common 3x3 box to search and create filters. The 0.5 dropout 
to the hidden layer drasticallly improved the loss, which for me at least at the level of 0,05 and less is the acceptable amount.
To compile I used the 'categorical_crossentropy' loss function which was the best out of the 3 I tried to test. Another interesting is 
in the tutorial it was recommended to add dropout to the convolutional layers, but I found out that it didn't really help with the 
efficiency, probably backpropagation took already care of that with assigining better weights to certain filters. The last thing I tested
is the data augmentation, I randomly assigned functions to change the photos, flip, rotate or zoom on them but it didn't really helped,
I don't know if the database of photos was already big enough or it didn't have enouch epochs to train. The amount of filters I found out really
depends on the numbers of epochs, you cannot add too many filters when you are not training enough times the model. You have to find the acceptable
middle ground.
