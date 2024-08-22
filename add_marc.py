# Add libraries 
import pandas as pd
from pymarc import MARCReader
from add_values import add_work, add_instance
from models import Work, Instance, InstancesHierarchy, session
import datetime
import re

genres = {'povídka': 'j',
          'soubor': 'j',
          'román': 'f',
          'esej': 'e',
          'báseň': 'p',
          'drama': 'd'}


database = 'data/marc_it.mrc'


def replace_characters(text):
    corrected_text = re.sub(r'á|a\s*́', 'á', text)
    corrected_text = re.sub(r'é|e\s*́', 'é', corrected_text)
    corrected_text = re.sub(r'í|i\s*́', 'í', corrected_text)
    corrected_text = re.sub(r'ó|o\s*́', 'ó', corrected_text)
    corrected_text = re.sub(r'ú|u\s*́', 'ú', corrected_text)
    corrected_text = re.sub(r'ý|y\s*́', 'ý', corrected_text)
    corrected_text = re.sub(r'ě|e\s*̌', 'ě', corrected_text)
    corrected_text = re.sub(r'š|s\s*̌', 'š', corrected_text)
    corrected_text = re.sub(r'č|c\s*̌', 'č', corrected_text)
    corrected_text = re.sub(r'ř|r\s*̌', 'ř', corrected_text)
    corrected_text = re.sub(r'ž|z\s*̌', 'ž', corrected_text)
    corrected_text = re.sub(r'ť|t\s*̌', 'ť', corrected_text)
    corrected_text = re.sub(r'ů|u\s*̊', 'ů', corrected_text)
    return corrected_text


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

                up_down = False
                genre  = None  
                for field_994 in record.get_fields('994'):
                    if field_994['a'] == 'UP':
                        up_down = 'UP'
                        genre = 'povídka'
                        connect = int(field_994['b'][2:])
                    elif field_994['a'] == 'DN':   
                        genre = 'soubor'
                        up_down = 'DN'                          
                    break    

                try:

                    typ = record.leader[7]

                    title_orig = None
                    for field_240 in record.get_fields('240'):
                        title_orig = replace_characters(field_240['a']) # TODO: ADD POSIBILITY WITH NO ORIGINAL TITLE
                    
                    author_name = field['a']
                    author_code = field['7']
                    target_audience = record['008'].data[22]
                    form_od_item = record['008'].data[23]
                    literary_form = record['008'].data[34]

                    works = session.query(Work).filter_by(original_title = title_orig).all()
                    title_trl = record['245']['a'].strip('/').strip()
                    
                    instance_exists = session.query(Instance).filter_by(title = title_trl).first()
                    first_published = datetime.date(int(record['264']['c']), 1, 1)
                
                    print('Instances')

                    if instance_exists == None:
                        if len(works) > 1: 
                            for work in works:
                                for instance in work.instances: 
                                    if instance.first_published < first_published:   # TODO: ADD CONDITIONS
                                        if genres[instance.genre] == literary_form or genre == instance.genre or literary_form == '-':
                                                
                                                found = True 
                                                trans_instance = add_instance(work_id = work.id, author_name = author_name, author_code = author_code, title = title_trl, genre = genre, art_form= 'literatura', first_published= first_published, relationship=False)
                                                trans_instance.relationship_essence = 'překlad'
                                                work.instances.append(trans_instance)

                                                if up_down == 'UP':
                                                    instances_association = InstancesHierarchy(is_part_of_id=trans_instance.id, has_id=connect)
                                                    session.add(instances_association)

                                                session.add(trans_instance)
                                                break
                                if found : break    

                        elif len(works) == 1:      # TODO: ADD UP-DOWN RELATIONSHIPS TO INSTANCES
                            work = works[0]

                            trans_instance = add_instance(work_id = work.id, author_name = author_name, author_code = author_code, title = title_trl, genre = genre, art_form= 'literatura', first_published= first_published, relationship=False)
                            trans_instance.relationship_essence = 'překlad'
                            work.instances.append(trans_instance)

                            if up_down == 'UP':
                                instances_association = InstancesHierarchy(is_part_of_id=trans_instance.id, has_id=connect)
                                session.add(instances_association)

                            session.add(trans_instance)
                        else: # ADD NEW WORK AND INSTANCE 
                            id_number  = int(record['001'].data[2:])
                            work = add_work(author_name = author_name, author_code = author_code, title = title_trl, id_number = id_number )
    

                            trans_instance = add_instance(id = id_number, author_name = author_name, author_code = author_code, title = title_trl, genre = genre, art_form= 'literatura', first_published= first_published, relationship=False)
                            trans_instance.relationship_essence = 'překlad'

                            if up_down == 'UP':
                                instances_association = InstancesHierarchy(is_part_of_id=trans_instance.id, has_id=connect)
                                session.add(instances_association)

                            work.instances.append(trans_instance)
                            session.add(work)
                            session.add(trans_instance)




                    print(record)
                except:
                    print(record)    
session.commit()                