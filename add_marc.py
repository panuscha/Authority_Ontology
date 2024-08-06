# Add libraries 
import pandas as pd
from pymarc import MARCReader
from add_values import add_work, add_instance
from models import Work, Instance, InstancesHierarchy, session
import datetime


database = 'data/marc_fin.mrc'

# Open file
with open(database, 'rb') as data:
    
    # Read marc file
    reader = MARCReader(data)

    # # Iterate through records in marc file 
    # for i, record in enumerate(reader):
    #     for field in record.get_fields('100'):
    #         if field['a'] == 'Hrabal, Bohumil':
                
    #             type = record.leader[7]
    #             title_orig = record['240']['a']
    #             author = '{} ({})'.format(field['a'], field['7']) 
    #             instances = session.query(Instance).filter_by(title = title_orig).all()
    #             title_trl = record['245']['a']
    #             instance_exists = session.query(Instance).filter_by(title = title_trl).first()
    #             print('Instances')

    #             UP = False
    #             DN = False

    #             for field in record.get_fields('994'):
    #                 UP = True if 'UP' in field['a'] else False  
    #                 DN = True if 'DN' in field['a'] else False  

    #             if instance_exists == None:
    #                 for instance in instances:
                        
    #                     is_part_of = instance.is_part_of
    #                     has = instance.has

    #                     if (len(has) == 0 and not UP) and (len(is_part_of) == 0 and not DN) :
    
    #                         work = instance.work
    #                         first_published = datetime.date(int(record['264']['c']), 1, 1)
                        
    #                         trans_instance = add_instance(author = author, title = title_trl, art_form= 'literatura', first_published= first_published, relationship=False)
    #                         trans_instance.relationship_essence = 'překlad'
    #                         work.instances.append(trans_instance)
    #                         session.add(trans_instance)
                       

    #             print(record)

        # Iterate through records in marc file 
    for i, record in enumerate(reader):
        for field in record.get_fields('100'):
            if field['a'] == 'Hrabal, Bohumil':
                
                type = record.leader[7]
                title_orig = record['240']['a']
                author = '{} ({})'.format(field['a'], field['7']) 
                works = session.query(Work).filter_by(original_title = title_orig).all()
                title_trl = record['245']['a']
                instance_exists = session.query(Instance).filter_by(title = title_trl).first()
                first_published = datetime.date(int(record['264']['c']), 1, 1)
                
                print('Instances')

                if instance_exists == None:
                    if len(works) > 1: 
                        for work in works:
                            for instance in work.instances: 
                                if instance.first_published < first_published: # TODO: ADD CONDITIONS 
                                    trans_instance = add_instance(author = author, title = title_trl, art_form= 'literatura', first_published= first_published, relationship=False)
                                    trans_instance.relationship_essence = 'překlad'
                                    work.instances.append(trans_instance)
                                    session.add(trans_instance)
                                    break

                    else:     
                        work = works[0]

                        trans_instance = add_instance(author = author, title = title_trl, art_form= 'literatura', first_published= first_published, relationship=False)
                        trans_instance.relationship_essence = 'překlad'
                        work.instances.append(trans_instance)
                        session.add(trans_instance)
                       

                print(record)
session.commit()                