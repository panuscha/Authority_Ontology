from models import Work, Instance, InstancesHierarchy, session
import pandas as pd 
import math 
import datetime
import re

def add_work(author_name, author_code, title, id_number):
    """Adds Work object to list work_objects

        Parameters
        ----------
        row : pandas row
            row with information about work

        work_objects : list
            list with works - Work object    

        Returns
        ------
        list
            work_objects with new element
        """
    
    return  Work(id = id_number, original_title = title, original_author_name = author_name,  original_author_code = author_code)


def add_instance(author_name = None, author_code = None, title = None, work_id = None, id = None , art_form = None, genre = None, subgenre = None, note = None, first_published = None,   relationship = False):
    """Adds WorkInstance object to list instances_objects

        Parameters
        ----------
        row : pandas row
            row with information about work instace

        instances_objects : list
            list with instances - Work Instances object 

        relationship : boolean
            True/False - add relationship essence or not       

        Returns
        ------
        list
            instances_objects with new element
        """


    instance = Instance(id = id, work_id = work_id, title = title, author_name = author_name, author_code = author_code, first_published = first_published, art_form=art_form, genre=genre, sub_genre=subgenre, note=note)

    if relationship: 
        instance.relationship_essence = relationship

    return instance

if __name__ == "__main__":
    first_row = 35

    # load pandas
    df = pd.read_excel('data/Autority děl - Hrabal.xlsx')

    df = df.iloc[first_row:]
    # TODO: multiple horizontal relationship
    #df['horizontální vazba (= patří do souboru díla)'] = df['horizontální vazba (= patří do souboru díla)'].apply(lambda x: [x] if str(x).isnumeric() else x.split()) 

    df['číslo záznamu'] = df['číslo záznamu'].apply(lambda x: int(x)) 
    df['vertikální vazba (=je součást čeho)'] = df['vertikální vazba (=je součást čeho)'].apply(lambda x: None if math.isnan(x) else int(x)) 
    df['horizontální vazba (= patří do souboru díla)'] = df['horizontální vazba (= patří do souboru díla)'].apply(lambda x: None if math.isnan(x) else int(x)) 
    df['rok vydání'] = df['rok vydání'].ffill()

    work_objects = {}
    instances_objects = {}
    used = set()


    for i, row in df.iterrows():
            
            horizontal = row['horizontální vazba (= patří do souboru díla)']
            relationship_essence = row['kvalita vazby'] 
            vertical = row['vertikální vazba (=je součást čeho)']
            id_number = row['číslo záznamu']
            

            pattern = r'(?P<name>[A-Za-z]+,\s[A-Za-z]+)\s\((?P<code>[a-zA-Z0-9]+)\)'
            found = re.search(pattern, row['autor'])

            if found:
                author_name = found.group('name')
                author_code = found.group('code')
            
            # Parameters for classes
            title = row['název']
            id_number = row['číslo záznamu']  
            art_form = row['umělecký druh']
            genre = row['žánr']
            subgenre = row['subžánr']
            note = row['poznámka']
            first_published = datetime.date(row['rok vydání'], 1, 1)
            relationship = row['kvalita vazby']

            # horizontal bond is not present 
            if horizontal not in used:
                
                
                work_object = add_work(author_name, author_code, title, id_number )
                work_objects[id_number] = work_object
                instances_object = add_instance(author_name = author_name, author_code = author_code, title = title, work_id= id_number, id = id_number, art_form= art_form, genre=genre, subgenre=subgenre, note=note , first_published= first_published,  relationship=False)
                instances_objects[id_number] = instances_object
                print(id_number)
                used.add(id_number)
                work_objects[id_number].instances.append(instances_objects[id_number])
                session.add(work_object)
                session.add(instances_objects[id_number])

            # 
            elif not pd.isna(relationship_essence):
                
                id_number = row['číslo záznamu'] 
                instances_object = add_instance(author_name = author_name, author_code = author_code, title = title, work_id= work_objects[horizontal].id, id = id_number, art_form= art_form, genre=genre, subgenre=subgenre, note=note , first_published= first_published,  relationship=relationship)
                instances_objects[id_number] = instances_object
                work_objects[horizontal].instances.append(instances_objects[id_number])

            else: 
                id_number = horizontal

            if vertical is not None:
                if vertical in instances_objects:
                    instances_association = InstancesHierarchy(is_part_of_id=vertical, has_id=id_number)
                    session.add(instances_association)



    session.commit()

    id11 = session.query(Instance).filter_by(id = 1).first()
    links = [instance.title for instance in id11.has]
    print(f"Instances: {', '.join(links)}")







