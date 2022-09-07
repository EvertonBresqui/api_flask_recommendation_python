from src.modules.utils import Utils
class PreProcessing():

    def preProcessing(self):
        # Obtem instancia do objeto
        pre_processing = Utils.getInstanceClassSpecificPlatform('pre_processing', 'PreProcessing')
            
        return pre_processing.process()
