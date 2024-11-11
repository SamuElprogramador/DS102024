import pandas as pd

class Display(object):
    """Mostrar la representación HTML de varios objetos"""
    template = """<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>"""
    
    def __init__(self, *args, context=None):
        # Si no se pasa un contexto, se usa el entorno local por defecto
        if context is None:
            context = globals()
        
        # Convertir los nombres de variables a objetos reales si son cadenas
        self.args = [eval(a, context) if isinstance(a, str) else a for a in args]
        self.arg_names = [a if isinstance(a, str) else repr(a) for a in args]
        
    def _repr_html_(self):
        return '\n'.join(self.template.format(name, obj._repr_html_())
                         for name, obj in zip(self.arg_names, self.args))
    
    def __repr__(self):
        return '\n\n'.join(name + '\n' + repr(obj)
                           for name, obj in zip(self.arg_names, self.args))

def make_df(cols:str, ind:list[int]) -> pd.DataFrame:
    """Crear rápidamente un DataFrame"""
    data = {c: [str(c) + str(i) for i in ind]
            for c in cols}
    return pd.DataFrame(data, ind)