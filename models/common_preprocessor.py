def preprocess(inputs):
    """
    Args:
      inputs: a [batch, height, width, channels] float tensor representing a
        batch of images.

    Returns:
      preprocessed_inputs: a [batch, height, width, channels] float tensor
        representing a batch of images.
    """
    if inputs.shape.as_list()[3] == 1:
      channel_offset=[0.526418766]   #mean for FLIR dataset
      channel_scale=[0.229577947]    #std-dev for FLIR dataset
      return ((inputs / 255.0) - [[channel_offset]]) / [[channel_scale]]
    else:
      return inputs
        
