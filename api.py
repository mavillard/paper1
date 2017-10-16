
# coding: utf-8

# In[1]:


def clean_x(prefix, x):
    return list(map(str.strip, x[len(prefix):].split('/')))

def clean_flavor(f):
    return clean_x('sabor:', f)

def clean_product(p):
    return clean_x('Producto:', p)
    
def clean_ingredient(i):
    return clean_x('', i)
    
def clean_technique(t):
    return clean_x('', t)

def clean_list(f, xs):
    return [k for x in xs for k in f(x)]


# In[2]:


# Preparation
def get_PreparationFamily_Preparation(g, p):
    return [k for k in g[p] if g[p][k]['edgetype'] == 'se clasifica']

def get_Products_Preparation(g, p):
    prod_rels = ['bañado', 'alcohol', 'chocolate', 'lacteo', 'nuevaPasta', 'producto', 'relleno']
    prods = [k for k in g[p] if g[p][k]['edgetype'] in prod_rels]
    return clean_list(clean_product, prods)

def get_Flavors_Preparation(g, p):
    flavs = [k for k in g[p] if g[p][k]['edgetype'] == 'sabor']
    return clean_list(clean_flavor, flavs)

def get_Techniques_Preparation(g, p):
    techs = [k for k in g[p] if g[p][k]['edgetype'] == 'tecnica']
    return clean_list(clean_technique, techs)

def get_Ingredients_Preparation(g, p):
    ingrs = [k for k in g[p] if g[p][k]['edgetype'] == 'composicion']
    return clean_list(clean_ingredient, ingrs)

def get_World_Preparation(g, p):
    return [k for k in g[p] if g[p][k]['edgetype'] == 'mundo']

def get_components_Preparation(g, p):
    prods = get_Products_Preparation(g, p)
    ingrs = get_Ingredients_Preparation(g, p)
    flavs = get_Flavors_Preparation(g, p)
    comps = []
    comps.extend(ingr for ingr in ingrs if ingr not in comps)
    comps.extend(prod for prod in prods if prod not in comps)
    comps.extend(flav for flav in flavs if flav not in comps)
    return comps

# Finish
def get_Techniques_Finish(g, f):
    techs = [k for k in g[f] if g[f][k]['edgetype'] == 'tecnica']
    return clean_list(clean_technique, techs)

def get_Ingredients_Finish(g, f):
    ingrs = [k for k in g[f] if g[f][k]['edgetype'] == 'composicion']
    return clean_list(clean_ingredient, ingrs)

# Style
def get_StyleFamily_Style(g, s):
    return [k for k in g[s] if g[s][k]['edgetype'] == 'se clasifica']

# TechniqueR
def get_TechniqueRFamily_TechniqueR(g, t):
    return [k for k in g[t] if g[t][k]['edgetype'] == 'se clasifica']

# Recipe
def get_Finish_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'acabacion']

def get_TechniquesR_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'tecnica']

def get_TechniquesRFamilies_Recipe(g, r):
    techs = get_TechniquesR_Recipe(g, r)
    return [k for t in techs for k in get_TechniqueRFamily_TechniqueR(g, t)]

def get_RecipeFamily_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'se clasifica']

def get_Year_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'publicado en']

def get_Temperature_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'temperatura']

def get_Styles_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'estilo']

def get_StylesFamilies_Recipe(g, r):
    styles = get_Styles_Recipe(g, r)
    return [k for s in styles for k in get_StyleFamily_Style(g, s)]

def get_Preparations_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'elaboracion']

def get_Worlds_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_World_Preparation(g, p)]

def get_Techniques_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    preps_techs = [k for p in preps for k in get_Techniques_Preparation(g, p)]
    finish = get_Finish_Recipe(g, r)
    finish_techs = [k for f in finish for k in get_Techniques_Finish(g, f)]
    return preps_techs + finish_techs

def get_PreparationsFamilies_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_PreparationFamily_Preparation(g, p)]

def get_components_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    preps_comps = [k for p in preps for k in get_components_Preparation(g, p)]
    finish = get_Finish_Recipe(g, r)
    finish_ingrs = [k for f in finish for k in get_Ingredients_Finish(g, f)]
    return preps_comps + finish_ingrs


# In[3]:


def INGREDIENTS(g1, g2, r):
    ingrs1 = map(str.lower, get_components_Recipe(g1, r))
    ingrs2 = map(str.lower, get_components_Recipe(g2, r))
    ingrs = []
    ingrs.extend(ingr for ingr in ingrs1 if ingr not in ingrs)
    ingrs.extend(ingr for ingr in ingrs2 if ingr not in ingrs)
    return ingrs

def TECHNIQUES(g1, g2, r):
    techs1 = map(str.lower, get_Techniques_Recipe(g1, r))
    techs2 = map(str.lower, get_Techniques_Recipe(g2, r))
    techs = []
    techs.extend(tech for tech in techs1 if tech not in techs)
    techs.extend(tech for tech in techs2 if tech not in techs)
    return techs


# In[4]:


def nodes_by_type(g, typ, data=False):
    return [
        (n, d) if data else n
        for n, d in g.nodes_iter(data=True)
        if d['nodetype'] == typ
    ]

def all_ingredients(g):
    ingrs = set()
    for r in nodes_by_type(g, 'Receta'):
        ingrs = ingrs.union(get_components_Recipe(g, r))
    return ingrs

def all_techniques(g):
    techs = set()
    for r in nodes_by_type(g, 'Receta'):
        techs = techs.union(get_Techniques_Recipe(g, r))
    return techs


# In[ ]:




