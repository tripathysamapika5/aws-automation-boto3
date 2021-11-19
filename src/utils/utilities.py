import configparser
import os 

class Utilities:
   
    def get_value_from_json(self, json, id): 
        if isinstance(json, list) :
            for elem in json:
                return self.get_value_from_json(elem, id)
    
        elif isinstance(json, dict):      
            for key in json.keys():
                if key == id:
                    return json.get(id)
                elif isinstance(json.get(key), dict):
                    return self.get_value_from_json(json.get(key), id)
                
                elif isinstance(json.get(key), list):
                    for elem in json.get(key):
                        return self.get_value_from_json(elem, id)
                
    def interpret(self, val):
        try:
            return eval(val)
        except:
            return val
        
    def find_absolute_path(self, relative_file_path):
        working_dir = os.getcwd()
        abs_config_file_path = os.path.join(working_dir, relative_file_path)
        return abs_config_file_path
    
    def find_config_file_path(self, env = 'prod'):
        relative_file_path = 'src/resources/app-config.properties'
        
        if env == 'test':
            relative_file_path = '-test.'.join(relative_file_path.split('.'))
            
        abs_config_file_path = self.find_absolute_path(relative_file_path)
        
        return abs_config_file_path
            
    def read_config_properties(self, env, section_name):
        
        abs_config_file_path = self.find_config_file_path(env)
        
        config = configparser.RawConfigParser()
        config.read(abs_config_file_path)
        result = dict(config.items(section_name))
        for key in result:
            result[key] = self.interpret(result[key])
        
        return   result      
    
    def read_file_to_string(self, relative_file_path):
        abs_config_file_path = self.find_absolute_path(relative_file_path)
        
        with open(abs_config_file_path) as f:
            file_content_string = '\n'.join(list(f.readlines()))
            
        return file_content_string