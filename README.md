This project builds off the Robot Operating System (ROS) framework 
to create a robot tour guide. The robot is further supported by the pocketsphinx
framework to understand voice commands from people on the tour who wish to see
a certain place. 

This is implemented using a form of reactive architecture with an underlying
subsumption system. The robot is also controlled with a priority system where certain actions are more important than others (EX: detecting and avoiding obstacles is a lower
priority than if the robot's bumper hits an object. Once the robot hits an object, the robot stops immediately and moves out of the object's way to not induce further harm.)


