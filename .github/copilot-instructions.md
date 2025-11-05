# AI Coding Agent Instructions for Python_Learning Repository

Welcome to the **Python_Learning** repository! This document provides essential guidelines for AI coding agents to be productive in this codebase. Follow these instructions to understand the architecture, workflows, and conventions.

---

## 📂 Project Overview

This repository contains a variety of Python projects, including:

1. **Design Patterns**: Examples of SOLID principles and other design patterns.
2. **Data Science**: Jupyter notebooks and Python scripts for data analysis.
3. **SQL**: PostgreSQL scripts for database operations.
4. **Dockerized Apps**: Multi-container applications with React and backend services.

---

## 🏗️ Architecture Highlights

### 1. **Design Patterns**
- Located in `design_patterns/`.
- Focus on SOLID principles (e.g., Single Responsibility Principle, Open-Close Principle).
- Each principle has:
  - A Python file with examples (`*.py`).
  - A Markdown file explaining the principle (`*.md`).
- Example: `design_patterns/Solid Principles/Single Responsibility Principle/`.

### 2. **Data Science Projects**
- Found in `Modules/pandas/` and other subdirectories.
- Jupyter notebooks (`*.ipynb`) demonstrate data manipulation and visualization.
- Example: `Modules/pandas/Freecodecamp/FreeCodeCamp-Pandas-Real-Life-Example-master/`.

### 3. **Dockerized Apps**
- Located in `docker_files/`.
- Example: `docker_multi_container_app/frontend/` contains a React app.
- Use `npm start` to run the frontend locally.

---

## 🔧 Developer Workflows

### 1. **Running Python Examples**
- Navigate to the relevant directory.
- Use `python3 <filename>.py` to execute scripts.
- Example:
  ```bash
  cd design_patterns/Solid\ Principles/Single\ Responsibility\ Principle
  python3 single_responsiblility_principle.py
  ```

### 2. **Testing**
- No centralized test framework is set up.
- Tests are often embedded within example scripts.
- Example: Running `single_responsiblility_principle.py` demonstrates good vs bad design patterns.

### 3. **Building Dockerized Apps**
- Navigate to the app directory (e.g., `docker_multi_container_app/frontend/`).
- Use `npm start` to run the React app locally.

---

## 📏 Project-Specific Conventions

### 1. **Code Organization**
- Follow the **Single Responsibility Principle** for Python classes.
- Example:
  ```python
  class Employee:
      def __init__(self, name, salary):
          self.name = name
          self.salary = salary

  class SalaryCalculator:
      def calculate(self, employee):
          return employee.salary * 1.1
  ```

### 2. **Markdown Documentation**
- Each design pattern has a corresponding `.md` file explaining the principle.
- Example: `single_responsiblility_principle.md` includes examples and benefits.

### 3. **Naming Conventions**
- Use descriptive names for files and classes.
- Example: `single_responsiblility_principle.py` clearly indicates its purpose.

---

## 🔗 Integration Points

### 1. **External Libraries**
- Common libraries include:
  - `abc` for abstract base classes.
  - `enum` for enumerations.
  - `pandas` for data manipulation.

### 2. **Cross-Component Communication**
- Dockerized apps use REST APIs for communication between frontend and backend.
- Example: React frontend in `docker_multi_container_app/frontend/` communicates with backend services.

---

## 🚀 Tips for AI Agents

1. **Understand the Context**: Read the `.md` files to understand the "why" behind the code.
2. **Follow Existing Patterns**: Maintain consistency with the SOLID examples.
3. **Be Modular**: Write reusable, single-purpose classes and functions.
4. **Document Your Code**: Add docstrings to explain the purpose of classes and methods.

---

For any questions or clarifications, refer to the examples in the `design_patterns/` directory. Happy coding! 🎉