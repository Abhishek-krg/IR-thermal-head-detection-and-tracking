# Custom Annotations to FLIR ADAS dataset
sharded tfrecords files for training and validation set: [here](https://drive.google.com/file/d/1NpnIgFlnmsYf1ucyTeMuBb5clvNhA7c6/view?usp=drivesdk)

custom [annotations](https://drive.google.com/file/d/1TghgsIdAzglHjpELFRAWIQFpQbhiFhhg/view?usp=drivesdk) to FLIR ADAS for human and head detection
## Training models
Tensorflow object detection needs a good amount of work while preparing for training onto FLIR's dataset
tf-object detection is only meant for 3-channel images inorder to train neural network on thermal images following should be addressed :
<ul>
  <li>image decoders</li>
  <li>image pre-processor</li>
  <li>neural-network input parameters</li>
</ul>
 
