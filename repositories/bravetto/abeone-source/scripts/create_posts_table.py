import asyncio
from sqlalchemy import text
from app.core.database import get_db

async def create_posts_table():
    async for session in get_db():
        try:
            # Create the posts table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL NOT NULL,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                summary VARCHAR(500),
                is_published BOOLEAN NOT NULL,
                is_featured BOOLEAN NOT NULL,
                slug VARCHAR(255),
                tags VARCHAR(500),
                view_count INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
                published_at TIMESTAMP WITH TIME ZONE,
                PRIMARY KEY (id),
                CONSTRAINT ck_posts_title_length CHECK (length(title) >= 1),
                CONSTRAINT ck_posts_content_length CHECK (length(content) >= 10),
                CONSTRAINT ck_posts_view_count_positive CHECK (view_count >= 0),
                FOREIGN KEY(author_id) REFERENCES users (id)
            );
            """

            await session.execute(text(create_table_sql))
            await session.commit()
            print("Posts table created successfully")

            # Create indexes
            index_queries = [
                "CREATE INDEX IF NOT EXISTS ix_posts_slug ON posts (slug);",
                "CREATE UNIQUE INDEX IF NOT EXISTS ix_posts_slug ON posts (slug);",
            ]

            for query in index_queries:
                try:
                    await session.execute(text(query))
                    print(f"Index created: {query[:50]}...")
                except Exception as e:
                    print(f"Index creation failed: {e}")

            await session.commit()
            print("All posts table operations completed")

        except Exception as e:
            print(f"Error creating posts table: {e}")
            await session.rollback()
        finally:
            await session.close()
            break

if __name__ == "__main__":
    asyncio.run(create_posts_table())
