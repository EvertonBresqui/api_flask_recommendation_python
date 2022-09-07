from src.modules.utils import Utils
class CreateModel(object):
    
    def createModel(self):
        # Obtem instancia do objeto
        create_model = Utils.getInstanceClassDinamicPlatform('create_model', 'CreateModel')
            
        return create_model.process()
