        deposit2 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 50)

        composite: list[BankAccountCommand] = CompositeBankAccountCommand(
            [deposit1, deposit2]
        )
        composite.invoke()
        print(ba)
        composite.undo()
        print(ba)

    def test_transfer_fail(self):
        ba1 = BankAccount(100)
        ba2 = BankAccount()

        a