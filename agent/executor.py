import ast

import pandas as pd


# ============================================================
# ALLOWED AST NODES
# ============================================================

ALLOWED_NODES = (
    ast.Module,
    ast.Assign,
    ast.Expr,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.Attribute,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Call,
    ast.keyword,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.List,
    ast.Tuple,
    ast.Dict,
)


# ============================================================
# BLOCKED NAMES
# ============================================================

BLOCKED_NAMES = {
    "os",
    "sys",
    "subprocess",
    "socket",
    "shutil",
    "pathlib",
    "requests",
    "urllib",
    "http",
    "eval",
    "exec",
    "compile",
    "open",
    "__import__",
}


# ============================================================
# VALIDATE GENERATED CODE
# ============================================================

def validate_code(code):
    """
    Performs basic AST validation before execution.
    """

    try:

        tree = ast.parse(
            code,
            mode="exec",
        )

    except SyntaxError as e:

        raise ValueError(
            f"Generated code contains invalid Python: {e}"
        )


    for node in ast.walk(tree):

        if not isinstance(
            node,
            ALLOWED_NODES,
        ):

            raise ValueError(
                f"Unsupported Python operation: "
                f"{type(node).__name__}"
            )


        if isinstance(
            node,
            ast.Name,
        ):

            if node.id in BLOCKED_NAMES:

                raise ValueError(
                    f"Blocked operation: {node.id}"
                )


        if isinstance(
            node,
            ast.Attribute,
        ):

            if node.attr.startswith("__"):

                raise ValueError(
                    "Private attributes are not allowed."
                )


    return True


# ============================================================
# EXECUTE GENERATED CODE
# ============================================================

def execute_analysis(
    code,
    df,
):
    """
    Executes validated Pandas analysis code.

    The generated code must create a variable
    called `result`.
    """

    validate_code(
        code
    )


    safe_globals = {
        "__builtins__": {},
        "pd": pd,
    }


    safe_locals = {
        "df": df.copy(),
    }


    exec(
        code,
        safe_globals,
        safe_locals,
    )


    if "result" not in safe_locals:

        raise ValueError(
            "The generated analysis did not "
            "produce a `result` variable."
        )


    return safe_locals["result"]