#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2021 Snowflake Computing Inc. All right reserved.
#
from src.snowflake.snowpark.internal.analyzer.analyzer_package import AnalyzerPackage
from src.snowflake.snowpark.internal.sp_expressions import Expression as SPExpression, \
    UnresolvedAttribute as SPUnresolvedAttribute, UnresolvedStar as SPUnresolvedStar, \
    UnresolvedAlias as SPUnresolvedAlias, NamedExpression as SPNamedExpression, Alias as SPAlias, \
    Literal as SPLiteral, EqualTo as SPEqualTo, NotEqualTo as SPNotEqualTo, GreaterThan as SPGreaterThan, \
    LessThan as SPLessThan, GreaterThanOrEqual as SPGreaterThanOrEqual, LessThanOrEqual as SPLessThanOrEqual, \
    EqualNullSafe as SPEqualNullSafe, And as SPAnd, Or as SPOr, UnaryMinus as SPUnaryMinus, Not as SPNot, \
    IsNaN as SPIsNaN, IsNull as SPIsNull, IsNotNull as SPIsNotNull, Add as SPAdd, Subtract as SPSubtract, \
    Multiply as SPMultiply, Divide as SPDivide, Remainder as SPRemainder, Pow as SPPow, BitwiseAnd as SPBitwiseAnd, \
    BitwiseOr as SPBitwiseOr, BitwiseXor as SPBitwiseXor
from typing import (
    Optional,
)


class Column:

    def __init__(self, expr):
        if type(expr) == str:
            self.expression = self.__get_expr(expr)
        elif isinstance(expr, SPExpression):
            self.expression = expr
        else:
            raise Exception("Column ctor takes only str or expression.")

    # TODO make subscriptable

    # Overload operators.
    def __eq__(self, other) -> 'Column':
        right = self.__to_expr(other)
        return self.with_expr(SPEqualTo(self.expression, right))

    def __ne__(self, other) -> 'Column':
        right = self.__to_expr(other)
        return self.with_expr(SPNotEqualTo(self.expression, right))

    def __gt__(self, other) -> 'Column':
        return self.with_expr(SPGreaterThan(self.expression, self.__to_expr(other)))

    def __lt__(self, other) -> 'Column':
        return self.with_expr(SPLessThan(self.expression, self.__to_expr(other)))

    def __ge__(self, other) -> 'Column':
        return self.with_expr(SPGreaterThanOrEqual(self.expression, self.__to_expr(other)))

    def __le__(self, other) -> 'Column':
        return self.with_expr(SPLessThanOrEqual(self.expression, self.__to_expr(other)))

    def __add__(self, other) -> 'Column':
        return self.with_expr(SPAdd(self.expression, self.__to_expr(other)))

    def __radd__(self, other) -> 'Column':
        return self.with_expr(SPAdd(self.__to_expr(other), self.expression))

    def __sub__(self, other) -> 'Column':
        return self.with_expr(SPSubtract(self.expression, self.__to_expr(other)))

    def __rsub__(self, other) -> 'Column':
        return self.with_expr(SPSubtract(self.__to_expr(other), self.expression))

    def __mul__(self, other) -> 'Column':
        return self.with_expr(SPMultiply(self.expression, self.__to_expr(other)))

    def __rmul__(self, other) -> 'Column':
        return self.with_expr(SPMultiply(self.__to_expr(other), self.expression))

    def __truediv__(self, other) -> 'Column':
        return self.with_expr(SPDivide(self.expression, self.__to_expr(other)))

    def __rtruediv__(self, other) -> 'Column':
        return self.with_expr(SPDivide(self.__to_expr(other), self.expression))

    def __mod__(self, other) -> 'Column':
        return self.with_expr(SPRemainder(self.expression, self.__to_expr(other)))

    def __rmod__(self, other) -> 'Column':
        return self.with_expr(SPRemainder(self.__to_expr(other), self.expression))

    def __pow__(self, other) -> 'Column':
        return self.with_expr(SPPow(self.expression, self.__to_expr(other)))

    def __rpow__(self, other) -> 'Column':
        return self.with_expr(SPPow(self.__to_expr(other), self.expression))

    def bitand(self, other) -> 'Column':
        return self.with_expr(SPBitwiseAnd(self.__to_expr(other), self.expression))

    def bitor(self, other) -> 'Column':
        return self.with_expr(SPBitwiseOr(self.__to_expr(other), self.expression))

    def bitxor(self, other) -> 'Column':
        return self.with_expr(SPBitwiseXor(self.__to_expr(other), self.expression))

    def __neg__(self) -> 'Column':
        return self.with_expr(SPUnaryMinus(self.expression))

    def equal_null(self, other) -> 'Column':
        return self.with_expr(SPEqualNullSafe(self.expression, self.__to_expr(other)))

    def equal_nan(self) -> 'Column':
        return self.with_expr(SPIsNaN(self.expression))

    def is_null(self) -> 'Column':
        return self.with_expr(SPIsNull(self.expression))

    def is_not_null(self) -> 'Column':
        return self.with_expr(SPIsNotNull(self.expression))

    # `and, or, not` cannot be overloaded in Python, so use bitwise operators as boolean operators
    def __and__(self, other) -> 'Column':
        return self.with_expr(SPAnd(self.expression, self.__to_expr(other)))

    def __rand__(self, other) -> 'Column':
        return self.with_expr(SPAnd(self.__to_expr(other), self.expression))

    def __or__(self, other) -> 'Column':
        return self.with_expr(SPOr(self.expression, self.__to_expr(other)))

    def __ror__(self, other) -> 'Column':
        return self.with_expr(SPAnd(self.__to_expr(other), self.expression))

    def __invert__(self) -> 'Column':
        return self.with_expr(SPNot(self.expression))

    def named(self) -> SPExpression:
        if isinstance(self.expression, SPNamedExpression):
            return self.expression
        else:
            return SPUnresolvedAlias(self.expression, None)

    def getName(self) -> Optional[str]:
        """Returns the column name if it has one."""
        return self.expression.name if isinstance(self.expression, SPNamedExpression) else None

    # TODO revisit toString() functionality
    def __repr__(self):
        return f"Column[{self.expression.toString()}]"

    def as_(self, alias: str) -> 'Column':
        """Returns a new renamed Column. Alias of [[name]]."""
        return self.name(alias)

    def alias(self, alias: str) -> 'Column':
        """Returns a new renamed Column. Alias of [[name]]."""
        return self.name(alias)

    def name(self, alias: str) -> 'Column':
        """Returns a new renamed Column."""
        return self.with_expr(SPAlias(self.expression, AnalyzerPackage.quote_name(alias)))

    @staticmethod
    def __to_expr(expr) -> SPExpression:
        if type(expr) is Column:
            return expr.expression
        # TODO revisit: instead of doing SPLit(exp).expr we check if SPExpression and return that
        # or crate an SPLiteral expression
        elif isinstance(expr, SPExpression):
            return expr
        else:
            return SPLiteral.create(expr)

    @classmethod
    def expr(cls, e):
        return cls(SPUnresolvedAttribute.quoted(e))

    @staticmethod
    def __get_expr(name):
        if name == "*":
            return SPUnresolvedStar(None)
        elif name.endswith('.*'):
            parts = SPUnresolvedAttribute.parse_attribute_name(name[0:-2])
            return SPUnresolvedStar(parts)
        else:
            return SPUnresolvedAttribute.quoted(name)

    @classmethod
    def with_expr(cls, new_expr):
        return cls(new_expr)

# TODO
# class CaseExp(Column):
#