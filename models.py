from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, CHAR, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

db_url = "sqlite:///database.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# association table for work_instances
class WorkInstancesAssociation(Base):
    __tablename__ =  'instances_association'
    id = Column(Integer, primary_key=True)

    is_part_of_id = Column(Integer, ForeignKey('work_instances.id'))
    has_id = Column(Integer, ForeignKey('work_instances.id'))
 

class WorkInstancesLinks(Base):
    __tablename__ =  'instances_links'
    id = Column(Integer, primary_key=True)
    original = Column(Integer, ForeignKey('work_instances.id'))
    remade = Column(Integer, ForeignKey('work_instances.id'))
    relationship_essence = Column(String)     

# class for abstract work 
class Work(Base):

    # name of the table
    __tablename__ = 'works'

    id = Column('id', Integer, primary_key=True,  autoincrement=True)
    original_title = Column('original_title', String)
    original_author = Column('original_author', String)

    instances = relationship('WorkInstance', back_populates="work")#

    def __init__(self, id, original_title = None, original_author = None):
        self.id = id
        self.original_title = original_title
        self.original_author = original_author

    def __repr__(self):
        return f"{self.id} {self.original_title} {self.original_author}"
        
# class for work instances         
class WorkInstance(Base):

    # name of the table
    __tablename__ = 'work_instances'

    id = Column('id', Integer, primary_key=True,  autoincrement=True)
    work_id = Column(Integer, ForeignKey('works.id'))
    
    title = Column('title', String)
    author = Column('author', String)

    first_published = Column('first_published', String) 
    relationship_essence = Column('relationship', String) 
    art_form = Column('art_form', String)
    genre = Column('genre', String)
    sub_genre = Column('sub_genre', String)
    note = Column('note', String)


    work = relationship('Work', back_populates="instances")

    has = relationship('WorkInstance', secondary='instances_association', 
                        primaryjoin='WorkInstancesAssociation.is_part_of_id == WorkInstance.id',
                        secondaryjoin='WorkInstancesAssociation.has_id == WorkInstance.id',
                        backref="is_part_of")

    link = relationship('WorkInstance', secondary='instances_links', 
                        primaryjoin='WorkInstancesLinks.original == WorkInstance.id',
                        secondaryjoin='WorkInstancesLinks.remade == WorkInstance.id',
                        backref="linked")

    def __init__(self, id , work_id, title = None, author = None, first_published = datetime.datetime.now(), art_form = None, genre = None , sub_genre = None, note = None):
        self.id  = id 
        self.work_id = work_id
        self.title = title
        self.author = author
        self.first_published = first_published
        self.art_form = art_form
        self.genre = genre
        self.sub_genre = sub_genre
        self.note = note

Base.metadata.create_all(engine)


          