# 07. Software Engineering Best Practices & Behavioral

## 🧪 1. Testing Strategies (Deep Dive)

### Types of Tests
- **Unit Tests:** Test individual functions/classes in isolation. Fast. Mocks dependencies.
- **Integration Tests:** Test how modules interact (e.g., API calling DB). Slower. Real dependencies (often via Docker containers).
- **End-to-End (E2E) Tests:** Simulates real user behavior. Very slow. Flaky.

### Pytest Fundamentals
The industry standard replacement for `unittest`.
- **Fixtures:** Dependency injection for tests.
```python
import pytest

@pytest.fixture
def db_connection():
    conn = connect_db()
    yield conn  # Provide to test
    conn.close() # Cleanup after test

def test_user_creation(db_connection):
    assert create_user(db_connection, "Sanket") == True
```
- **Parametrization:** Run same test with different inputs.
```python
@pytest.mark.parametrize("input,expected", [(1, 2), (2, 4), (3, 6)])
def test_double(input, expected):
    assert input * 2 == expected
```

### Mocks & Patches
Used to isolate the System Under Test (SUT) from external dependencies (API, DB, Time).
- `unittest.mock.patch`: Replaces an object at runtime.
```python
from unittest.mock import patch

# Mocking a request to an external API
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": 1}
    
    response = my_function_calling_api()
    assert response['id'] == 1
```

### Test-Driven Development (TDD)
**Cycle:** Red -> Green -> Refactor.
1. **Red:** Write a failing test for the feature.
2. **Green:** Write the minimum code to make it pass.
3. **Refactor:** Clean up code while tests still pass.
**Benefit:** Forces design thinking, high test coverage, confidence in refactoring.

### Code Coverage
Measures what % of code is executed by tests.
- **Tools:** `pytest-cov` (Python).
- **Command:** `pytest --cov=mymodule tests/`
- **Target:** 80%+ is a good goal. 100% is often impractical.
- **Warning:** High coverage ≠ good tests. You can have 100% coverage with zero assertions.

---

## ✨ 2. Clean Code Principles

### DRY (Don't Repeat Yourself)
Avoid duplicating logic. Extract to functions/classes.

### KISS (Keep It Simple, Stupid)
Simplest solution is often best. Avoid over-engineering.

### YAGNI (You Aren't Gonna Need It)
Don't build features "just in case". Build what's needed NOW.

### Code Smells (Warning Signs)
- **Long Methods:** > 20-30 lines. Hard to read.
- **Large Classes:** Doing too much. Violates Single Responsibility.
- **Primitive Obsession:** Using primitives instead of small objects (e.g., using string for Money instead of `Money` class).
- **Feature Envy:** Method uses more data from another class than its own.
- **Dead Code:** Unused code. Delete it.

### Refactoring Techniques
- **Extract Method:** Pull code into a new function.
- **Rename:** Improve clarity of names.
- **Move Method:** To the class where it belongs.
- **Replace Magic Number with Constant:** `if status == 2` -> `if status == STATUS_APPROVED`.

---

## 🌳 3. Git & Version Control (Deep Dive)

### Branching Strategies
- **Git Flow:** `master` (prod), `develop` (integration), `feature/xyz`, `release/v1.0`, `hotfix/bug`. Strict but complex.
- **GitHub Flow:** `main` (always deployable) -> Create Branch -> PR -> Merge to `main`. Ideal for CI/CD.

### Advanced Git Commands
- `git rebase main`: Replays your commits on top of the latest main. Keeps history linear.
- `git cherry-pick <commit>`: Pick a specific commit from another branch.
- `git stash`: Temporarily store uncommitted changes.
- `git bisect`: Binary search through commit history to find the commit that introduced a bug.

### Pull Request (PR) Etiquette
- **Small PRs:** Easier to review. < 400 lines.
- **Context:** Description should explain *what*, *why*, and *how*.
- **Self-Review:** Comment on your own PR to explain tricky parts before assigning reviewers.

---

## 🧠 4. Behavioral Questions (STAR Method)

**Structure:** **S**ituation, **T**ask, **A**ction, **R**esult.

### Q1: Tell me about a time you had a conflict with a team member.
- **Goal:** collaborative resolution, not winning.
- **Example:** "My peer wanted to use library X, I wanted Y. We were stuck. I proposed we build a small POC (Proof of Concept) with both. We found X was easier to maintain. I agreed to go with X."

### Q2: Describe a challenging bug you fixed.
- **Goal:** Troubleshooting process, persistence.
- **Example:** "Production API latency spiked at 2 AM. Logs were clean. I used `git bisect` to find a recent commit. It was an N+1 query introduced in a serializer. I added `select_related` to fix it. Latency dropped 90%."

### Q3: How do you handle a missed deadline?
- **Goal:** Communication, ownership.
- **Example:** "I realized 2 days prior I wouldn't make it due to unexpected complexity. I raised it immediately in standup. We descoped a non-critical feature. We shipped the MVP on time."

### Q4: How do you perform Code Reviews?
- **Goal:** Quality gatekeeper + Mentor.
- **Points:**
  - Be kind. Comment on code, NOT the person.
  - "Nit:" for minor things (formatting).
  - Look for: Logic bugs, Security issues, Test coverage, Readability.

---

## 📊 5. Agile & Scrum (Quick Reference)

### Scrum Ceremonies
- **Sprint Planning:** Team selects items from backlog for the sprint.
- **Daily Standup:** 15 min. What did you do? What will you do? Any blockers?
- **Sprint Review:** Demo to stakeholders.
- **Retrospective:** What went well? What to improve?

### Key Concepts
- **User Story:** "As a [user], I want [feature] so that [benefit]".
- **Story Points:** Estimate effort (not time). Fibonacci: 1, 2, 3, 5, 8, 13.
- **Velocity:** Average story points completed per sprint.
- **Burndown Chart:** Visualizes remaining work vs time.

---

## 🔗 Recommended Resources

- **Testing:** [Pytest Documentation](https://docs.pytest.org/en/7.1.x/)
- **Git:** [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- **Behavioral:** [The Muse - STAR Method](https://www.themuse.com/advice/star-interview-method)
