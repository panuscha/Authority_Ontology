from models import Work, Instance, InstancesHierarchy, session
import pandas as pd 
import math 
import datetime

def add_work(row, work_objects):
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
    author = row['autor']
    title = row['název']
    id_number = row['číslo záznamu']

    work_objects[id_number] = Work(id = id_number, original_title = title, original_author = author)

    return work_objects

def add_instance(row, instances_objects, relationship):
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
    author = row['autor']
    title = row['název']
    id_number = row['číslo záznamu']
    art_form = row['umělecký druh']
    genre = row['žánr']
    subgenre = row['subžánr']
    note = row['poznámka']
    first_published = datetime.date(row['rok vydání'], 1, 1)

    instances_objects[id_number] = Instance(id = id_number, work_id = id_number, title = title, author = author, first_published = first_published, art_form=art_form, genre=genre, sub_genre=subgenre, note=note)

    if relationship: 
        instances_objects[id_number].relationship_essence = row['kvalita vazby']

    return instances_objects


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

try:

    for i, row in df.iterrows():
        
        horizontal = row['horizontální vazba (= patří do souboru díla)']
        relationship_essence = row['kvalita vazby'] 
        vertical = row['vertikální vazba (=je součást čeho)']
        id_number = row['číslo záznamu']

        # horizontal bond is not present 
        if horizontal not in used:
            
            add_work(row, work_objects)
            add_instance(row, instances_objects, False)
            print(id_number)
            used.add(id_number)
            work_objects[id_number].instances.append(instances_objects[id_number])
            session.add(work_objects[id_number])
            session.add(instances_objects[id_number])

        # 
        elif not pd.isna(relationship_essence):
            
            id_number = row['číslo záznamu'] 
            add_instance(row, instances_objects, True)
            work_objects[horizontal].instances.append(instances_objects[id_number])

        else: 
            id_number = horizontal

        if vertical is not None:
            if vertical in instances_objects:
                instances_association = InstancesHierarchy(is_part_of_id=vertical, has_id=id_number)
                session.add(instances_association)


except Exception as error: 
    print(error)
finally:
    session.commit()

    id11 = session.query(Instance).filter_by(id = 1).first()
    links = [instance.title for instance in id11.has]
    print(f"Instances: {', '.join(links)}")







