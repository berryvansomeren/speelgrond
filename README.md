# Speelgrond

**Speelgrond is a screen shader playground with python scripting and hot-reloading** 

Think **[shadertoy](https://www.shadertoy.com/)**  but with python scripting for game logic.  

This allows you to easily implement much more complex update logic for shader toys, 
now that you can use the full space of python libraries. 
It also makes it easier to integrate input devices, now that the logic processing the inputs can be implemented in Python, 
instead of needing to pass input events through OpenGL buffer objects, as is done in shadertoy. 

Speelgrond is a lighweight wrapper of [ververser](https://github.com/berryvansomeren/ververser). 