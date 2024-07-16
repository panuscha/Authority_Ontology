from models import Work, WorkInstance, WorkInstancesAssociation, session
import pandas as pd 
import math 
import sqlalchemy_data_model_visualizer

models = [ Work, WorkInstance, WorkInstancesAssociation]
output_file_name = 'my_data_model_diagram'
sqlalchemy_data_model_visualizer.generate_data_model_diagram(models, output_file_name)
sqlalchemy_data_model_visualizer.add_web_font_and_interactivity('my_data_model_diagram.svg', 'my_interactive_data_model_diagram.svg')