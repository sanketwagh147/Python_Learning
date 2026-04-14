from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ExpenseApprovalContext:
    """Data available when an employee requests expense approval."""

    role: str
    department: str
    amount: float
    is_budget_owner: bool = False


class ApprovalRule(ABC):
    """Base interface for all approval policy rules."""

    @abstractmethod
    def interpret(self, context: ExpenseApprovalContext) -> bool:
        raise NotImplementedError

    def __bool__(self) -> bool:
        raise TypeError("Use '&' and '|' to compose ApprovalRule objects, not 'and'/'or'.")

    def __and__(self, other: ApprovalRule) -> ApprovalRule:
        if not isinstance(other, ApprovalRule):
            return NotImplemented
        return AndRule(self, other)

    def __or__(self, other: ApprovalRule) -> ApprovalRule:
        if not isinstance(other, ApprovalRule):
            return NotImplemented
        return OrRule(self, other)


@dataclass(frozen=True)
class RoleIs(ApprovalRule):
    role: str

    def interpret(self, context: ExpenseApprovalContext) -> bool:
        return context.role == self.role


@dataclass(frozen=True)
class DepartmentIs(ApprovalRule):
    department: str

    def interpret(self, context: ExpenseApprovalContext) -> bool:
        return context.department == self.department


@dataclass(frozen=True)
class AmountLessThan(ApprovalRule):
    limit: float

    def interpret(self, context: ExpenseApprovalContext) -> bool:
        return context.amount < self.limit


class BudgetOwnerRule(ApprovalRule):
    def interpret(self, context: ExpenseApprovalContext) -> bool:
        return context.is_budget_owner


@dataclass(frozen=True)
class AndRule(ApprovalRule):
    left: ApprovalRule
    right: ApprovalRule

    def interpret(self, context: ExpenseApprovalContext) -> bool:
        return self.left.interpret(context) and self.right.interpret(context)


@dataclass(frozen=True)
class OrRule(ApprovalRule):
    left: ApprovalRule
    right: ApprovalRule

    def interpret(self, context: ExpenseApprovalContext) -> bool:
        return self.left.interpret(context) or self.right.interpret(context)


def build_expense_approval_policy() -> ApprovalRule:
    """Approve an expense when any allowed business path evaluates to true."""

    return (
        RoleIs("admin")
        | BudgetOwnerRule()
        | (RoleIs("manager") & DepartmentIs("finance") & AmountLessThan(10_000))
        | (RoleIs("manager") & DepartmentIs("finance") & AmountLessThan(10_000))
    )


def main() -> None:
    policy = build_expense_approval_policy()
    requests = [
        ExpenseApprovalContext(role="admin", department="sales", amount=25_000),
        ExpenseApprovalContext(role="manager", department="finance", amount=8_500),
        ExpenseApprovalContext(role="manager", department="finance", amount=14_500),
        ExpenseApprovalContext(role="analyst", department="engineering", amount=12_000, is_budget_owner=True),
        ExpenseApprovalContext(role="analyst", department="engineering", amount=2_000),
    ]

    for request in requests:
        can_approve = policy.interpret(request)
        print(
            f"role={request.role:8} dept={request.department:11} "
            f"amount={request.amount:8.0f} budget_owner={request.is_budget_owner:<5} "
            f"-> approved={can_approve}"
        )


if __name__ == "__main__":
    main()