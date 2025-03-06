# Command Design pattern

A behavioral design pattern that encapsulates a request as an object, allowing you to pass, queue, delay, or undo actions easily.

## Key Components

**Command Interface** - Declares an execution method.  
**Concrete Command** - Implements the command interface and defines the actions to be executed.  
**Receiver** - Contains the actual business logic that needs to be executed.  
**Invoker** - Calls the command and executes the request.  
**Client** - Creates and assigns commands to the invoker.  

## Implementation in Python

```python

from abc import ABC, abstractmethod

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Receiver
class Light:
    def turn_on(self):
        print("The light is ON")
    
    def turn_off(self):
        print("The light is OFF")

# Concrete Commands
class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()

class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()

# Invoker
class RemoteControl:
    def __init__(self):
        self.command = None
    
    def set_command(self, command: Command):
        self.command = command
    
    def press_button(self):
        if self.command:
            self.command.execute()

# Client Code
if __name__ == "__main__":
    light = Light()
    turn_on = TurnOnCommand(light)
    turn_off = TurnOffCommand(light)
    
    remote = RemoteControl()
    
    remote.set_command(turn_on)
    remote.press_button()
    
    remote.set_command(turn_off)
    remote.press_button()
```

### Advantages

1.Decouples the sender and receiver of a request.  
2.Supports undo/redo operations.  
3.Helps implement macro commands (executing multiple commands in sequence).  
4.Simplifies logging and transactional systems.

## Use Cases

GUI buttons and menu items (e.g., undo/redo actions).  
Task scheduling systems.  
Macro recording and playback functionality.  

## Conclusion

The Command Pattern is useful when you need to decouple the object that issues a request from the one that performs it. It enhances flexibility and maintainability in software systems.
