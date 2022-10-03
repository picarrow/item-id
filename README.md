# Item ID
This data pack namespace is intended to serve as a tool for other data packs.
The namespace enables the id of item entities to be more easily and efficiently identified.

### How to Use
Generate a working data pack by executing iid.py.
If you would like to distinguish if a certain item is in a set, before executing the python file, add tags to the tags folder.
Refer to the examples included inside for help formatting.

The data pack ensures that every loaded item entity is given an id that corresponds to the item that it is.
This id is numerical and is stored inside the scoreboard objective picarrow.iid.item_id.
For example:
 - dirt is given the id of 337.
 - feathers are given the id of 381.
 - sponges are given the id of 967.
 - zombified piglin spawn eggs are given the id of 1151.

As of 1.19.2, there are 1,151 items in the game (excluding air), so the ids range from 1 to this number.
To find the numerical id of an item, you can throw it on the ground and query its score from the objective picarrow.iid.item_id.
Or you can use the lookup table provided in the root directory of the namespace.

### How It Works / Why It Might Be Necessary
In Minecraft 1.19.2 and prior versions, identifying more than one kind of item entity can be tricky.
The conventional way to detect the id of an item entity is to exploit the nbt command which is costly.
To distinguish what an item entity is between N item ids will require N nbt checks!
That's far too many at large values of N!
This data pack uses a lesser-known trick with predicates.
Everywhere nbt can be used, a predicate can be used instead which is more efficient.
Yet truly, not efficient enough.
Again, to distinguish between N item ids will require N nbt/predicate checks!
By using predicates in a way that models a ternary search algorithm, the data pack guarantees no more than 3 * log_3(N) predicate checks.
Where for the purposes of this data pack, N is the number of items in the game.

### Limitations / Compatibility
The data pack requires the chunk at chunk coordinate (0, 0) to be forever loaded.
Changing the (nbt) id of an item entity that has already been given an id by the data pack will cause the two to be out of sync.
Make sure to manually correct the id given by the data pack whenever you do this.
Naively using /kill may jeopardize the life of the dummy entity this data pack relies on.
If this entity is killed, item entities may no longer be given the correct id until a reload.
Make sure to exclude entities with the tag picarrow.iid.helper from /kill commands!
