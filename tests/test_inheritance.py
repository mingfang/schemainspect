from sqlbag import S

from schemainspect import get_inspector

INHERITANCE = """

create table normal (id integer);

create table parent (t timestamp);

create table child (a integer, b integer) inherits (parent);
"""


def test_inheritance(db):
    with S(db) as s:
        s.execute(INHERITANCE)

        ii = get_inspector(s)

        normal = ii.tables['"public"."normal"']
        parent = ii.tables['"public"."parent"']
        child = ii.tables['"public"."child"']

        assert list(normal.columns) == ["id"]
        assert list(parent.columns) == ["t"]
        assert list(child.columns) == "t a b".split()

        assert normal.columns["id"].is_inherited is False
        assert parent.columns["t"].is_inherited is False
        assert child.columns["t"].is_inherited is True

        for c in "a b".split():
            child.columns[c].is_inherited is False

        assert parent.dependents == ['"public"."child"']
        assert child.dependent_on == ['"public"."parent"']