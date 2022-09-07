from src.modules.utils import Utils
class Recommendation(object):
    
    def recommendation(self, body):
        # Obtem instancia do objeto
        recommendation_model = Utils.getInstanceClassSpecificPlatform('recommendation', 'Recommendation')
            
        return recommendation_model.process(body)
