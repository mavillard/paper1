
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

# Style
def get_StyleFamily_Style(g, s):
    return [k for k in g[s] if g[s][k]['edgetype'] == 'se clasifica']

# TechniqueR
def get_TechniqueRFamily_TechniqueR(g, t):
    return [k for k in g[t] if g[t][k]['edgetype'] == 'se clasifica']

# Recipe
def get_TechniquesR_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'Tecnica']

def get_TechniqueRFamilies_Recipe(g, r):
    techs = get_TechniquesR_Recipe(g, r)
    return [k for t in techs for k in get_Technique_Family(g, t)]

def get_RecipeFamily_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'se clasifica']

def get_Year_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'publicado en']

def get_Temperature_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'temperatura']

def get_Styles_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'estilo']

def get_StyleFamilies_Recipe(g, r):
    styles = get_Styles_Recipe(g, r)
    return [k for s in styles for k in get_StyleFamily_Style(g, s)]

def get_Preparations_Recipe(g, r):
    return [k for k in g[r] if g[r][k]['edgetype'] == 'elaboracion']

def get_Worlds_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_World_Preparation(g, p)]

def get_Ingredients_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_Ingredients_Preparation(g, p)]

def get_Techniques_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_Techniques_Preparation(g, p)]

def get_Flavors_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_Flavors_Preparation(g, p)]

def get_Products_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_Products_Preparation(g, p)]

def get_PreparationFamilies_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_PreparationFamily_Preparation(g, p)]

def get_components_Recipe(g, r):
    preps = get_Preparations_Recipe(g, r)
    return [k for p in preps for k in get_components_Preparation(g, p)]


# In[3]:


def INGREDIENTS(g1, g2, r):
    ingrs1 = get_components_Recipe(g1, r)
    ingrs2 = get_components_Recipe(g2, r)
    ingrs = []
    ingrs.extend(ingr for ingr in ingrs1 if ingr not in ingrs)
    ingrs.extend(ingr for ingr in ingrs2 if ingr not in ingrs)
    return ingrs

def TECHNIQUES(g1, g2, r):
    techs1 = get_Techniques_Recipe(g1, r)
    techs2 = get_Techniques_Recipe(g2, r)
    techs = []
    techs.extend(tech for tech in techs1 if tech not in techs)
    techs.extend(tech for tech in techs2 if tech not in techs)
    return techs


# In[4]:


def get_nodes_by_type(g, typ):
    return [n for n, data in g.nodes_iter(data=True) if data['nodetype'] == typ]

def get_recipes(g):
    return get_nodes_by_type(g, 'Receta')

def all_ingredients(g):
    ingrs = set()
    for r in get_recipes(g):
        ingrs = ingrs.union(get_components_Recipe(g, r))
    return ingrs

def all_techniques(g):
    techs = set()
    for r in get_recipes(g):
        techs = techs.union(get_Techniques_Recipe(g, r))
    return techs


# In[5]:


import networkx as nx


# In[6]:


g_nlg = nx.read_gexf('out/elbulli_nlg.gexf')


# In[7]:


g_dat = nx.read_gexf('out/elbulli_dat.gexf')


# In[8]:


for g in [g_nlg, g_dat]:
    for p in get_nodes_by_type(g, 'Elaboracion'):
        assert(len(get_PreparationFamily_Preparation(g, p)) <= 1)
        prods = get_Products_Preparation(g, p)
        flavs = get_Flavors_Preparation(g, p)
        ingrs = get_Ingredients_Preparation(g, p)
        comps = get_components_Preparation(g, p)
        assert(set(comps) == set(prods + flavs + ingrs))
        get_Techniques_Preparation(g, p)
        assert(len(get_World_Preparation(g, p)) <= 1)


# In[9]:


for g in [g_nlg, g_dat]:
    for s in get_nodes_by_type(g, 'Estilo'):
        assert(len(get_StyleFamily_Style(g, s)) == 1)


# In[10]:


for g in [g_nlg, g_dat]:
    for t in get_nodes_by_type(g, 'Tecnica'):
        assert(len(get_TechniqueRFamily_TechniqueR(g, t)) == 1)


# In[11]:


for g in [g_nlg, g_dat]:
    for r in get_nodes_by_type(g, 'Receta'):
        techsR = get_TechniquesR_Recipe(g, r)
        techsF = get_TechniqueRFamilies_Recipe(g, r)
        assert(len(techsR) == len(techsF))
        assert(len(get_RecipeFamily_Recipe(g, r)) == 1)
        assert(len(get_Year_Recipe(g, r)) == 1)
        assert(len(get_Temperature_Recipe(g, r)) == 1)
        stylesR = get_Styles_Recipe(g, r)
        stylesF = get_StyleFamilies_Recipe(g, r)
        assert(len(stylesR) == len(stylesF))
        preps = get_Preparations_Recipe(g, r)
        worlds = get_Worlds_Recipe(g, r)
        assert(len(worlds) <= len(preps))
        ingrs = get_Ingredients_Recipe(g, r)
        flavs = get_Flavors_Recipe(g, r)
        prods = get_Products_Recipe(g, r)
        comps = get_components_Recipe(g, r)
        assert(set(comps) == set(prods + flavs + ingrs))
        get_Techniques_Recipe(g, r)
        fams = get_PreparationFamilies_Recipe(g, r)
        assert(len(fams) <= len(preps))


# In[12]:


for r in get_nodes_by_type(g_dat, 'Receta'):
    s11 = set(INGREDIENTS(g_dat, g_nlg, r))
    s12 = set(INGREDIENTS(g_nlg, g_dat, r))
    s13 = set(get_components_Recipe(g_dat, r)).union(get_components_Recipe(g_nlg, r))
    assert(s11 == s12 == s13)
    s21 = set(TECHNIQUES(g_dat, g_nlg, r))
    s22 = set(TECHNIQUES(g_nlg, g_dat, r))
    s23 = set(get_Techniques_Recipe(g_dat, r)).union(get_Techniques_Recipe(g_nlg, r))
    assert(s21 == s22 == s23)


# In[ ]:




