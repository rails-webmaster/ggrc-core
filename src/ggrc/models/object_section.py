# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import Base, Timeboxed
from .reflection import PublishOnly

class ObjectSection(Base, Timeboxed, db.Model):
  __tablename__ = 'object_sections'

  role = db.Column(db.String)
  notes = db.Column(db.Text)
  section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

  # TODO: Polymorphic relationship
  sectionable_id = db.Column(db.Integer)
  sectionable_type = db.Column(db.String)

  @property
  def sectionable_attr(self):
    return '{0}_sectionable'.format(self.sectionable_type)

  @property
  def sectionable(self):
    return getattr(self, self.sectionable_attr)

  @sectionable.setter
  def sectionable(self, value):
    self.sectionable_id = value.id if value is not None else None
    self.sectionable_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.sectionable_attr, value)

  _publish_attrs = [
      'role',
      'notes',
      'section',
      'sectionable',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(ObjectSection, cls).eager_query()
    return query.options(
        orm.subqueryload('section'))

class Sectionable(object):
  @declared_attr
  def object_sections(cls):
    cls.sections = association_proxy(
        'object_sections', 'section',
        creator=lambda section: ObjectSection(
            section=section,
            modified_by_id=1,
            sectionable_type=cls.__name__,
            )
        )
    joinstr = 'and_(foreign(ObjectSection.sectionable_id) == {type}.id, '\
                   'foreign(ObjectSection.sectionable_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'ObjectSection',
        primaryjoin=joinstr,
        backref='{0}_sectionable'.format(cls.__name__),
        )

  _publish_attrs = [
      PublishOnly('sections'),
      'object_sections',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Sectionable, cls).eager_query()
    return query.options(orm.subqueryload_all('object_sections.section'))