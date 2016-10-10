import field
import entities
import visualization

universe = field.Field(60, 40)  # Create sample universe (length, height

demiurge = field.Demiurge()  # Set deity
universe.set_demiurge(demiurge)

# Fill universe with blanks, blocks, other scenery if necessary
for y in range(10, 30):
    universe.insert_object(20, y, field.Block())

for x in range(21, 40):
    universe.insert_object(x, 10, field.Block())

for y in range(10, 30):
    universe.insert_object(40, y, field.Block())

universe.populate(entities.Creature, 20)  # Populate universe with creatures

visualization.visualize(universe)




