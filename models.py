from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

db_url = "sqlite:///database.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# association table for instances
class InstancesHierarchy(Base):
    __tablename__ =  'instances_hierarchy'
    id = Column(Integer, primary_key=True)

    is_part_of_id = Column(Integer, ForeignKey('instances.id'))
    has_id = Column(Integer, ForeignKey('instances.id'))
 

class InstancesLinks(Base):
    __tablename__ =  'instances_links'
    id = Column(Integer, primary_key=True)
    original = Column(Integer, ForeignKey('instances.id'))
    remade = Column(Integer, ForeignKey('instances.id'))
    relationship_essence = Column(String)     


# class for abstract work 
class Work(Base):
    """ Declarative Base for an abstract work. 
    Can have multiple instances.  

    Attributes:
        id (int): Unique identifier of the work
        original title (str, optional): Title of the first instance of the work 
        original author (str, optional): Author of the first instance of the work 

    """

    # name of the table
    __tablename__ = 'works'

    id = Column('id', Integer, primary_key=True,  autoincrement=True)
    original_title = Column('original_title', String)
    original_author = Column('original_author', String)

    instances = relationship('Instance', back_populates="work")#

    def __init__(self, id, original_title = None, original_author = None):
        """Initializes the Work with the provided id, original title (optional), and original author (optional).

        Args:
            id (int): Unique identifier of the work
            original title (str, optional): Title of the first instance of the work 
            original author (str, optional): Author of the first instance of the work 
        """
        self.id = id
        self.original_title = original_title
        self.original_author = original_author

    def __repr__(self):
        return f"{self.id} {self.original_title} {self.original_author}"
        
# class for work instances         
class Instance(Base):
    """ Declarative Base for an instance of the work. 
    Has a link to one abstract work.   

    Attributes:
        id (int): Unique identifier of the instance
        work_id (int): Unique identifier of the work

        title (str, optional): Title of the first instance of the work 
        author (str, optional): Author of the first instance of the work 


    """

    # name of the table
    __tablename__ = 'instances'

    id = Column('id', Integer, primary_key=True,  autoincrement=True)
    work_id = Column(Integer, ForeignKey('works.id'))
    
    title = Column('title', String)
    author = Column('author', String)

    first_published = Column('first_published', Date) 
    relationship_essence = Column('relationship', String) 
    art_form = Column('art_form', String)
    genre = Column('genre', String)
    sub_genre = Column('sub_genre', String)
    note = Column('note', String)


    work = relationship('Work', back_populates="instances")

    has = relationship('Instance', secondary='instances_hierarchy', 
                        primaryjoin='InstancesHierarchy.is_part_of_id == Instance.id',
                        secondaryjoin='InstancesHierarchy.has_id == Instance.id',
                        backref="is_part_of")

    link = relationship('Instance', secondary='instances_links', 
                        primaryjoin='InstancesLinks.original == Instance.id',
                        secondaryjoin='InstancesLinks.remade == Instance.id',
                        backref="linked")

    def __init__(self, id , work_id, title = None, author = None, first_published = None, art_form = None, genre = None , sub_genre = None, note = None):
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


          