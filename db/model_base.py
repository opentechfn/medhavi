from oslo_db.sqlalchemy import models
from sqlalchemy.ext import declarative
from sqlalchemy.orm import attributes


class _BaseClass(models.ModelBase):
    """Base class for all SQLAlchemy DB Models."""

    def to_dict(self):
        """sqlalchemy based automatic to_dict method."""
        d = {}

        # if a column is unloaded at this point, it is
        # probably deferred. We do not want to access it
        # here and thereby cause it to load...
        unloaded = attributes.instance_state(self).unloaded

        columns = self.__table__.columns

        for col in columns:
            if col.name not in unloaded:
                d[col.name] = getattr(self, col.name)

        return d


ModelBase = declarative.declarative_base(cls=_BaseClass)
