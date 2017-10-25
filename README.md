# BotDetection 

Neural Network trained to detect spammers on Reddit. Usage is as simple as: 

```
from models import Classifier 
t = 0.9 #confidence threshold to return True  

Algorithm = Classifier(t)
print(Algorithm.is_a_bot('ThaChippa'))``` 

The `is_a_bot` method from the previous example returns the following tuple: `(True, 0.9999999999956763)`, where the first item is the result and the second item is the network's confidence. 

