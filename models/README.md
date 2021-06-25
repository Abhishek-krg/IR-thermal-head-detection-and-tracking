Thermal images needs to be rescaled for neural network ssd-efficientdet requires mean and std-dev as hyper-parameter for scaling the inputs sample code with computed mean and std-dev for FLIR's dataset is provided in [common_preprocessor.py](https://github.com/Abhishek-krg/covid-ir/blob/main/models/common_preprocessor.py)  

ssd-efficientdet model overrides should be passed as dictionary while calling backbone neural network
```python
efficientnet_base = efficientnet_model.EfficientNet.from_name(
        model_name=self._efficientnet_version,
        overrides={'rescale_input': False,'input_channels':1})
        
```
The overrides above along with the pre-processor will generate a single channel compatible object-detection model which can then be used for inference.

Training the models can be a bit more complicated as the default tfrecord decoders are incompatible with single channel data produced by thermal cameras.
