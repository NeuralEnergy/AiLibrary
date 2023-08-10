
from basic_inference_server import Logger
from models.utils import TransformerHelper

  
if __name__ == '__main__':
  PROMPTS = [
    'Capitala Frantei este:',
    
    'Cat face 2 + 2?',
    
    'Cine esti?',
    
    'Cu ce ma poti ajuta?',
    
    """Asteroidea este denumirea unei clase taxonomice din care fac parte stelele de mare.
    Asteroideele sunt animale marine care fac parte din ordinul Echinodermata.
    Stelele de mare cuprind un număr mare de specii care trăiesc în mediul marin, în apropierea coastelor, preferă locurile stâncoase, dar pot fi întâlnite și la adâncimi de 9.000 m, pe nisip sau pe substraturi vegetale.
    Din studiul fosilelor s-a constatat că stelele de mare există de peste 300 milioane de ani.
    Un reprezentant mai cunoscut al grupei este specia Asterias rubens
    In baza acestui text raspundeti la urmatoarea intrebare: Ce sunt stelele de mare?"""
  ]
  
  l = Logger('ROLLM', base_folder='.', app_folder='_cache')
  
  eng1 = TransformerHelper(name='r1', log=l)
  eng2 = TransformerHelper(name='r2', log=l)
  engines = [eng1, eng2]
  
  mem = [round(x.model.get_memory_footprint() / (1024**3),2) for x in engines]
  l.P(f"Model footprints GB: {mem}")
  
  for prompt in PROMPTS:
    for eng in engines:
      for setting, color in zip(['normal', 'c1', 'c3', 's3'], [None, 'b', 'y', 'm']):
        text = eng.generate(prompt, setting=setting)
        l.P("Result for {} on '{}...', setting: {}:".format(
          eng.name, prompt[:20], setting), 
          color='g'
        )
        l.P("Text:\n{}".format(text), color=color)
    