# Step 1: Define the Visitor Interface
class SQLVisitor:
    def visit_select(self, select_query):
        pass

    def visit_table(self, table):
        pass

    def visit_where(self, where):
        pass


# Step 2: Define SQL AST Nodes (Expressions)
class SQLExpression:
    def accept(self, visitor):
        method_name = f"visit_{self.__class__.__name__.lower()}"
        return getattr(visitor, method_name)(self)


class Table(SQLExpression):
    def __init__(self, name):
        self.name = name

    # def accept(self, visitor):
    #     return visitor.visit_table(self)


class Where(SQLExpression):
    def __init__(self, column, value):
        self.column = column
        self.value = value

    # def accept(self, visitor):
    #     return visitor.visit_where(self)


class Select(SQLExpression):
    def __init__(self, table, where=None):
        self.table = table
        self.where = where

    # def accept(self, visitor):
    #     return visitor.visit_select(self)


# Step 3: Implement the Query Builder Visitor
class SQLQueryBuilder(SQLVisitor):
    def visit_table(self, table):
        return f"FROM {table.name}"

    def visit_where(self, where):
        return f"WHERE {where.column} = '{where.value}'"

    def visit_select(self, select_query):
        query = "SELECT * "
        query += select_query.table.accept(self)
        if select_query.where:
            query += " " + select_query.where.accept(self)
        return query


# Step 4: Build and Execute a Query
if __name__ == "__main__":
    # Construct an SQL Query AST
    table = Table("users")
    condition = Where("age", 30)
    query = Select(table, condition)

    # Use Visitor to build SQL
    query_builder = SQLQueryBuilder()
    sql_string = query.accept(query_builder)

    print(sql_string)  # Output: SELECT * FROM users WHERE age = '30'
