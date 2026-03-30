# Strategy Pattern — Question 3 (Hard)

## Problem: ML Model Pipeline with Interchangeable Components

Build a machine learning pipeline where each stage (preprocessing, feature extraction, model, evaluation) is a swappable strategy.

### Requirements

#### Strategies

```python
class Preprocessor(ABC):
    def transform(self, data: list[dict]) -> list[dict]: ...

class FeatureExtractor(ABC):
    def extract(self, data: list[dict]) -> list[list[float]]: ...

class Model(ABC):
    def train(self, features: list[list[float]], labels: list) -> None: ...
    def predict(self, features: list[list[float]]) -> list: ...

class Evaluator(ABC):
    def evaluate(self, predictions: list, actuals: list) -> dict: ...
```

#### Concrete Strategies

Preprocessors: `StandardScaler`, `MinMaxNormalizer`, `LogTransformer`  
Feature Extractors: `ManualFeatureExtractor(columns)`, `PCAExtractor(n_components)`  
Models: `LinearRegressionModel`, `DecisionTreeModel`, `KNNModel`  
Evaluators: `RMSEEvaluator`, `AccuracyEvaluator`, `F1Evaluator`

#### Pipeline Context

```python
class MLPipeline:
    def __init__(
        self,
        preprocessor: Preprocessor,
        feature_extractor: FeatureExtractor,
        model: Model,
        evaluator: Evaluator,
    ): ...
    
    def run(self, train_data, test_data, label_column) -> PipelineResult: ...
```

### Expected Usage

```python
# Experiment 1: Simple linear regression
pipeline1 = MLPipeline(
    preprocessor=StandardScaler(),
    feature_extractor=ManualFeatureExtractor(["age", "income"]),
    model=LinearRegressionModel(),
    evaluator=RMSEEvaluator(),
)
result1 = pipeline1.run(train_data, test_data, "price")

# Experiment 2: Swap strategies for a different approach
pipeline2 = MLPipeline(
    preprocessor=MinMaxNormalizer(),
    feature_extractor=PCAExtractor(n_components=3),
    model=KNNModel(k=5),
    evaluator=AccuracyEvaluator(),
)
result2 = pipeline2.run(train_data, test_data, "category")

# Compare
print(f"Experiment 1 (Linear): {result1.metrics}")
print(f"Experiment 2 (KNN):    {result2.metrics}")
```

### Bonus: Grid Search

```python
class GridSearch:
    """Try all combinations of strategies and find the best."""
    def __init__(self, preprocessors, extractors, models, evaluators): ...
    def run(self, train_data, test_data, label_column) -> list[PipelineResult]: ...
    def best(self) -> PipelineResult: ...
```

### Constraints

- All models use the same simple interface (train + predict) — no leaking implementation details.
- Simulated data and simple math is fine (no need for real ML libraries).
- `PipelineResult` includes: strategy names, metrics dict, training time.
- GridSearch tries ALL combinations and returns sorted results.

### Think About

- How does this compare to scikit-learn's Pipeline + GridSearchCV?
- When would you switch from Strategy to Plugin/Registry pattern?
- What's the difference between Strategy and Template Method here?
