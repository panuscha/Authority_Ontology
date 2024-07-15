from models import Work, WorkInstance, WorkInstancesAssociation, session
import pandas as pd 
import math 

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

def add_work_instances(row, instances_objects):
    """Adds WorkInstance object to list instances_objects

        Parameters
        ----------
        row : pandas row
            row with information about work instace

        instances_objects : list
            list with instances - Work Instances object    

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

    instances_objects[id_number] = WorkInstance(id = id_number, work_id = id_number, title = title, author = author, art_form=art_form, genre=genre, sub_genre=subgenre, note=note)

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

work_objects = {}
instances_objects = {}
used = set()

try:

    for i, row in df.iterrows():
        horizontal = row['horizontální vazba (= patří do souboru díla)']
        relationship_essence = row['kvalita vazby'] 
        if horizontal not in used:
            add_work(row, work_objects)
            add_work_instances(row, instances_objects)
            id_number = row['číslo záznamu'] 
            print(id_number)
            used.add(id_number)
            work_objects[id_number].instances.append(instances_objects[id_number])
            session.add(work_objects[id_number])
            session.add(instances_objects[id_number])
        
            vertical = row['vertikální vazba (=je součást čeho)']
            if vertical is not None:
                if vertical in instances_objects:
                    instances_association = WorkInstancesAssociation(is_part_of_id=vertical, has_id=id_number)
                    session.add(instances_association)
    #elif relationship_essence is not None:
except Exception as error: 
    print(error)
finally:
    #print(list(work_objects.values()))
    #session.bulk_save_objects(list(work_objects.values()))
    #session.bulk_save_objects(list(instances_objects.values()))
    

    # # create values
    work1 = Work(id = 1000, original_title = 'Perlička na dně', original_author = 'Bohumil Hrabal')
    work_instance1 = WorkInstance(id = 1000, work_id = 1, title = 'Perlička na dně', author = 'Bohumil Hrabal')
    work_instance2 = WorkInstance(id = 2000, work_id = 1, title = 'Andělský voči', author = 'Bohumil Hrabal')

    # # add to session
    session.add(work1)
    session.add(work_instance1)
    session.add(work_instance2)
    session.commit()

    id11 = session.query(WorkInstance).filter_by(id = 1).first()
    links = [instance.title for instance in id11.has]
    print(f"Instances: {', '.join(links)}")







