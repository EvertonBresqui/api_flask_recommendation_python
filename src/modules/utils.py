from src.config import Config
from src.core.server.instance import server
class Utils():
    
    def transformStringPattern(str):
        str = str.strip()
        str = str.lower()
        str = str.replace(" ", "_")

        return str

    # Get Reference class
    def getClassDynamic(module, path):
        attr_module = module
        path_array = path.split('.')

        for attr_str in path_array:
            attr_module = getattr(attr_module, attr_str)

        return attr_module

    def getFunctionDynamic(ref_instance, name_function):
        if hasattr(ref_instance, name_function) and callable(func := getattr(ref_instance, name_function)):
            return func
        return None

    def getInstanceClassDinamicPlatform(file_name, class_name):

        # Get type algorithm 
        algorithm = Config.getAlgorithm(server.conf_sale['increment_id'])
        if algorithm == None:
            return None
        # Get params algorithm 
        if server.conf_params == None:
            return None

        # File path
        file_path = "src.modules." + str(algorithm) + "." + str(file_name)
        
        # Import and instance class
        file_module = __import__(file_path)

        # Get path reference class
        path_module = "modules." + str(algorithm) + "." + str(file_name) + "." + str(class_name)
        # Get Reference class
        class_reference = Utils.getClassDynamic(file_module, path_module)
        # Instance class         
        obj = class_reference()

        return obj

    def getInstanceClassSpecificPlatform(file_name, class_name):        
        # Get sale type
        sale_type = Config.getSaleGroupType(server.conf_sale_group['id'])
        if sale_type == None:
            return None
        # Get type algorithm 
        algorithm = Config.getAlgorithm(server.conf_sale['increment_id'])
        if algorithm == None:
            return None
        # Get params algorithm 
        if server.conf_params == None:
            return None

        # File path
        file_path = "src.modules." + str(algorithm) + "." + str(sale_type) + "." + str(file_name)
        
        # Import and instance class
        file_module = __import__(file_path)

        # Get path reference class
        path_module = "modules." + str(algorithm) + "." + str(sale_type) + "." + str(file_name) + "." + str(class_name)
        # Get Reference class
        class_reference = Utils.getClassDynamic(file_module, path_module)
        # Instance class         
        obj = class_reference()

        return obj