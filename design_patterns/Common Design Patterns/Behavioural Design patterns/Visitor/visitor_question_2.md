# Visitor Pattern — Question 2 (Medium)

## Problem: AST (Abstract Syntax Tree) Analyzer

Build a set of visitors that analyze a simple programming language's AST without modifying the node classes.

### Requirements

#### AST Nodes
```python
class ASTNode(ABC):
    def accept(self, visitor: ASTVisitor): ...

class ProgramNode(ASTNode):      # root — contains list of statements
class AssignNode(ASTNode):        # variable = expression
class PrintNode(ASTNode):         # print(expression)
class BinaryOpNode(ASTNode):      # left op right  (op: +, -, *, /)
class NumberNode(ASTNode):        # literal number
class VariableNode(ASTNode):      # variable reference
class IfNode(ASTNode):            # if condition then body [else body]
```

#### Visitors
1. **PrettyPrintVisitor**: outputs formatted source code from the AST
2. **VariableCollectorVisitor**: returns set of all variable names used
3. **ComplexityVisitor**: counts the number of branches (if statements) and operations

#### Sample AST (representing the code below)
```
x = 10
y = x + 5
if y > 12:
    print(y)
```

### Expected Usage

```python
ast = build_sample_ast()  # builds the AST above

printer = PrettyPrintVisitor()
ast.accept(printer)
# → x = 10
# → y = x + 5
# → if y > 12:
# →     print(y)

vars_visitor = VariableCollectorVisitor()
ast.accept(vars_visitor)
print(vars_visitor.variables)  # → {"x", "y"}

complexity = ComplexityVisitor()
ast.accept(complexity)
print(complexity.report())
# → {"branches": 1, "operations": 2, "assignments": 2, "prints": 1}
```

### Constraints

- AST node classes must NOT change when adding a new visitor.
- Each visitor handles ALL node types.
- Use the standard `visit_<NodeType>` method naming convention.

### Think About

- How is this used in real compilers and linters (e.g., Python's `ast` module)?
- What if you add a new node type? Every visitor must be updated — is this a problem?
