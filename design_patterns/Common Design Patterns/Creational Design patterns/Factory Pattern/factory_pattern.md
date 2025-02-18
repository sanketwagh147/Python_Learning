# Factory Pattern

- Creational design pattern  used to create objects without specifying the exact class of object that will be created. It provides a method to instantiate objects in a way that lets subclasses decide which class to instantiate, making the code more flexible and scalable.

## Key Points of the Factory Pattern

- **Decouples Object Creation** : The client code does not need to know the concrete class it is using. Instead, it interacts with a factory method.
- **Enhances Flexibility**: The factory method can be extended to return different types of objects based on input parameters, configuration, or context.
- **Centralizes Object Creation**: Centralizes the object creation process in one place, making it easier to modify or extend in the future.

## Types of Factories

1. ### Simple Factory

    Imagine you are building a Document Generator system that creates either PDF or Word documents. Instead of directly creating the document objects everywhere in your code, you use a factory to create the appropriate document type.

    ```python
    # 1️⃣ Define common Interface (Base Class)

    class Document:
        def create(self):
            pass

    # 2️⃣ Concrete implementation

    class PDFDocument(Document):
        def create(self):
            return "PDF document is created"

    class HTMLDocument(Document):
        def create(self):
            return "PDF document is created"

    # 3️⃣ Factory Class

    class DocumentFactory:
    @staticmethod
    def create_document(doc_type):
        if doc_type == "pdf":
            return PDFDocument()
        elif doc_type == "word":
            return WordDocument()
        else:
            raise ValueError("Unknown document type")
    
    # 4️⃣ Client does not need to know which concrete class to use.
    doc_type = "pdf"
    document = DocumentFactory.create_document(doc_type)
    print(document.create())  # Output: PDF document created.
    ```

2. ### Factory Method

    | **Aspect**               | **Explanation**                                                  |
    |--------------------------|------------------------------------------------------------------|
    | **Purpose**               | Delegates object creation to subclasses, offering flexibility.   |
    | **When to Use**           | When a class can't predict the objects it will create and relies on subclasses to decide. |
    | **Key Characteristics**   | - Abstract factory method in the parent class.<br>- Subclasses override the method to create objects.<br>- Client code uses the factory method without knowing the concrete class. |
    | **Benefit**               | Decouples object creation from the client code, enhancing flexibility. |

    ```python
    from abc import ABC, abstractmethod

    # Abstract class that defines the factory method
    class Shape(ABC):
        @abstractmethod
        def draw(self):
            pass

    class Circle(Shape):
        def draw(self):
            return "Drawing a Circle"

    class Square(Shape):
        def draw(self):
            return "Drawing a Square"

    # Creator class with an abstract factory method
    class ShapeFactory(ABC):
        @abstractmethod
        def create_shape(self):
            pass

    # Concrete creators override the factory method
    class CircleFactory(ShapeFactory):
        def create_shape(self):
            return Circle()

    class SquareFactory(ShapeFactory):
        def create_shape(self):
            return Square()

    # Client code using the factory method
    def get_shape(factory: ShapeFactory):
        shape = factory.create_shape()
        print(shape.draw())

    # Example usage
    circle_factory = CircleFactory()
    get_shape(circle_factory)  # Output: Drawing a Circle

    square_factory = SquareFactory()
    get_shape(square_factory)  # Output: Drawing a Square


3. ### Abstract Factory Pattern

    | **Aspect**               | **Explanation**                                                  |
    |--------------------------|------------------------------------------------------------------|
    | **Purpose**               | Creates families of related objects without specifying their concrete classes. |
    | **When to Use**           | When you need to create multiple related objects that must be used together. |
    | **Key Characteristics**   | - Defines an interface for creating related objects.<br>- Concrete factories implement the interface.<br>- Client code uses the factory without knowing the specific product classes. |
    | **Benefit**               | Ensures compatibility of related products and provides flexibility in switching product families. |

    ```python

    from abc import ABC, abstractmethod

    # Abstract products for UI components

    class Button(ABC):
        @abstractmethod
        def render(self):
            pass

    class Textbox(ABC):
        @abstractmethod
        def render(self):
            pass

    # Concrete products for Windows

    class WindowsButton(Button):
        def render(self):
            return "Rendering Windows Button"

    class WindowsTextbox(Textbox):
        def render(self):
            return "Rendering Windows Textbox"

    # Concrete products for Mac

    class MacButton(Button):
        def render(self):
            return "Rendering Mac Button"

    class MacTextbox(Textbox):
        def render(self):
            return "Rendering Mac Textbox"

    # Abstract factory that defines methods for creating UI components

    class GUIFactory(ABC):
        @abstractmethod
        def create_button(self) -> Button:
            pass

        @abstractmethod
        def create_textbox(self) -> Textbox:
            pass

    # Concrete factories for Windows and Mac

    class WindowsFactory(GUIFactory):
        def create_button(self) -> Button:
            return WindowsButton()

        def create_textbox(self) -> Textbox:
            return WindowsTextbox()

    class MacFactory(GUIFactory):
        def create_button(self) -> Button:
            return MacButton()

        def create_textbox(self) -> Textbox:
            return MacTextbox()

    # Client code using the abstract factory

    def render_ui(factory: GUIFactory):
        button = factory.create_button()
        textbox = factory.create_textbox()
        print(button.render())
        print(textbox.render())

    # Example usage

    windows_factory = WindowsFactory()
    render_ui(windows_factory)  # Output: Rendering Windows Button, Rendering Windows Textbox

    mac_factory = MacFactory()
    render_ui(mac_factory)  # Output: Rendering Mac Button, Rendering Mac Textbox

    ```

## Conclusion

The Factory Pattern simplifies object creation by delegating it to subclasses. It decouples client code from specific object classes, providing flexibility and easy extensibility. This pattern is useful when object types are determined at runtime or when dealing with related object families.

| **When to Use**                                            | **When Not to Use**                                        |
|------------------------------------------------------------|------------------------------------------------------------|
| - When you need to create objects without specifying the exact class. | - When object creation logic is simple and doesn't require flexibility. |
| - When your code needs to create families of related objects. | - When you have a fixed set of objects that do not change.  |
| - When the type of object to be created is determined at runtime. | - When direct instantiation is sufficient and doesn't harm flexibility. |
| - When you want to decouple object creation from client code. | - When the overhead of multiple classes is unnecessary.    |
