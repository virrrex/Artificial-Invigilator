# EnGaze

A lightweight, real-time application to invigilate an exam automatically without requiring any manual invigilator, expensive hardware or data-set training. Suited for users with lesser bandwidth.


## Link to Embedded Video

Click on the picture below to see embedded video :-

[![EnGaze](https://i.ytimg.com/vi/cF7wHhn4jXM/hqdefault.jpg)](https://youtu.be/cF7wHhn4jXM)

If the above link is somehow not working - [Click here](https://youtu.be/cF7wHhn4jXM)

### Suspicious Images

During the run, following suspicious images were found that were saved for the future reference

[Suspicious Images](https://github.com/prnvdixit/Engaze/tree/master/suspicious_images)

## Installation requirements :-
	
```
	1. Python  2.7.12+
	2. OpenCV 2.4.*
	3. numpy 1.11.0+
```

## Utility :-

1. For online exams, the existing applications are heavy on user's bandwidth since they require continous video streaming.

2. Since suspicious images would be compressed & saved into some directory, they may be used for future reference by instructor too.

2. Usual Eye-gaze tracker softwares require user to NOT to be in bright enough lighting. Using Contrast optimisations, this application is somewhat receptive to that.


A major defect in a lot of existing proctoring softwares is :-

	1. Majority of them requires good enough webcam for proper functioning.
	
	2. Some require a dataset for training the model at first - Training the dataset in real-time actually slows down the application.
	
	3. Most of them require a physical proctor at some remote location keeping an eye on students constantly. This application automates it with good enough accuracy.


### Contributor

* **Pranav Dixit** - [Github](https://github.com/prnvdixit) - [Linkedin](https://www.linkedin.com/in/prnvdixit/)
