from model.model import Model

mymodel = Model()
mymodel.buildGraph(7200000)
n, m = mymodel.printGraphDetails()
print(f"nodi: {n}, archi: {m}")

len, durata = mymodel.componenteConnessa(141)

print(F"len: {len}, durata: {durata}")

mymodel.getSetAlbum(141, 250)
