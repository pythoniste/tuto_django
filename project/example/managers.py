from django.db.models import Manager


raw_category_tree_pks_sql = """
    WITH RECURSIVE category_tree AS (
        SELECT
            id,
            ARRAY[id] AS path
        FROM example_category
        WHERE parent_id IS NULL

        UNION ALL

        SELECT
            c.id,
            ct.path || c.id AS path
        FROM example_category c
        INNER JOIN category_tree ct ON c.parent_id = ct.id
    )
    SELECT id FROM category_tree ORDER BY path;
"""


raw_category_tree_sql = """
        WITH RECURSIVE category_tree AS (
            SELECT
                id,
                label,
                parent_id,
                1 AS level,
                ARRAY[id] AS path
            FROM example_category
            WHERE parent_id IS NULL

            UNION ALL

            SELECT
                c.id,
                c.label,
                c.parent_id,
                ct.level + 1 AS level,
                ct.path || c.id AS path
            FROM example_category c
            INNER JOIN category_tree ct ON c.parent_id = ct.id
        )
        SELECT * FROM category_tree ORDER BY path;
    """

class CategoryManager(Manager):
    def tree_pks(self):
        return [c.pk for c in self.raw(raw_category_tree_pks_sql)]

    def tree(self):
        return list(self.raw(raw_category_tree_sql))
