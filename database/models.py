from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CrawlingUrl(Base):
    __tablename__ = "crawling_urls"

    url = Column(String, primary_key=True)
    instock = Column(Boolean, default=False)
    stockdata = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<CrawlingUrl(url='{self.url}', instock={self.instock})>"